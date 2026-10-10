import {
  Snapshot,
  BusinessProfile,
  AppStatusResponse,
  SnapshotSummary,
  SignalType
} from "./types";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export async function fetchSystemStatus(): Promise<AppStatusResponse> {
  const res = await fetch(`${API_BASE}/api/status`);
  if (!res.ok) throw new Error("Failed to fetch system status");
  return res.json();
}

export async function runScan(
  businessProfile: BusinessProfile,
  useCache: boolean = true,
  compareWithSnapshotId?: string,
  isBaselineCreation: boolean = false
): Promise<Snapshot> {
  const res = await fetch(`${API_BASE}/api/scan`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      business_profile: businessProfile,
      use_cache: useCache,
      compare_with_snapshot_id: compareWithSnapshotId || null,
      is_baseline_creation: isBaselineCreation,
    }),
  });

  if (!res.ok) {
    const errorData = await res.json().catch(() => ({}));
    throw new Error(errorData.detail || "Market scan failed");
  }
  return res.json();
}

export async function listSnapshots(): Promise<SnapshotSummary[]> {
  const res = await fetch(`${API_BASE}/api/snapshots`);
  if (!res.ok) throw new Error("Failed to fetch snapshots list");
  return res.json();
}

export async function getSnapshot(id: string): Promise<Snapshot> {
  const res = await fetch(`${API_BASE}/api/snapshots/${id}`);
  if (!res.ok) throw new Error("Failed to fetch snapshot details");
  return res.json();
}

export async function getCurrentBaseline(category = "reusable steel water bottles", market = "India"): Promise<Snapshot | null> {
  const res = await fetch(`${API_BASE}/api/baseline/current?category=${encodeURIComponent(category)}&market=${encodeURIComponent(market)}`);
  if (!res.ok) return null;
  return res.json();
}

export async function seedSampleBaseline(): Promise<Snapshot> {
  const res = await fetch(`${API_BASE}/api/baseline/sample`, {
    method: "POST",
  });
  if (!res.ok) throw new Error("Failed to seed sample baseline");
  return res.json();
}

export async function setBaseline(snapshotId: string): Promise<void> {
  const res = await fetch(`${API_BASE}/api/baseline/set/${snapshotId}`, {
    method: "POST",
  });
  if (!res.ok) throw new Error("Failed to set baseline");
}

export async function suggestCompetitors(category: string, market = "India"): Promise<string[]> {
  const res = await fetch(`${API_BASE}/api/competitors/suggest`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ category, market }),
  });
  if (!res.ok) throw new Error("Failed to suggest competitors");
  const data = await res.json();
  return data.suggested_competitors || [];
}

export async function submitSignalFeedback(
  signalId: string,
  competitor: string,
  signalType: SignalType,
  itemTitle: string | undefined,
  isUseful: boolean
): Promise<void> {
  const res = await fetch(`${API_BASE}/api/signals/feedback`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      signal_id: signalId,
      competitor,
      signal_type: signalType,
      item_title: itemTitle,
      is_useful: isUseful,
    }),
  });
  if (!res.ok) throw new Error("Failed to submit feedback");
}
