import pytest
from app.models import Signal, EvidenceItem, MarketItem
from app.brief_generator import (
    validate_and_sanitize_actions, generate_deterministic_brief, extract_valid_ids
)

def test_validate_and_sanitize_drops_invalid_evidence_ids():
    valid_ids = {"sig_100", "item_200"}

    raw_actions = [
        {
            "id": "act_valid",
            "title": "Action With Valid Evidence",
            "rationale": "Directly linked to signal 100",
            "evidence_ids": ["sig_100", "item_nonexistent"],
            "effort": "low",
            "verify_before_acting": ["Check stock availability"],
            "confidence": "high"
        },
        {
            "id": "act_invalid",
            "title": "Action With Bogus Evidence",
            "rationale": "Hallucinated claim without evidence",
            "evidence_ids": ["item_fake_999"],
            "effort": "high",
            "verify_before_acting": ["Do something"],
            "confidence": "medium"
        }
    ]

    cleaned = validate_and_sanitize_actions(raw_actions, valid_ids)
    assert len(cleaned) == 1
    assert cleaned[0].title == "Action With Valid Evidence"
    # Bogus evidence id stripped, valid kept
    assert cleaned[0].evidence_ids == ["sig_100"]

def test_deterministic_brief_generation():
    signal = Signal(
        id="sig_test_price",
        type="PRICE_CHANGE",
        competitor="Milton",
        what_changed="Milton Thermosteel dropped by 18% from ₹990 to ₹810 on Amazon IN.",
        evidence=[
            EvidenceItem(
                item_id="item_ts_1",
                title="Milton Thermosteel 1000ml",
                url="https://amazon.in/1",
                source_type="shopping",
                seller_or_source="Amazon IN",
                price=810.0
            )
        ],
        observed_at="2026-10-10T00:00:00Z",
        confidence="likely",
        limitations="Price may exclude shipping"
    )

    items = [
        MarketItem(
            id="item_ts_1",
            source_type="shopping",
            query="Milton",
            title="Milton Thermosteel 1000ml",
            seller_or_source="Amazon IN",
            url="https://amazon.in/1",
            snippet="Vacuum flask",
            price=810.0,
            currency="INR",
            product_id="prod_ts",
            location_context="in",
            observed_at="2026-10-10T00:00:00Z",
            competitor="Milton"
        )
    ]

    brief = generate_deterministic_brief([signal], items)
    assert brief.generated_by == "rule_based"
    assert len(brief.actions) >= 1
    action = brief.actions[0]
    assert "Milton" in action.title or "Milton" in action.rationale
    assert signal.id in action.evidence_ids
    assert len(action.verify_before_acting) >= 2
    assert action.effort in ("low", "medium", "high")
