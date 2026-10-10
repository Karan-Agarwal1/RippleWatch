import pytest
from app.models import MarketItem
from app.normalizer import deduplicate_items

def test_dedup_by_product_id():
    item1 = MarketItem(
        id="item_1",
        source_type="shopping",
        query="Milton bottle",
        title="Milton Thermosteel 1000ml",
        seller_or_source="Amazon IN",
        url="https://amazon.in/1",
        snippet="Vacuum flask",
        price=899.0,
        currency="INR",
        product_id="milton_ts_1000",
        location_context="in",
        observed_at="2026-10-10T00:00:00Z",
        competitor="Milton"
    )
    # Duplicate with same product_id but missing price
    item2 = MarketItem(
        id="item_2",
        source_type="shopping",
        query="Milton bottle promo",
        title="Milton Thermosteel 1000ml Flask Silver",
        seller_or_source="Amazon IN",
        url="https://amazon.in/1?ref=promo",
        snippet="Vacuum flask on sale",
        price=None,
        currency="INR",
        product_id="milton_ts_1000",
        location_context="in",
        observed_at="2026-10-10T00:00:00Z",
        competitor="Milton"
    )

    unique, removed_count = deduplicate_items([item1, item2])
    assert len(unique) == 1
    assert removed_count == 1
    # Should retain the one with price
    assert unique[0].price == 899.0

def test_dedup_by_normalized_title_and_seller():
    item1 = MarketItem(
        id="item_a",
        source_type="shopping",
        query="Cello bottle",
        title="Cello Lifestyle Stainless Steel Water Bottle, 1000 ml",
        seller_or_source="Flipkart",
        url="https://flipkart.com/a",
        snippet="Single wall",
        price=600.0,
        currency="INR",
        product_id=None,
        location_context="in",
        observed_at="2026-10-10T00:00:00Z",
        competitor="Cello"
    )
    item2 = MarketItem(
        id="item_b",
        source_type="shopping",
        query="Cello bottle combo",
        title="Cello Lifestyle Stainless Steel Water Bottle 1000 ml",
        seller_or_source="Flipkart",
        url="https://flipkart.com/b",
        snippet="Single wall bottle",
        price=600.0,
        currency="INR",
        product_id=None,
        location_context="in",
        observed_at="2026-10-10T00:00:00Z",
        competitor="Cello"
    )

    unique, removed_count = deduplicate_items([item1, item2])
    assert len(unique) == 1
    assert removed_count == 1

def test_preserve_different_variants():
    # 500ml vs 1000ml must NOT be treated as duplicates!
    item_500 = MarketItem(
        id="item_500",
        source_type="shopping",
        query="Borosil bottle",
        title="Borosil Hydra Stainless Steel Bottle 500ml",
        seller_or_source="Amazon IN",
        url="https://amazon.in/500",
        snippet="500ml capacity",
        price=650.0,
        currency="INR",
        product_id="borosil_500",
        location_context="in",
        observed_at="2026-10-10T00:00:00Z",
        competitor="Borosil"
    )
    item_1000 = MarketItem(
        id="item_1000",
        source_type="shopping",
        query="Borosil bottle",
        title="Borosil Hydra Stainless Steel Bottle 1000ml",
        seller_or_source="Amazon IN",
        url="https://amazon.in/1000",
        snippet="1000ml capacity",
        price=895.0,
        currency="INR",
        product_id="borosil_1000",
        location_context="in",
        observed_at="2026-10-10T00:00:00Z",
        competitor="Borosil"
    )

    unique, removed_count = deduplicate_items([item_500, item_1000])
    assert len(unique) == 2
    assert removed_count == 0
