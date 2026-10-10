import sqlite3
import json
import os
from typing import Optional, List, Dict, Any
from pathlib import Path
from app.config import settings
from app.models import Snapshot, BusinessProfile, ScanQualityMetrics, ActionBrief, Signal, MarketItem, FeedbackRequest

DB_PATH = Path(settings.DATABASE_URL.replace("sqlite:///", ""))

def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL;")
    return conn

def init_db():
    conn = get_connection()
    try:
        with conn:
            conn.execute("""
            CREATE TABLE IF NOT EXISTS snapshots (
                id TEXT PRIMARY KEY,
                created_at TEXT NOT NULL,
                business_name TEXT NOT NULL,
                category TEXT NOT NULL,
                market TEXT NOT NULL,
                gl TEXT NOT NULL,
                hl TEXT NOT NULL,
                competitors_json TEXT NOT NULL,
                items_json TEXT NOT NULL,
                signals_json TEXT NOT NULL,
                brief_json TEXT,
                quality_metrics_json TEXT NOT NULL,
                is_baseline INTEGER NOT NULL DEFAULT 0,
                is_sample INTEGER NOT NULL DEFAULT 0
            );
            """)

            conn.execute("""
            CREATE TABLE IF NOT EXISTS feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                signal_id TEXT NOT NULL,
                competitor TEXT NOT NULL,
                signal_type TEXT NOT NULL,
                item_title TEXT,
                is_useful INTEGER NOT NULL,
                created_at TEXT NOT NULL
            );
            """)
    finally:
        conn.close()

def save_snapshot(snapshot: Snapshot) -> None:
    conn = get_connection()
    try:
        with conn:
            # If this is set as baseline, demote previous baselines for same category/market
            if snapshot.is_baseline:
                conn.execute(
                    "UPDATE snapshots SET is_baseline = 0 WHERE category = ? AND market = ?",
                    (snapshot.business_profile.category, snapshot.business_profile.market)
                )

            conn.execute("""
            INSERT OR REPLACE INTO snapshots (
                id, created_at, business_name, category, market, gl, hl,
                competitors_json, items_json, signals_json, brief_json,
                quality_metrics_json, is_baseline, is_sample
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                snapshot.id,
                snapshot.created_at,
                snapshot.business_profile.business_name,
                snapshot.business_profile.category,
                snapshot.business_profile.market,
                snapshot.business_profile.gl,
                snapshot.business_profile.hl,
                json.dumps(snapshot.business_profile.competitors),
                json.dumps([item.model_dump() for item in snapshot.items]),
                json.dumps([sig.model_dump() for sig in snapshot.signals]),
                json.dumps(snapshot.brief.model_dump()) if snapshot.brief else None,
                json.dumps(snapshot.quality_metrics.model_dump()),
                1 if snapshot.is_baseline else 0,
                1 if snapshot.is_sample else 0
            ))
    finally:
        conn.close()

def get_snapshot(snapshot_id: str) -> Optional[Snapshot]:
    conn = get_connection()
    try:
        cur = conn.execute("SELECT * FROM snapshots WHERE id = ?", (snapshot_id,))
        row = cur.fetchone()
        if not row:
            return None
        return _row_to_snapshot(row)
    finally:
        conn.close()

def list_snapshots(limit: int = 50) -> List[Dict[str, Any]]:
    conn = get_connection()
    try:
        cur = conn.execute("""
        SELECT id, created_at, business_name, category, market, is_baseline, is_sample,
               length(items_json) as items_len, length(signals_json) as signals_len
        FROM snapshots
        ORDER BY created_at DESC
        LIMIT ?
        """, (limit,))
        rows = cur.fetchall()
        return [
            {
                "id": r["id"],
                "created_at": r["created_at"],
                "business_name": r["business_name"],
                "category": r["category"],
                "market": r["market"],
                "is_baseline": bool(r["is_baseline"]),
                "is_sample": bool(r["is_sample"]),
            }
            for r in rows
        ]
    finally:
        conn.close()

def get_active_baseline(category: str, market: str) -> Optional[Snapshot]:
    conn = get_connection()
    try:
        cur = conn.execute("""
        SELECT * FROM snapshots 
        WHERE is_baseline = 1 AND category = ? AND market = ?
        ORDER BY created_at DESC LIMIT 1
        """, (category, market))
        row = cur.fetchone()
        if not row:
            # Fallback to any latest baseline if category matches
            cur = conn.execute("""
            SELECT * FROM snapshots 
            WHERE is_baseline = 1
            ORDER BY created_at DESC LIMIT 1
            """)
            row = cur.fetchone()
        if not row:
            return None
        return _row_to_snapshot(row)
    finally:
        conn.close()

def set_active_baseline(snapshot_id: str) -> bool:
    conn = get_connection()
    try:
        with conn:
            cur = conn.execute("SELECT category, market FROM snapshots WHERE id = ?", (snapshot_id,))
            row = cur.fetchone()
            if not row:
                return False
            conn.execute("UPDATE snapshots SET is_baseline = 0 WHERE category = ? AND market = ?", 
                         (row["category"], row["market"]))
            conn.execute("UPDATE snapshots SET is_baseline = 1 WHERE id = ?", (snapshot_id,))
            return True
    finally:
        conn.close()

def record_feedback(req: FeedbackRequest) -> None:
    conn = get_connection()
    try:
        with conn:
            from datetime import datetime, timezone
            now = datetime.now(timezone.utc).isoformat()
            conn.execute("""
            INSERT INTO feedback (signal_id, competitor, signal_type, item_title, is_useful, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (
                req.signal_id,
                req.competitor,
                req.signal_type,
                req.item_title or "",
                1 if req.is_useful else 0,
                now
            ))
            # Also update signal feedback in snapshots if found
            cur = conn.execute("SELECT id, signals_json FROM snapshots WHERE signals_json LIKE ?", (f"%{req.signal_id}%",))
            for s_row in cur.fetchall():
                try:
                    signals = json.loads(s_row["signals_json"])
                    updated = False
                    for s in signals:
                        if s.get("id") == req.signal_id:
                            s["is_useful"] = req.is_useful
                            updated = True
                    if updated:
                        conn.execute("UPDATE snapshots SET signals_json = ? WHERE id = ?", (json.dumps(signals), s_row["id"]))
                except Exception:
                    pass
    finally:
        conn.close()

def get_suppressed_patterns() -> List[Dict[str, Any]]:
    conn = get_connection()
    try:
        cur = conn.execute("""
        SELECT competitor, signal_type, item_title 
        FROM feedback 
        WHERE is_useful = 0
        """)
        rows = cur.fetchall()
        return [
            {
                "competitor": r["competitor"].lower(),
                "signal_type": r["signal_type"],
                "item_title": r["item_title"].lower() if r["item_title"] else ""
            }
            for r in rows
        ]
    finally:
        conn.close()

def _row_to_snapshot(row: sqlite3.Row) -> Snapshot:
    return Snapshot(
        id=row["id"],
        created_at=row["created_at"],
        business_profile=BusinessProfile(
            business_name=row["business_name"],
            category=row["category"],
            market=row["market"],
            gl=row["gl"],
            hl=row["hl"],
            competitors=json.loads(row["competitors_json"])
        ),
        items=[MarketItem(**item) for item in json.loads(row["items_json"])],
        signals=[Signal(**sig) for sig in json.loads(row["signals_json"])],
        brief=ActionBrief(**json.loads(row["brief_json"])) if row["brief_json"] else None,
        quality_metrics=ScanQualityMetrics(**json.loads(row["quality_metrics_json"])),
        is_baseline=bool(row["is_baseline"]),
        is_sample=bool(row["is_sample"])
    )
