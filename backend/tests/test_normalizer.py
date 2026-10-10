import pytest
from app.normalizer import (
    parse_price_string, is_noise_item, MarketItemNormalizer,
    normalize_title_for_comparison, generate_item_id
)

def test_parse_price_string():
    assert parse_price_string("₹1,299") == (1299.0, "INR")
    assert parse_price_string("₹ 499.50") == (499.5, "INR")
    assert parse_price_string("Rs. 850") == (850.0, "INR")
    assert parse_price_string("$24.99") == (24.99, "USD")
    assert parse_price_string(1500) == (1500.0, "INR")
    assert parse_price_string(None) == (None, "INR")
    assert parse_price_string("Invalid price") == (None, "INR")

def test_is_noise_item_accessories():
    cat = "reusable steel water bottles"
    # Should be flagged as noise
    assert is_noise_item("Long bottle cleaning brush with soft bristles", "", cat) is True
    assert is_noise_item("Silicone protective boot sleeve for 32oz bottle", "", cat) is True
    assert is_noise_item("Replacement lid and straw set", "", cat) is True
    assert is_noise_item("Water bottle stickers cute waterproof pack of 50", "", cat) is True

    # Genuine water bottles should NOT be noise
    assert is_noise_item("Milton Thermosteel Flip Lid Flask 1000ml Silver", "", cat) is False
    assert is_noise_item("Borosil Hydra Trek Stainless Steel Vacuum Bottle 700ml", "", cat) is False
    assert is_noise_item("Cello Puro Steel-X Insulated Bottle 900ml", "", cat) is False

def test_shopping_normalization():
    raw_shopping = {
        "title": "Milton Thermosteel 1000ml Flask",
        "link": "https://amazon.in/dp/B001",
        "source": "Amazon IN",
        "price": "₹999",
        "product_id": "prod_12345",
        "snippet": "Stainless steel 304 grade vacuum insulated bottle."
    }
    item = MarketItemNormalizer.normalize_shopping_item(
        raw=raw_shopping,
        query="Milton reusable steel water bottles",
        competitor="Milton",
        location="in"
    )
    assert item is not None
    assert item.title == "Milton Thermosteel 1000ml Flask"
    assert item.price == 999.0
    assert item.currency == "INR"
    assert item.product_id == "prod_12345"
    assert item.seller_or_source == "Amazon IN"
    assert item.competitor == "Milton"
    assert item.source_type == "shopping"

def test_news_normalization():
    raw_news = {
        "title": "Borosil reports 22% growth in insulated drinkware category",
        "link": "https://financialexpress.com/article/1",
        "source": {"name": "Financial Express"},
        "snippet": "Borosil expands production of stainless steel bottles."
    }
    item = MarketItemNormalizer.normalize_news_item(
        raw=raw_news,
        query="Borosil launch",
        competitor="Borosil",
        location="in"
    )
    assert item is not None
    assert item.source_type == "news"
    assert item.seller_or_source == "Financial Express"
    assert item.price is None
    assert item.competitor == "Borosil"
