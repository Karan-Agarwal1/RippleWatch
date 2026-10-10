import json
import re
from typing import List, Dict, Any, Optional, Set
from datetime import datetime, timezone

from app.config import settings
from app.models import (
    Signal, MarketItem, ActionItem, ActionBrief, ActionEffort, ActionConfidence
)

SYSTEM_PROMPT = """You are RippleWatch, an AI market-change intelligence agent advising a small business owner.
You are given strict, normalized market signals and verified clickable evidence from public market scans (Google Shopping, News, Search).

CRITICAL CONSTRAINTS:
1. ONLY utilize the provided signals and evidence items. Do NOT assume, fabricate, or hallucinate external facts.
2. STRICTLY FORBIDDEN: You must NEVER infer or claim competitor sales volume, revenues, market share, or inventory levels.
3. Every recommendation is for HUMAN APPROVAL ONLY. Never suggest automated or algorithmic price-setting.
4. Output 1 to 3 high-leverage, practical next actions. Keep effort low-to-medium where possible.
5. EVERY action MUST include 'evidence_ids', a JSON array referencing the EXACT 'id' of the signal or item provided. If an action does not directly cite at least one provided ID, it will be discarded.
6. Provide a 'verify_before_acting' list with 2-3 specific verification checks the owner should manually confirm before taking action.
7. Return strictly valid JSON matching this schema:
{
  "actions": [
    {
      "id": "act_1",
      "title": "Action title in imperative mood",
      "rationale": "Clear explanation of why this matters based on the cited evidence",
      "evidence_ids": ["sig_...", "..."],
      "effort": "low" | "medium" | "high",
      "verify_before_acting": ["Check 1", "Check 2"],
      "confidence": "high" | "medium" | "low"
    }
  ]
}
"""

def build_prompt_payload(signals: List[Signal], items: List[MarketItem], business_category: str) -> str:
    signals_data = []
    for s in signals:
        signals_data.append({
            "signal_id": s.id,
            "type": s.type,
            "competitor": s.competitor,
            "what_changed": s.what_changed,
            "confidence": s.confidence,
            "limitations": s.limitations,
            "evidence": [
                {
                    "item_id": ev.item_id,
                    "title": ev.title,
                    "url": ev.url,
                    "seller": ev.seller_or_source,
                    "price": ev.price
                }
                for ev in s.evidence
            ]
        })

    payload = {
        "category": business_category,
        "signals_count": len(signals),
        "signals": signals_data
    }
    return json.dumps(payload, indent=2)

def extract_valid_ids(signals: List[Signal], items: List[MarketItem]) -> Set[str]:
    valid_ids = set()
    for s in signals:
        valid_ids.add(s.id)
        for ev in s.evidence:
            valid_ids.add(ev.item_id)
    for it in items:
        valid_ids.add(it.id)
    return valid_ids

def validate_and_sanitize_actions(
    raw_actions: List[Dict[str, Any]],
    valid_ids: Set[str]
) -> List[ActionItem]:
    clean_actions: List[ActionItem] = []
    
    for idx, act in enumerate(raw_actions, start=1):
        raw_evidence = act.get("evidence_ids", [])
        if not isinstance(raw_evidence, list):
            continue

        # Keep ONLY evidence IDs that actually exist in the scan data
        sanitized_evidence = [eid for eid in raw_evidence if str(eid) in valid_ids]

        # REQUIREMENT: Drop any claim whose evidence_ids do not exist
        if not sanitized_evidence:
            continue

        raw_effort = str(act.get("effort", "low")).lower()
        effort: ActionEffort = raw_effort if raw_effort in ("low", "medium", "high") else "low"

        raw_conf = str(act.get("confidence", "medium")).lower()
        conf: ActionConfidence = raw_conf if raw_conf in ("high", "medium", "low") else "medium"

        raw_verify = act.get("verify_before_acting", [])
        verify_list = [str(v) for v in raw_verify if str(v).strip()] if isinstance(raw_verify, list) else []
        if not verify_list:
            verify_list = ["Verify competitor retailer listing terms and active stock status."]

        clean_actions.append(ActionItem(
            id=f"act_{idx}_{act.get('id', '')}"[:16],
            title=act.get("title", f"Action {idx}").strip(),
            rationale=act.get("rationale", "").strip(),
            evidence_ids=sanitized_evidence,
            effort=effort,
            verify_before_acting=verify_list,
            confidence=conf
        ))

    # Keep top 1 to 3 actions
    return clean_actions[:3]

def generate_deterministic_brief(signals: List[Signal], items: List[MarketItem]) -> ActionBrief:
    """
    Deterministic rule-based fallback brief generator.
    Guarantees reliable, evidence-backed actions when Gemini API key is missing or calls fail.
    """
    now_utc = datetime.now(timezone.utc).isoformat()
    actions: List[ActionItem] = []

    price_signals = [s for s in signals if s.type == "PRICE_CHANGE"]
    promo_signals = [s for s in signals if s.type == "PROMOTION"]
    product_signals = [s for s in signals if s.type == "NEW_PRODUCT"]
    news_signals = [s for s in signals if s.type == "NEWS"]

    action_idx = 1

    # 1. Action for Price Change
    if price_signals:
        sig = price_signals[0]
        ev_ids = [sig.id] + [ev.item_id for ev in sig.evidence]
        actions.append(ActionItem(
            id=f"act_{action_idx}_price_defense",
            title=f"Emphasize build quality and warranty over price matching against {sig.competitor}",
            rationale=(
                f"Evidence indicates {sig.what_changed} Rather than slashing margins to match prices, "
                f"reinforce value propositions like grade-304 food steel, zero-leak caps, and customer warranty on product pages."
            ),
            evidence_ids=ev_ids[:3],
            effort="low",
            verify_before_acting=[
                f"Check whether {sig.competitor}'s price cut is a temporary platform flash sale or a permanent MSRP reduction.",
                "Review current unit gross margin to establish a strict price floor before making any retail changes."
            ],
            confidence="high" if sig.confidence == "confirmed" else "medium"
        ))
        action_idx += 1

    # 2. Action for Promotion / Bundle
    if promo_signals:
        sig = promo_signals[0]
        ev_ids = [sig.id] + [ev.item_id for ev in sig.evidence]
        actions.append(ActionItem(
            id=f"act_{action_idx}_bundle_counter",
            title=f"Test a value-add 2-pack bundle to counter {sig.competitor}'s promotional packaging",
            rationale=(
                f"{sig.competitor} is leveraging bundle offers ({sig.what_changed}). "
                f"Offering a 2-bottle twin pack or bundling with cleaning accessories protects Average Order Value without discounting single units."
            ),
            evidence_ids=ev_ids[:3],
            effort="medium",
            verify_before_acting=[
                "Confirm packaging costs and box dimensions for twin-pack distribution.",
                "Verify stock balance of matching bottle capacities in current inventory."
            ],
            confidence="high" if sig.confidence == "confirmed" else "medium"
        ))
        action_idx += 1

    # 3. Action for New Product or News
    if len(actions) < 3 and (product_signals or news_signals):
        sig = product_signals[0] if product_signals else news_signals[0]
        ev_ids = [sig.id] + [ev.item_id for ev in sig.evidence]
        actions.append(ActionItem(
            id=f"act_{action_idx}_catalog_keyword_audit",
            title=f"Audit product title keywords and features against {sig.competitor}'s latest moves",
            rationale=(
                f"With {sig.competitor} shifting market attention ({sig.what_changed}), "
                f"ensure your listings emphasize key search criteria such as 'insulated', 'sweat-proof', and 'BPA-free' to capture customer search intent."
            ),
            evidence_ids=ev_ids[:3],
            effort="low",
            verify_before_acting=[
                "Review search term impression share in your Google Merchant Center or Amazon Ads dashboard.",
                "Verify that product specifications and capacity callouts are prominently displayed above the fold."
            ],
            confidence="medium"
        ))
        action_idx += 1

    # If no signals detected (quiet market)
    if not actions and items:
        top_item = items[0]
        actions.append(ActionItem(
            id="act_quiet_market_baseline",
            title="Maintain current positioning and monitor competitor promotional cycles",
            rationale="No drastic competitor price cuts or disruptive promotions were observed between snapshots. Stable market conditions suggest sticking to baseline pricing.",
            evidence_ids=[top_item.id],
            effort="low",
            verify_before_acting=[
                "Confirm that seller listings remain active and in-stock across primary channels.",
                "Schedule the next competitive scan ahead of seasonal retail events."
            ],
            confidence="high"
        ))

    return ActionBrief(
        actions=actions,
        generated_by="rule_based",
        timestamp=now_utc,
        notes="Generated via deterministic rule engine (evidence validated server-side)."
    )

class ActionBriefGenerator:
    @staticmethod
    async def generate_brief(
        signals: List[Signal],
        items: List[MarketItem],
        business_category: str
    ) -> ActionBrief:
        # If no signals or items, return a baseline action
        if not signals and not items:
            return ActionBrief(
                actions=[],
                generated_by="rule_based",
                timestamp=datetime.now(timezone.utc).isoformat(),
                notes="No market signals detected to analyze."
            )

        valid_ids = extract_valid_ids(signals, items)

        # Check if Gemini API Key is available
        api_key = settings.GEMINI_API_KEY.strip()
        if not api_key:
            return generate_deterministic_brief(signals, items)

        # Attempt LLM generation with google-genai SDK
        try:
            from google import genai
            from google.genai import types

            client = genai.Client(api_key=api_key)
            prompt_content = (
                f"{SYSTEM_PROMPT}\n\n"
                f"CURRENT MARKET SCAN DATA:\n"
                f"{build_prompt_payload(signals, items, business_category)}"
            )

            max_retries = 2
            last_error = ""

            for attempt in range(max_retries + 1):
                try:
                    response = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=prompt_content if attempt == 0 else f"{prompt_content}\n\nPREVIOUS ATTEMPT VALIDATION ERROR: {last_error}\nPlease fix and output strictly valid JSON matching the schema.",
                        config=types.GenerateContentConfig(
                            response_mime_type="application/json",
                            temperature=0.2
                        )
                    )

                    text = response.text or ""
                    # Clean possible markdown wrapping
                    text = re.sub(r"^```json\s*", "", text.strip())
                    text = re.sub(r"\s*```$", "", text.strip())

                    parsed = json.loads(text)
                    raw_actions = parsed.get("actions", [])
                    clean_actions = validate_and_sanitize_actions(raw_actions, valid_ids)

                    if clean_actions:
                        return ActionBrief(
                            actions=clean_actions,
                            generated_by="gemini",
                            timestamp=datetime.now(timezone.utc).isoformat(),
                            notes="AI brief synthesized using Gemini 2.5 Flash and verified against evidence records."
                        )
                    else:
                        last_error = "None of the generated actions had valid evidence_ids matching the scan data."
                except Exception as inner_err:
                    last_error = str(inner_err)

            # Fall back to deterministic brief if Gemini retries fail
            fallback = generate_deterministic_brief(signals, items)
            fallback.notes = f"Fell back to rule engine after LLM retry: {last_error}"
            return fallback

        except Exception as e:
            fallback = generate_deterministic_brief(signals, items)
            fallback.notes = f"Rule-based brief fallback triggered: {str(e)}"
            return fallback
