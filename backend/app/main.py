import os
import uuid
from datetime import datetime, timezone
from typing import List, Optional, Dict, Any
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.models import (
    ScanRequest, Snapshot, BusinessProfile, ScanQualityMetrics,
    SuggestCompetitorsRequest, FeedbackRequest, AppStatusResponse,
    MarketItem, Signal
)
from app.database import (
    init_db, save_snapshot, get_snapshot, list_snapshots,
    get_active_baseline, set_active_baseline, record_feedback
)
from app.serpapi_client import serpapi_client
from app.normalizer import process_raw_serp_batch
from app.detector import MarketChangeDetector
from app.brief_generator import ActionBriefGenerator
from app.sample_data import create_sample_baseline_snapshot

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize SQLite database on startup
    init_db()
    # Check if a sample baseline exists; if no snapshots at all, seed the sample baseline
    existing = list_snapshots(limit=1)
    if not existing:
        sample_baseline = create_sample_baseline_snapshot()
        save_snapshot(sample_baseline)
    yield

app = FastAPI(
    title="RippleWatch API",
    description="AI Market-Change Agent for Small Businesses (SerpApi Hackathon MVP)",
    version="1.0.0",
    lifespan=lifespan
)

from fastapi.responses import HTMLResponse
from app.web_ui import get_dashboard_html

# CORS Middleware (permits Next.js frontend local dev on 3000 or custom ports)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", response_class=HTMLResponse)
async def serve_dashboard():
    """
    Renders the interactive RippleWatch dashboard.
    """
    return HTMLResponse(content=get_dashboard_html())

@app.get("/api/status", response_model=AppStatusResponse)
async def get_system_status():
    """
    Checks operational status, API keys, cache metrics, and active baseline.
    """
    cache_files = [f for f in os.listdir(settings.CACHE_DIR) if f.startswith("serp_")]
    all_snaps = list_snapshots(limit=100)
    current_baseline = get_active_baseline("reusable steel water bottles", "India")

    return AppStatusResponse(
        status="operational",
        serpapi_configured=bool(settings.SERPAPI_KEY.strip()),
        gemini_configured=bool(settings.GEMINI_API_KEY.strip()),
        cache_entries_count=len(cache_files),
        total_snapshots=len(all_snaps),
        active_baseline_id=current_baseline.id if current_baseline else None
    )

@app.post("/api/scan", response_model=Snapshot)
async def run_market_scan(req: ScanRequest):
    """
    Executes a market scan via SerpApi across tracked competitors.
    Normalizes results, detects changes against baseline, synthesizes Action Brief, and persists snapshot.
    """
    profile = req.business_profile
    if not profile.competitors:
        raise HTTPException(status_code=400, detail="At least one competitor must be provided for tracking.")

    # 1. Fetch raw market data for each competitor concurrently
    raw_by_competitor: Dict[str, Dict[str, Any]] = {}
    for competitor in profile.competitors:
        comp_data = await serpapi_client.fetch_competitor_data(
            competitor=competitor,
            category=profile.category,
            gl=profile.gl,
            hl=profile.hl,
            use_cache=req.use_cache
        )
        raw_by_competitor[competitor] = comp_data

    # Count total raw results fetched before cleaning
    total_raw_count = 0
    for comp, sections in raw_by_competitor.items():
        for s_key, s_val in sections.items():
            if s_val.get("success"):
                d = s_val.get("data", {})
                total_raw_count += len(d.get("shopping_results", []))
                total_raw_count += len(d.get("inline_shopping_results", []))
                total_raw_count += len(d.get("news_results", []))
                total_raw_count += len(d.get("organic_results", []))

    # 2. Normalize, filter noise, and deduplicate
    deduped_items, duplicates_removed, noise_filtered = process_raw_serp_batch(
        raw_results_by_competitor=raw_by_competitor,
        category=profile.category,
        gl=profile.gl
    )

    # 3. Calculate link validity percentage
    valid_links = sum(1 for it in deduped_items if it.url.startswith("http"))
    working_links_pct = round((valid_links / max(len(deduped_items), 1)) * 100.0, 1)

    now_utc = datetime.now(timezone.utc).isoformat()
    snapshot_id = f"snap_{uuid.uuid4().hex[:12]}"

    disclaimer = (
        "What this prototype does NOT verify: Regional delivery fee variations, "
        "cart-level bank instant discounts, seller-specific warehouse stockout states, "
        "or private marketplace wholesale agreements."
    )

    quality_metrics = ScanQualityMetrics(
        total_results_fetched=total_raw_count,
        duplicates_removed=duplicates_removed,
        noise_filtered=noise_filtered,
        working_links_pct=working_links_pct,
        verification_disclaimer=disclaimer
    )

    # If user explicitly requested creating a baseline snapshot
    if req.is_baseline_creation:
        baseline_snapshot = Snapshot(
            id=snapshot_id,
            created_at=now_utc,
            business_profile=profile,
            items=deduped_items,
            signals=[],
            brief=None,
            quality_metrics=quality_metrics,
            is_baseline=True,
            is_sample=False
        )
        save_snapshot(baseline_snapshot)
        return baseline_snapshot

    # 4. Compare with baseline snapshot
    baseline_snapshot: Optional[Snapshot] = None
    if req.compare_with_snapshot_id:
        baseline_snapshot = get_snapshot(req.compare_with_snapshot_id)
    if not baseline_snapshot:
        baseline_snapshot = get_active_baseline(profile.category, profile.market)

    baseline_items = baseline_snapshot.items if baseline_snapshot else []

    # 5. Detect changes and emit signals
    signals = MarketChangeDetector.detect_changes(
        current_items=deduped_items,
        baseline_items=baseline_items,
        tracked_competitors=profile.competitors
    )

    # 6. Generate Action Brief (Gemini or deterministic rule fallback)
    brief = await ActionBriefGenerator.generate_brief(
        signals=signals,
        items=deduped_items,
        business_category=profile.category
    )

    # 7. Create and persist snapshot
    new_snapshot = Snapshot(
        id=snapshot_id,
        created_at=now_utc,
        business_profile=profile,
        items=deduped_items,
        signals=signals,
        brief=brief,
        quality_metrics=quality_metrics,
        is_baseline=False,
        is_sample=False
    )
    save_snapshot(new_snapshot)

    return new_snapshot

@app.get("/api/snapshots")
async def get_snapshots(limit: int = 50):
    """
    Returns history of recent market snapshots.
    """
    return list_snapshots(limit=limit)

@app.get("/api/snapshots/{snapshot_id}", response_model=Snapshot)
async def get_snapshot_detail(snapshot_id: str):
    """
    Returns full details of a specific snapshot by ID.
    """
    snap = get_snapshot(snapshot_id)
    if not snap:
        raise HTTPException(status_code=404, detail="Snapshot not found")
    return snap

@app.get("/api/baseline/current", response_model=Optional[Snapshot])
async def get_current_baseline(
    category: str = Query("reusable steel water bottles"),
    market: str = Query("India")
):
    """
    Fetches the currently active baseline snapshot.
    """
    return get_active_baseline(category, market)

@app.post("/api/baseline/sample", response_model=Snapshot)
async def seed_sample_baseline():
    """
    Seeds a sample baseline snapshot (clearly labeled sample data) so change detection can be demoed immediately.
    """
    sample = create_sample_baseline_snapshot()
    save_snapshot(sample)
    set_active_baseline(sample.id)
    return sample

@app.post("/api/baseline/set/{snapshot_id}")
async def make_baseline(snapshot_id: str):
    """
    Promotes a snapshot to be the active baseline.
    """
    success = set_active_baseline(snapshot_id)
    if not success:
        raise HTTPException(status_code=404, detail="Snapshot not found")
    return {"success": True, "message": f"Snapshot {snapshot_id} is now the active baseline."}

@app.post("/api/competitors/suggest")
async def suggest_competitors(req: SuggestCompetitorsRequest):
    """
    Suggests top competitor brands for category and market via SerpApi.
    """
    suggestions = await serpapi_client.suggest_competitors(
        category=req.category,
        market=req.market,
        gl=req.gl,
        hl=req.hl
    )
    return {"category": req.category, "suggested_competitors": suggestions}

@app.post("/api/signals/feedback")
async def submit_feedback(req: FeedbackRequest):
    """
    Records Useful or Irrelevant feedback for a signal to suppress future false positives.
    """
    record_feedback(req)
    return {
        "success": True,
        "message": f"Feedback recorded for signal {req.signal_id} ({'Useful' if req.is_useful else 'Irrelevant'})."
    }
