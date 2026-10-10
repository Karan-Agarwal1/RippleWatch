from datetime import datetime, timezone, timedelta
from app.models import (
    Snapshot, BusinessProfile, MarketItem, Signal, EvidenceItem,
    ActionBrief, ActionItem, ScanQualityMetrics
)

def create_sample_baseline_snapshot() -> Snapshot:
    """
    Creates a realistic baseline snapshot representing market data from 14 days ago.
    Clearly labeled with is_sample=True and is_baseline=True.
    """
    baseline_time = (datetime.now(timezone.utc) - timedelta(days=14)).isoformat()

    items = [
        MarketItem(
            id="item_milton_thermo_1000",
            source_type="shopping",
            query="Milton reusable steel water bottles",
            title="Milton Thermosteel Flip Lid Flask 1000ml Silver",
            seller_or_source="Amazon IN",
            url="https://www.amazon.in/Milton-Thermosteel-Flip-Flask-Silver/dp/B0073Q46MG",
            snippet="Milton Thermosteel 1000 ml Vacuum Insulated Flask Keeps Drinks Hot & Cold 24 Hours.",
            price=990.0,
            currency="INR",
            product_id="milton_ts_1000_in",
            location_context="in",
            observed_at=baseline_time,
            competitor="Milton",
            raw_attributes={"rating": 4.3, "reviews": 18240}
        ),
        MarketItem(
            id="item_milton_duo_750",
            source_type="shopping",
            query="Milton reusable steel water bottles",
            title="Milton Duo DLX 750ml Stainless Steel Water Bottle",
            seller_or_source="Flipkart",
            url="https://www.flipkart.com/milton-duo-dlx-750-ml-bottle/p/itm12345",
            snippet="100% leak proof single wall grade 304 stainless steel bottle.",
            price=475.0,
            currency="INR",
            product_id="milton_duo_750_in",
            location_context="in",
            observed_at=baseline_time,
            competitor="Milton",
            raw_attributes={"rating": 4.1, "reviews": 6500}
        ),
        MarketItem(
            id="item_cello_lifestyle_1000",
            source_type="shopping",
            query="Cello reusable steel water bottles",
            title="Cello Lifestyle Stainless Steel Water Bottle 1000ml",
            seller_or_source="Amazon IN",
            url="https://www.amazon.in/Cello-Lifestyle-Stainless-Bottle-1000ml/dp/B07XYZ1234",
            snippet="BPA free durable ergonomic water bottle for gym and office.",
            price=620.0,
            currency="INR",
            product_id="cello_ls_1000_in",
            location_context="in",
            observed_at=baseline_time,
            competitor="Cello",
            raw_attributes={"rating": 4.2, "reviews": 9400}
        ),
        MarketItem(
            id="item_cello_puro_900",
            source_type="shopping",
            query="Cello reusable steel water bottles",
            title="Cello Puro Steel-X Insulated Bottle 900ml Matte Black",
            seller_or_source="Jiomart",
            url="https://www.jiomart.com/p/groceries/cello-puro-steel-x-900ml/590001",
            snippet="Double walled PU insulated stainless steel bottle.",
            price=550.0,
            currency="INR",
            product_id="cello_puro_900_in",
            location_context="in",
            observed_at=baseline_time,
            competitor="Cello",
            raw_attributes={"rating": 4.0, "reviews": 3200}
        ),
        MarketItem(
            id="item_borosil_hydra_700",
            source_type="shopping",
            query="Borosil reusable steel water bottles",
            title="Borosil Hydra Trek Stainless Steel Vacuum Bottle 700ml Blue",
            seller_or_source="Amazon IN",
            url="https://www.amazon.in/Borosil-Hydra-Stainless-Vacuum-Bottle/dp/B08XYZ9876",
            snippet="Food grade SS 304 inside and out, keeps cold for 24h, hot for 20h.",
            price=895.0,
            currency="INR",
            product_id="borosil_trek_700_in",
            location_context="in",
            observed_at=baseline_time,
            competitor="Borosil",
            raw_attributes={"rating": 4.4, "reviews": 11200}
        ),
        MarketItem(
            id="item_borosil_flask_1000",
            source_type="shopping",
            query="Borosil reusable steel water bottles",
            title="Borosil Stainless Steel Flask with Thermal Jacket 1000ml",
            seller_or_source="Borosil Official",
            url="https://myborosil.com/products/stainless-steel-flask-1000ml",
            snippet="Premium double wall vacuum insulated flask with carry pouch.",
            price=1120.0,
            currency="INR",
            product_id="borosil_flask_1000_in",
            location_context="in",
            observed_at=baseline_time,
            competitor="Borosil",
            raw_attributes={"rating": 4.5, "reviews": 4800}
        ),
        MarketItem(
            id="item_milton_news_baseline",
            source_type="news",
            query="Milton launch",
            title="Hamilton Housewares (Milton) announces green packaging shift across domestic ranges",
            seller_or_source="Business Standard",
            url="https://www.business-standard.com/article/companies/milton-packaging-announcement",
            snippet="Hamilton Housewares moves toward 100% recyclable outer carton packaging for insulated ware.",
            price=None,
            currency="INR",
            product_id=None,
            location_context="in",
            observed_at=baseline_time,
            competitor="Milton",
            raw_attributes={"date": "14 days ago"}
        )
    ]

    quality = ScanQualityMetrics(
        total_results_fetched=14,
        duplicates_removed=4,
        noise_filtered=3,
        working_links_pct=100.0,
        verification_disclaimer="Sample baseline seeded for comparative evaluation. Not a live scan."
    )

    return Snapshot(
        id="snap_sample_baseline_in_bottles",
        created_at=baseline_time,
        business_profile=BusinessProfile(
            business_name="EcoVessel India",
            category="reusable steel water bottles",
            market="India",
            gl="in",
            hl="en",
            competitors=["Milton", "Cello", "Borosil"]
        ),
        items=items,
        signals=[],
        brief=None,
        quality_metrics=quality,
        is_baseline=True,
        is_sample=True
    )
