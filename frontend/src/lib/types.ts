export type SourceType = "shopping" | "news" | "search";
export type SignalType = "NEW_PRODUCT" | "PRICE_CHANGE" | "PROMOTION" | "NEWS";
export type SignalConfidence = "possible" | "likely" | "confirmed";
export type ActionEffort = "low" | "medium" | "high";
export type ActionConfidence = "high" | "medium" | "low";

export interface MarketItem {
  id: string;
  source_type: SourceType;
  query: string;
  title: string;
  seller_or_source: string;
  url: string;
  snippet: string;
  price: number | null;
  currency: string;
  product_id: string | null;
  location_context: string;
  observed_at: string;
  competitor?: string;
  raw_attributes?: Record<string, any>;
}

export interface EvidenceItem {
  item_id: string;
  title: string;
  url: string;
  source_type: string;
  seller_or_source: string;
  price: number | null;
}

export interface Signal {
  id: string;
  type: SignalType;
  competitor: string;
  what_changed: string;
  evidence: EvidenceItem[];
  observed_at: string;
  confidence: SignalConfidence;
  limitations: string;
  is_useful?: boolean | null;
}

export interface ActionItem {
  id: string;
  title: string;
  rationale: string;
  evidence_ids: string[];
  effort: ActionEffort;
  verify_before_acting: string[];
  confidence: ActionConfidence;
}

export interface ActionBrief {
  actions: ActionItem[];
  generated_by: "gemini" | "rule_based";
  timestamp: string;
  notes?: string;
}

export interface ScanQualityMetrics {
  total_results_fetched: number;
  duplicates_removed: number;
  noise_filtered: number;
  working_links_pct: number;
  verification_disclaimer: string;
}

export interface BusinessProfile {
  business_name: string;
  category: string;
  market: string;
  gl: string;
  hl: string;
  competitors: string[];
}

export interface Snapshot {
  id: string;
  created_at: string;
  business_profile: BusinessProfile;
  items: MarketItem[];
  signals: Signal[];
  brief: ActionBrief | null;
  quality_metrics: ScanQualityMetrics;
  is_baseline: boolean;
  is_sample: boolean;
}

export interface AppStatusResponse {
  status: string;
  serpapi_configured: boolean;
  gemini_configured: boolean;
  cache_entries_count: number;
  total_snapshots: number;
  active_baseline_id: string | null;
}

export interface SnapshotSummary {
  id: string;
  created_at: string;
  business_name: string;
  category: string;
  market: string;
  is_baseline: boolean;
  is_sample: boolean;
}
