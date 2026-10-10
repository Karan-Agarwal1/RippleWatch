import re
import hashlib
from datetime import datetime, timezone
from typing import List, Dict, Any, Tuple, Optional
from app.models import MarketItem, SourceType

def parse_price_string(price_str: Optional[Any]) -> Tuple[Optional[float], Optional[str]]:
    """
    Parses a price string like '₹1,299', 'Rs. 950.00', '$24.99' or numeric into (price_float, currency).
    """
    if price_str is None:
        return None, "INR"

    if isinstance(price_str, (int, float)):
        return float(price_str), "INR"

    text = str(price_str).strip()
    currency = "INR"
    if "$" in text:
        currency = "USD"
    elif "€" in text:
        currency = "EUR"
    elif "£" in text:
        currency = "GBP"
    elif "₹" in text or "Rs" in text or "INR" in text:
        currency = "INR"

    # Remove currency prefixes like 'Rs.' or 'Rs' or 'INR' before numeric extraction
    cleaned = re.sub(r"(?i)\b(rs\.?|inr|usd|eur|gbp)\b", " ", text)
    # Remove commas
    cleaned = cleaned.replace(",", "")
    # Find decimal or integer number pattern
    match = re.search(r"(\d+(?:\.\d+)?)", cleaned)
    if match:
        try:
            return float(match.group(1)), currency
        except ValueError:
            pass

    return None, currency

def generate_item_id(source_type: str, product_id: Optional[str], url: str, title: str) -> str:
    """
    Generates a deterministic 16-character identifier.
    """
    unique_seed = product_id if product_id else (url if url and len(url) > 10 else f"{source_type}:{title}")
    raw = f"{source_type}:{unique_seed}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]

def normalize_title_for_comparison(title: str) -> str:
    """
    Normalizes a product title by lowercasing, stripping punctuation, and compressing whitespace.
    Retains volume/spec tokens (e.g. 500ml, 1l, 1000ml) to ensure variants are not treated as identical.
    """
    t = title.lower()
    t = re.sub(r"[^\w\s\d]", " ", t)
    t = re.sub(r"\s+", " ", t).strip()
    return t

def is_noise_item(title: str, snippet: str, category: str) -> bool:
    """
    Detects whether an item is noise (e.g. accessory, spare part, unrelated item).
    """
    t_lower = f"{title.lower()} {snippet.lower()}"
    cat_lower = category.lower()

    if not title or len(title.strip()) < 4:
        return True

    # If watching water bottles, filter out accessories and cleaning items
    if "bottle" in cat_lower or "flask" in cat_lower:
        accessory_keywords = [
            "bottle brush", "cleaning brush", "straw cleaner", "brush set",
            "silicone boot", "protective boot", "boot sleeve", "protective sleeve",
            "bottle cover", "bottle bag", "pouch for bottle", "bottle strap",
            "replacement lid", "replacement cap", "bottle cap only", "spare lid",
            "silicone gasket", "rubber gasket", "stickers", "water bottle stickers",
            "ice tray", "cleaning tablet"
        ]
        for kw in accessory_keywords:
            if kw in t_lower:
                return True

    # Generic noise indicators (broken titles, generic directory listings)
    unrelated_keywords = [
        "404 not found", "page not found", "access denied", "robot check"
    ]
    for uk in unrelated_keywords:
        if uk in t_lower:
            return True

    return False

class MarketItemNormalizer:
    @staticmethod
    def normalize_shopping_item(
        raw: Dict[str, Any],
        query: str,
        competitor: str,
        location: str = "in"
    ) -> Optional[MarketItem]:
        title = raw.get("title", "").strip()
        url = raw.get("link", raw.get("product_link", "")).strip()
        if not title:
            return None

        # Seller / Store
        seller = raw.get("source", raw.get("seller", "Google Shopping")).strip()

        # Product ID
        product_id = raw.get("product_id", raw.get("data_docid"))

        # Price
        extracted_price = raw.get("extracted_price")
        raw_price = raw.get("price")
        if extracted_price is not None:
            price = float(extracted_price)
            _, currency = parse_price_string(raw_price)
        else:
            price, currency = parse_price_string(raw_price)

        snippet = raw.get("snippet", raw.get("description", raw.get("delivery", "")))
        observed_at = datetime.now(timezone.utc).isoformat()
        item_id = generate_item_id("shopping", product_id, url, title)

        return MarketItem(
            id=item_id,
            source_type="shopping",
            query=query,
            title=title,
            seller_or_source=seller,
            url=url,
            snippet=snippet or "",
            price=price,
            currency=currency or "INR",
            product_id=product_id,
            location_context=location,
            observed_at=observed_at,
            competitor=competitor,
            raw_attributes={
                "rating": raw.get("rating"),
                "reviews": raw.get("reviews"),
                "badge": raw.get("badge")
            }
        )

    @staticmethod
    def normalize_news_item(
        raw: Dict[str, Any],
        query: str,
        competitor: str,
        location: str = "in"
    ) -> Optional[MarketItem]:
        title = raw.get("title", "").strip()
        url = raw.get("link", "").strip()
        if not title:
            return None

        # Source can be dict or str
        source_raw = raw.get("source")
        if isinstance(source_raw, dict):
            seller_or_source = source_raw.get("name", "Google News")
        else:
            seller_or_source = str(source_raw) if source_raw else "Google News"

        snippet = raw.get("snippet", raw.get("date", ""))
        observed_at = datetime.now(timezone.utc).isoformat()
        item_id = generate_item_id("news", None, url, title)

        return MarketItem(
            id=item_id,
            source_type="news",
            query=query,
            title=title,
            seller_or_source=seller_or_source,
            url=url,
            snippet=snippet or "",
            price=None,
            currency="INR",
            product_id=None,
            location_context=location,
            observed_at=observed_at,
            competitor=competitor,
            raw_attributes={
                "date": raw.get("date"),
                "thumbnail": raw.get("thumbnail")
            }
        )

    @staticmethod
    def normalize_search_item(
        raw: Dict[str, Any],
        query: str,
        competitor: str,
        location: str = "in"
    ) -> Optional[MarketItem]:
        title = raw.get("title", "").strip()
        url = raw.get("link", "").strip()
        if not title:
            return None

        seller_or_source = raw.get("displayed_link", "Organic Search")
        snippet = raw.get("snippet", "")
        price, currency = parse_price_string(raw.get("rich_snippet", {}).get("bottom", {}).get("price"))
        observed_at = datetime.now(timezone.utc).isoformat()
        item_id = generate_item_id("search", None, url, title)

        return MarketItem(
            id=item_id,
            source_type="search",
            query=query,
            title=title,
            seller_or_source=seller_or_source,
            url=url,
            snippet=snippet or "",
            price=price,
            currency=currency or "INR",
            product_id=None,
            location_context=location,
            observed_at=observed_at,
            competitor=competitor,
            raw_attributes={}
        )

def process_raw_serp_batch(
    raw_results_by_competitor: Dict[str, Dict[str, Any]],
    category: str,
    gl: str = "in"
) -> Tuple[List[MarketItem], int, int]:
    """
    Parses, cleans, filters noise, and deduplicates market items.
    Returns: (deduplicated_items, duplicates_removed_count, noise_filtered_count)
    """
    collected: List[MarketItem] = []
    noise_filtered_count = 0

    for competitor, sections in raw_results_by_competitor.items():
        for section_key, section_data in sections.items():
            if not section_data.get("success"):
                continue
            data = section_data.get("data", {})
            query = section_data.get("query", "")

            # 1. Shopping results
            for s_item in data.get("shopping_results", []):
                norm = MarketItemNormalizer.normalize_shopping_item(s_item, query, competitor, gl)
                if norm:
                    if is_noise_item(norm.title, norm.snippet, category):
                        noise_filtered_count += 1
                    else:
                        collected.append(norm)

            for s_item in data.get("inline_shopping_results", []):
                norm = MarketItemNormalizer.normalize_shopping_item(s_item, query, competitor, gl)
                if norm:
                    if is_noise_item(norm.title, norm.snippet, category):
                        noise_filtered_count += 1
                    else:
                        collected.append(norm)

            # 2. News results
            for n_item in data.get("news_results", []):
                norm = MarketItemNormalizer.normalize_news_item(n_item, query, competitor, gl)
                if norm:
                    if is_noise_item(norm.title, norm.snippet, category):
                        noise_filtered_count += 1
                    else:
                        collected.append(norm)

            # 3. Organic search results
            for o_item in data.get("organic_results", []):
                norm = MarketItemNormalizer.normalize_search_item(o_item, query, competitor, gl)
                if norm:
                    if is_noise_item(norm.title, norm.snippet, category):
                        noise_filtered_count += 1
                    else:
                        collected.append(norm)

    # Intelligent Deduplication
    deduped_items, duplicates_removed_count = deduplicate_items(collected)
    return deduped_items, duplicates_removed_count, noise_filtered_count

def deduplicate_items(items: List[MarketItem]) -> Tuple[List[MarketItem], int]:
    """
    Deduplicates items without collapsing variants:
    - Match on product_id first if present.
    - Otherwise match on (normalized_title + normalized_seller).
    - Preserves variants (500ml vs 1000ml) because normalize_title_for_comparison keeps alphanumeric specs.
    """
    by_product_id: Dict[str, MarketItem] = {}
    by_title_seller: Dict[str, MarketItem] = {}
    duplicates_count = 0

    unique_results: List[MarketItem] = []

    for item in items:
        # Check product_id first
        if item.product_id:
            pid_key = f"{item.source_type}:{item.product_id}"
            if pid_key in by_product_id:
                duplicates_count += 1
                # Keep the one with valid price if the existing didn't have one
                existing = by_product_id[pid_key]
                if existing.price is None and item.price is not None:
                    by_product_id[pid_key] = item
                continue
            else:
                by_product_id[pid_key] = item

        # Check title + seller match
        norm_title = normalize_title_for_comparison(item.title)
        norm_seller = item.seller_or_source.lower().strip()
        key = f"{item.source_type}:{item.competitor}:{norm_title}::{norm_seller}"

        if key in by_title_seller:
            duplicates_count += 1
            existing = by_title_seller[key]
            if existing.price is None and item.price is not None:
                by_title_seller[key] = item
            continue
        else:
            by_title_seller[key] = item

    # Combine unique items
    seen_ids = set()
    for item in by_title_seller.values():
        if item.id not in seen_ids:
            seen_ids.add(item.id)
            unique_results.append(item)

    return unique_results, duplicates_count
