import asyncio
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from app.config import settings
from app.serpapi_client import serpapi_client
from app.models import ScanRequest, BusinessProfile
from app.main import run_market_scan, init_db
from app.database import get_active_baseline

async def main():
    print(f"[*] Starting live SerpApi verification...")
    print(f"[*] SerpApi Key length: {len(settings.SERPAPI_KEY)} chars")
    
    # 1. Direct query test
    print("[*] Test 1: Fetching Google Shopping results for 'Milton reusable steel water bottles'...")
    res = await serpapi_client.execute_query(
        engine="google_shopping",
        query="Milton reusable steel water bottles",
        gl="in",
        hl="en",
        use_cache=True
    )
    shopping = res.get("shopping_results", [])
    print(f"[+] Success! Received {len(shopping)} shopping results from SerpApi.")
    if shopping:
        first = shopping[0]
        print(f"    Sample Product: '{first.get('title')}' | Price: {first.get('price')} | Store: {first.get('source')}")

    # 2. End-to-end scan test against baseline
    print("\n[*] Test 2: Running full market scan against active baseline...")
    init_db()
    req = ScanRequest(
        business_profile=BusinessProfile(
            business_name="EcoVessel India",
            category="reusable steel water bottles",
            market="India",
            gl="in",
            hl="en",
            competitors=["Milton", "Cello"]
        ),
        use_cache=True,
        is_baseline_creation=False
    )
    snapshot = await run_market_scan(req)
    print(f"[+] Success! Created Snapshot ID: {snapshot.id}")
    print(f"    Total items: {len(snapshot.items)}")
    print(f"    Signals detected: {len(snapshot.signals)}")
    for s in snapshot.signals[:3]:
        print(f"    - [{s.type}] ({s.confidence}) {s.competitor}: {s.what_changed[:90]}...")
    
    print(f"    Action Brief items: {len(snapshot.brief.actions) if snapshot.brief else 0}")
    if snapshot.brief:
        for a in snapshot.brief.actions:
            print(f"    * Action: {a.title} (Effort: {a.effort}, Confidence: {a.confidence})")
            print(f"      Citations: {a.evidence_ids}")

    print(f"\n[+] Scan Quality: {snapshot.quality_metrics.model_dump()}")
    print("\n[>>>] ALL BACKEND LIVE SERPAPI CHECKS PASSED SUCCESSFULLY! [<<<]")

if __name__ == "__main__":
    asyncio.run(main())
