import pytest
from app.models import MarketItem, FeedbackRequest
from app.detector import MarketChangeDetector
from app.database import init_db, record_feedback

@pytest.fixture(autouse=True)
def setup_database():
    init_db()

def create_item(item_id, competitor, title, price, seller="Amazon IN", source_type="shopping", product_id=None, snippet=""):
    return MarketItem(
        id=item_id,
        source_type=source_type,
        query=f"{competitor} bottles",
        title=title,
        seller_or_source=seller,
        url=f"https://example.com/{item_id}",
        snippet=snippet or f"Description for {title}",
        price=price,
        currency="INR",
        product_id=product_id or item_id,
        location_context="in",
        observed_at="2026-10-10T00:00:00Z",
        competitor=competitor
    )

def test_detector_success_price_change():
    baseline = [
        create_item("b_1", "Milton", "Milton Thermosteel 1000ml", 1000.0, product_id="milton_ts_1000")
    ]
    # Current has 20% price drop (₹800 vs ₹1000)
    current = [
        create_item("c_1", "Milton", "Milton Thermosteel 1000ml", 800.0, product_id="milton_ts_1000")
    ]

    signals = MarketChangeDetector.detect_changes(current, baseline, ["Milton"])
    assert len(signals) == 1
    assert signals[0].type == "PRICE_CHANGE"
    assert signals[0].competitor == "Milton"
    assert "dropped by 20.0%" in signals[0].what_changed
    assert len(signals[0].evidence) == 2

def test_detector_no_change():
    baseline = [
        create_item("b_1", "Milton", "Milton Thermosteel 1000ml", 1000.0, product_id="milton_ts_1000"),
        create_item("b_2", "Cello", "Cello Lifestyle 750ml", 500.0, product_id="cello_ls_750")
    ]
    current = [
        create_item("c_1", "Milton", "Milton Thermosteel 1000ml", 1000.0, product_id="milton_ts_1000"),
        create_item("c_2", "Cello", "Cello Lifestyle 750ml", 500.0, product_id="cello_ls_750")
    ]

    signals = MarketChangeDetector.detect_changes(current, baseline, ["Milton", "Cello"])
    assert len(signals) == 0

def test_detector_no_results():
    baseline = [
        create_item("b_1", "Milton", "Milton Thermosteel 1000ml", 1000.0)
    ]
    current = []

    signals = MarketChangeDetector.detect_changes(current, baseline, ["Milton"])
    assert len(signals) == 0

def test_detector_success_promotion():
    baseline = [
        create_item("b_1", "Cello", "Cello Duro Steel Bottle 1000ml", 600.0, product_id="cello_duro")
    ]
    # Current item includes 'pack of 2' promo
    current = [
        create_item("c_1", "Cello", "Cello Duro Steel Bottle 1000ml (Pack of 2 Combo)", 1050.0, product_id="cello_duro_combo")
    ]

    signals = MarketChangeDetector.detect_changes(current, baseline, ["Cello"])
    promo_signals = [s for s in signals if s.type == "PROMOTION"]
    assert len(promo_signals) >= 1
    assert promo_signals[0].competitor == "Cello"

def test_detector_success_new_product():
    baseline = [
        create_item("b_1", "Borosil", "Borosil Hydra 700ml", 850.0, product_id="borosil_hydra_700")
    ]
    current = [
        create_item("b_1", "Borosil", "Borosil Hydra 700ml", 850.0, product_id="borosil_hydra_700"),
        create_item("c_new", "Borosil", "Borosil Apex Double Wall Flask 1200ml", 1299.0, product_id="borosil_apex_1200")
    ]

    signals = MarketChangeDetector.detect_changes(current, baseline, ["Borosil"])
    new_prod_signals = [s for s in signals if s.type == "NEW_PRODUCT"]
    assert len(new_prod_signals) == 1
    assert new_prod_signals[0].competitor == "Borosil"
    assert "Borosil Apex Double Wall Flask 1200ml" in new_prod_signals[0].what_changed

def test_detector_multi_source_confirmed_confidence():
    baseline = [
        create_item("b_1", "Milton", "Milton Thermosteel 1000ml", 1000.0, seller="Amazon IN", product_id="milton_ts_1000")
    ]
    # Price drop observed across both Amazon and Flipkart
    current = [
        create_item("c_1", "Milton", "Milton Thermosteel 1000ml", 850.0, seller="Amazon IN", product_id="milton_ts_1000"),
        create_item("c_2", "Milton", "Milton Thermosteel 1000ml", 850.0, seller="Flipkart", product_id="milton_ts_1000_fk")
    ]

    signals = MarketChangeDetector.detect_changes(current, baseline, ["Milton"])
    price_signals = [s for s in signals if s.type == "PRICE_CHANGE"]
    assert len(price_signals) >= 1
    # Multiple sources present in current snapshot elevates confidence to 'confirmed'
    assert price_signals[0].confidence == "confirmed"

def test_detector_feedback_suppression():
    # User marks an irrelevant false positive
    record_feedback(FeedbackRequest(
        signal_id="sig_test_123",
        competitor="Milton",
        signal_type="PRICE_CHANGE",
        item_title="Milton Minor Product",
        is_useful=False
    ))

    baseline = [
        create_item("b_1", "Milton", "Milton Minor Product 500ml", 400.0, product_id="m_minor")
    ]
    current = [
        create_item("c_1", "Milton", "Milton Minor Product 500ml", 350.0, product_id="m_minor")
    ]

    signals = MarketChangeDetector.detect_changes(current, baseline, ["Milton"])
    # Should be suppressed by user feedback rule
    assert len(signals) == 0
