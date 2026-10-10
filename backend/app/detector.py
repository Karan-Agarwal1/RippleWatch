import hashlib
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime, timezone

from app.models import (
    MarketItem, Signal, EvidenceItem, SignalType, SignalConfidence
)
from app.normalizer import normalize_title_for_comparison
from app.database import get_suppressed_patterns

PROMOTION_KEYWORDS = [
    "pack of 2", "pack of 3", "pack of 4", "bundle", "combo",
    "buy 1 get 1", "bogo", "% off", "percent off", "deal of the day",
    "limited time deal", "festive offer", "special offer", "flat 20%",
    "flat 30%", "flat 50%", "super saver"
]

def generate_signal_id(signal_type: str, competitor: str, key_token: str) -> str:
    raw = f"{signal_type}:{competitor}:{key_token}"
    return f"sig_{hashlib.sha256(raw.encode('utf-8')).hexdigest()[:12]}"

def extract_promotional_phrase(text: str) -> Optional[str]:
    t = text.lower()
    for kw in PROMOTION_KEYWORDS:
        if kw in t:
            return kw
    return None

def is_signal_suppressed(competitor: str, sig_type: str, text: str, suppressions: List[Dict[str, Any]]) -> bool:
    c_lower = competitor.lower()
    t_lower = text.lower()
    for supp in suppressions:
        if supp.get("competitor") == c_lower and supp.get("signal_type") == sig_type:
            item_kw = supp.get("item_title", "")
            if not item_kw or item_kw in t_lower:
                return True
    return False

def match_items(
    current_item: MarketItem,
    baseline_items: List[MarketItem]
) -> Optional[MarketItem]:
    """
    Finds the corresponding item in the baseline snapshot.
    Matches on product_id first, then normalized title + seller.
    """
    if current_item.product_id:
        for b_item in baseline_items:
            if b_item.product_id and b_item.product_id == current_item.product_id:
                return b_item

    cur_norm_title = normalize_title_for_comparison(current_item.title)
    cur_seller = current_item.seller_or_source.lower().strip()

    # Exact title + seller
    for b_item in baseline_items:
        if (normalize_title_for_comparison(b_item.title) == cur_norm_title and 
            b_item.seller_or_source.lower().strip() == cur_seller):
            return b_item

    # Close token overlap (> 85%) on same competitor
    cur_tokens = set(cur_norm_title.split())
    if len(cur_tokens) >= 3:
        for b_item in baseline_items:
            if b_item.competitor == current_item.competitor:
                b_tokens = set(normalize_title_for_comparison(b_item.title).split())
                overlap = len(cur_tokens & b_tokens) / max(len(cur_tokens), len(b_tokens))
                if overlap >= 0.85 and (cur_seller in b_item.seller_or_source.lower() or b_item.seller_or_source.lower() in cur_seller):
                    return b_item

    return None

class MarketChangeDetector:
    @staticmethod
    def detect_changes(
        current_items: List[MarketItem],
        baseline_items: List[MarketItem],
        tracked_competitors: List[str]
    ) -> List[Signal]:
        signals: List[Signal] = []
        suppressions = get_suppressed_patterns()
        now_utc = datetime.now(timezone.utc).isoformat()

        # Map baseline items for lookup
        baseline_item_ids = {b.id for b in baseline_items}
        baseline_news_titles = {normalize_title_for_comparison(b.title) for b in baseline_items if b.source_type == "news"}

        # Track products seen across multiple sellers for confidence boost
        competitor_title_counts: Dict[str, List[MarketItem]] = {}
        for item in current_items:
            key = f"{item.competitor}:{normalize_title_for_comparison(item.title)}"
            competitor_title_counts.setdefault(key, []).append(item)

        # 1. PRICE_CHANGE & PROMOTION & NEW_PRODUCT
        checked_matched_keys = set()

        for cur_item in current_items:
            competitor = cur_item.competitor or "Competitor"
            if tracked_competitors and competitor not in tracked_competitors:
                continue

            # Skip news items here (handled separately)
            if cur_item.source_type == "news":
                continue

            matched_baseline = match_items(cur_item, baseline_items)

            if matched_baseline:
                match_key = f"{cur_item.id}:{matched_baseline.id}"
                if match_key in checked_matched_keys:
                    continue
                checked_matched_keys.add(match_key)

                # Check PRICE_CHANGE
                if cur_item.price is not None and matched_baseline.price is not None and matched_baseline.price > 0:
                    old_p = matched_baseline.price
                    new_p = cur_item.price
                    diff_pct = (new_p - old_p) / old_p

                    if abs(diff_pct) >= 0.05:  # >= 5% change
                        direction = "dropped" if diff_pct < 0 else "increased"
                        pct_display = abs(diff_pct) * 100
                        what_changed = (
                            f"{competitor} '{cur_item.title}' {direction} by {pct_display:.1f}% "
                            f"(from ₹{old_p:,.0f} to ₹{new_p:,.0f}) on {cur_item.seller_or_source}."
                        )

                        if not is_signal_suppressed(competitor, "PRICE_CHANGE", cur_item.title, suppressions):
                            title_key = f"{cur_item.competitor}:{normalize_title_for_comparison(cur_item.title)}"
                            multi_seller_matches = competitor_title_counts.get(title_key, [])
                            confidence: SignalConfidence = "confirmed" if len(multi_seller_matches) >= 2 else "likely"

                            evidence = [
                                EvidenceItem(
                                    item_id=cur_item.id,
                                    title=f"Current: {cur_item.title}",
                                    url=cur_item.url,
                                    source_type=cur_item.source_type,
                                    seller_or_source=cur_item.seller_or_source,
                                    price=cur_item.price
                                ),
                                EvidenceItem(
                                    item_id=matched_baseline.id,
                                    title=f"Baseline: {matched_baseline.title}",
                                    url=matched_baseline.url,
                                    source_type=matched_baseline.source_type,
                                    seller_or_source=matched_baseline.seller_or_source,
                                    price=matched_baseline.price
                                )
                            ]

                            signals.append(Signal(
                                id=generate_signal_id("PRICE_CHANGE", competitor, f"{cur_item.title}_{new_p}"),
                                type="PRICE_CHANGE",
                                competitor=competitor,
                                what_changed=what_changed,
                                evidence=evidence,
                                observed_at=now_utc,
                                confidence=confidence,
                                limitations="Price may exclude shipping/delivery fees or bank card discounts; region and variant dependent."
                            ))

                # Check PROMOTION in matched item (newly added promo phrase)
                cur_promo = extract_promotional_phrase(f"{cur_item.title} {cur_item.snippet}")
                base_promo = extract_promotional_phrase(f"{matched_baseline.title} {matched_baseline.snippet}")

                if cur_promo and not base_promo:
                    what_changed = (
                        f"{competitor} introduced promotional campaign ('{cur_promo}') on '{cur_item.title}' "
                        f"priced at ₹{cur_item.price or 0:,.0f} on {cur_item.seller_or_source}."
                    )
                    if not is_signal_suppressed(competitor, "PROMOTION", cur_item.title, suppressions):
                        evidence = [
                            EvidenceItem(
                                item_id=cur_item.id,
                                title=cur_item.title,
                                url=cur_item.url,
                                source_type=cur_item.source_type,
                                seller_or_source=cur_item.seller_or_source,
                                price=cur_item.price
                            )
                        ]
                        signals.append(Signal(
                            id=generate_signal_id("PROMOTION", competitor, f"{cur_item.title}_{cur_promo}"),
                            type="PROMOTION",
                            competitor=competitor,
                            what_changed=what_changed,
                            evidence=evidence,
                            observed_at=now_utc,
                            confidence="likely",
                            limitations="Promotions are subject to stock availability and seller-specific terms."
                        ))

            else:
                # No match in baseline: Check if this is a NEW_PRODUCT or a standalone PROMOTION
                promo_phrase = extract_promotional_phrase(f"{cur_item.title} {cur_item.snippet}")
                
                if promo_phrase:
                    what_changed = (
                        f"{competitor} listed a new promotional bundle ('{promo_phrase}'): '{cur_item.title}' "
                        f"at ₹{cur_item.price or 0:,.0f} on {cur_item.seller_or_source}."
                    )
                    if not is_signal_suppressed(competitor, "PROMOTION", cur_item.title, suppressions):
                        evidence = [
                            EvidenceItem(
                                item_id=cur_item.id,
                                title=cur_item.title,
                                url=cur_item.url,
                                source_type=cur_item.source_type,
                                seller_or_source=cur_item.seller_or_source,
                                price=cur_item.price
                            )
                        ]
                        title_key = f"{cur_item.competitor}:{normalize_title_for_comparison(cur_item.title)}"
                        multi = competitor_title_counts.get(title_key, [])
                        conf: SignalConfidence = "confirmed" if len(multi) >= 2 else "likely"

                        signals.append(Signal(
                            id=generate_signal_id("PROMOTION", competitor, f"{cur_item.title}_{promo_phrase}"),
                            type="PROMOTION",
                            competitor=competitor,
                            what_changed=what_changed,
                            evidence=evidence,
                            observed_at=now_utc,
                            confidence=conf,
                            limitations="Bundle pricing and availability vary by retailer distribution."
                        ))
                else:
                    # NEW_PRODUCT
                    if cur_item.source_type == "shopping" and cur_item.price is not None:
                        what_changed = (
                            f"New product listing detected from {competitor}: '{cur_item.title}' "
                            f"at ₹{cur_item.price:,.0f} on {cur_item.seller_or_source}."
                        )
                        if not is_signal_suppressed(competitor, "NEW_PRODUCT", cur_item.title, suppressions):
                            evidence = [
                                EvidenceItem(
                                    item_id=cur_item.id,
                                    title=cur_item.title,
                                    url=cur_item.url,
                                    source_type=cur_item.source_type,
                                    seller_or_source=cur_item.seller_or_source,
                                    price=cur_item.price
                                )
                            ]
                            title_key = f"{cur_item.competitor}:{normalize_title_for_comparison(cur_item.title)}"
                            multi = competitor_title_counts.get(title_key, [])
                            conf: SignalConfidence = "confirmed" if len(multi) >= 2 else "likely"

                            signals.append(Signal(
                                id=generate_signal_id("NEW_PRODUCT", competitor, cur_item.title),
                                type="NEW_PRODUCT",
                                competitor=competitor,
                                what_changed=what_changed,
                                evidence=evidence,
                                observed_at=now_utc,
                                confidence=conf,
                                limitations="New SKU cataloging may be gradual; check seller authenticity."
                            ))

        # 2. NEWS: check articles
        for cur_item in current_items:
            if cur_item.source_type != "news":
                continue
            competitor = cur_item.competitor or "Competitor"
            if tracked_competitors and competitor not in tracked_competitors:
                continue

            norm_t = normalize_title_for_comparison(cur_item.title)
            if norm_t not in baseline_news_titles:
                what_changed = (
                    f"New industry media report concerning {competitor}: '{cur_item.title}' "
                    f"published by {cur_item.seller_or_source}."
                )
                if not is_signal_suppressed(competitor, "NEWS", cur_item.title, suppressions):
                    evidence = [
                        EvidenceItem(
                            item_id=cur_item.id,
                            title=cur_item.title,
                            url=cur_item.url,
                            source_type="news",
                            seller_or_source=cur_item.seller_or_source,
                            price=None
                        )
                    ]
                    signals.append(Signal(
                        id=generate_signal_id("NEWS", competitor, cur_item.title),
                        type="NEWS",
                        competitor=competitor,
                        what_changed=what_changed,
                        evidence=evidence,
                        observed_at=now_utc,
                        confidence="likely",
                        limitations="Media articles express editorial viewpoints; verify operational rollout independently."
                    ))

        # Deduplicate signals by signal ID
        unique_signals = []
        seen_sig_ids = set()
        for s in signals:
            if s.id not in seen_sig_ids:
                seen_sig_ids.add(s.id)
                unique_signals.append(s)

        # Rank signals: confirmed first, price change/promo first, limit to top high-impact signals (e.g. 5-8)
        confidence_rank = {"confirmed": 3, "likely": 2, "possible": 1}
        type_rank = {"PRICE_CHANGE": 4, "PROMOTION": 3, "NEW_PRODUCT": 2, "NEWS": 1}

        unique_signals.sort(
            key=lambda s: (confidence_rank.get(s.confidence, 0), type_rank.get(s.type, 0)),
            reverse=True
        )

        return unique_signals
