from typing import List, Optional, Literal, Dict, Any
from pydantic import BaseModel, Field

SourceType = Literal["shopping", "news", "search"]
SignalType = Literal["NEW_PRODUCT", "PRICE_CHANGE", "PROMOTION", "NEWS"]
SignalConfidence = Literal["possible", "likely", "confirmed"]
ActionEffort = Literal["low", "medium", "high"]
ActionConfidence = Literal["high", "medium", "low"]

class MarketItem(BaseModel):
    id: str
    source_type: SourceType
    query: str
    title: str
    seller_or_source: str
    url: str
    snippet: str
    price: Optional[float] = None
    currency: Optional[str] = "INR"
    product_id: Optional[str] = None
    location_context: str = "in"
    observed_at: str
    competitor: Optional[str] = None
    raw_attributes: Dict[str, Any] = Field(default_factory=dict)

class EvidenceItem(BaseModel):
    item_id: str
    title: str
    url: str
    source_type: str
    seller_or_source: str
    price: Optional[float] = None

class Signal(BaseModel):
    id: str
    type: SignalType
    competitor: str
    what_changed: str
    evidence: List[EvidenceItem]
    observed_at: str
    confidence: SignalConfidence
    limitations: str
    is_useful: Optional[bool] = None

class ActionItem(BaseModel):
    id: str
    title: str
    rationale: str
    evidence_ids: List[str]
    effort: ActionEffort
    verify_before_acting: List[str]
    confidence: ActionConfidence

class ActionBrief(BaseModel):
    actions: List[ActionItem]
    generated_by: Literal["gemini", "rule_based"]
    timestamp: str
    notes: Optional[str] = None

class ScanQualityMetrics(BaseModel):
    total_results_fetched: int
    duplicates_removed: int
    noise_filtered: int
    working_links_pct: float
    verification_disclaimer: str

class BusinessProfile(BaseModel):
    business_name: str = "EcoVessel India"
    category: str = "reusable steel water bottles"
    market: str = "India"
    gl: str = "in"
    hl: str = "en"
    competitors: List[str] = Field(default_factory=lambda: ["Milton", "Cello", "Borosil"])

class Snapshot(BaseModel):
    id: str
    created_at: str
    business_profile: BusinessProfile
    items: List[MarketItem]
    signals: List[Signal]
    brief: Optional[ActionBrief] = None
    quality_metrics: ScanQualityMetrics
    is_baseline: bool = False
    is_sample: bool = False

# Request / Response Models
class ScanRequest(BaseModel):
    business_profile: BusinessProfile
    use_cache: bool = True
    compare_with_snapshot_id: Optional[str] = None
    is_baseline_creation: bool = False

class SuggestCompetitorsRequest(BaseModel):
    category: str = "reusable steel water bottles"
    market: str = "India"
    gl: str = "in"
    hl: str = "en"

class FeedbackRequest(BaseModel):
    signal_id: str
    competitor: str
    signal_type: SignalType
    item_title: Optional[str] = None
    is_useful: bool

class AppStatusResponse(BaseModel):
    status: str
    serpapi_configured: bool
    gemini_configured: bool
    cache_entries_count: int
    total_snapshots: int
    active_baseline_id: Optional[str]
