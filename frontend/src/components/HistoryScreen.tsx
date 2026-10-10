import React from "react";
import { Snapshot, SnapshotSummary } from "../lib/types";
import {
  HistoryIcon,
  CheckCircleIcon,
  ExternalLinkIcon,
  TrendingDownIcon,
  TrendingUpIcon,
  RefreshCwIcon,
} from "./Icons";

interface HistoryScreenProps {
  currentSnapshot: Snapshot | null;
  baselineSnapshot: Snapshot | null;
  snapshotsList: SnapshotSummary[];
  onSelectSnapshot: (id: string) => void;
  onSetAsBaseline: (id: string) => void;
  isLoading: boolean;
}

export function HistoryScreen({
  currentSnapshot,
  baselineSnapshot,
  snapshotsList,
  onSelectSnapshot,
  onSetAsBaseline,
  isLoading,
}: HistoryScreenProps) {
  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
        <div>
          <h2 className="text-xl font-bold text-white tracking-tight">Snapshot Comparison & History</h2>
          <p className="text-xs text-slate-400 mt-0.5">
            Compare your baseline market position side-by-side with the latest live scan.
          </p>
        </div>

        {/* Snapshots select dropdown */}
        <div className="flex items-center gap-2">
          <span className="text-xs text-slate-400">Past Scans:</span>
          <select
            onChange={(e) => onSelectSnapshot(e.target.value)}
            value={currentSnapshot?.id || ""}
            className="px-3 py-1.5 rounded-xl bg-slate-900 border border-slate-700 text-xs text-white focus:outline-none focus:border-indigo-500"
          >
            {snapshotsList.map((snap) => (
              <option key={snap.id} value={snap.id}>
                {new Date(snap.created_at).toLocaleDateString()} {new Date(snap.created_at).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}
                {snap.is_baseline ? " [Baseline]" : ""}
                {snap.is_sample ? " (Sample)" : ""}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Side-by-Side Comparison Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Left Column: Baseline Snapshot */}
        <div className="glass-panel p-5 rounded-2xl border border-slate-800 space-y-4">
          <div className="flex items-center justify-between pb-3 border-b border-slate-800">
            <div>
              <div className="flex items-center gap-2">
                <span className="text-xs font-semibold px-2 py-0.5 rounded-md bg-slate-800 text-slate-300">
                  {baselineSnapshot?.is_sample ? "Sample Baseline Data" : "Active Baseline Snapshot"}
                </span>
                <span className="text-xs text-emerald-400 font-medium">● Baseline</span>
              </div>
              <h3 className="text-sm font-bold text-white mt-1">
                {baselineSnapshot?.business_profile.category || "Baseline Market"}
              </h3>
              <p className="text-[11px] text-slate-500 font-mono">
                Captured: {baselineSnapshot ? new Date(baselineSnapshot.created_at).toLocaleString() : "None"}
              </p>
            </div>

            <div className="text-right">
              <span className="text-lg font-bold text-slate-200">
                {baselineSnapshot?.items.length || 0}
              </span>
              <p className="text-[11px] text-slate-500">catalog items</p>
            </div>
          </div>

          {/* Baseline Items Table */}
          <div className="space-y-2 max-h-[480px] overflow-y-auto pr-1">
            {baselineSnapshot?.items.map((item) => (
              <div
                key={item.id}
                className="p-3 rounded-xl bg-slate-950/40 border border-slate-800/80 flex items-center justify-between gap-3 text-xs"
              >
                <div className="min-w-0">
                  <div className="flex items-center gap-1.5 mb-0.5">
                    <span className="font-semibold text-slate-300">{item.competitor}</span>
                    <span className="text-slate-500">· {item.seller_or_source}</span>
                  </div>
                  <p className="text-slate-400 truncate">{item.title}</p>
                </div>

                <div className="text-right flex-shrink-0">
                  <span className="font-mono font-semibold text-slate-200">
                    {item.price !== null ? `₹${item.price.toLocaleString("en-IN")}` : "N/A"}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Right Column: Current Live Snapshot */}
        <div className="glass-panel p-5 rounded-2xl border border-indigo-900/40 space-y-4">
          <div className="flex items-center justify-between pb-3 border-b border-slate-800">
            <div>
              <div className="flex items-center gap-2">
                <span className="text-xs font-semibold px-2 py-0.5 rounded-md bg-indigo-950 text-indigo-300 border border-indigo-800/50">
                  Current Live Scan
                </span>
                <span className="text-xs text-cyan-400 font-medium">● Latest State</span>
              </div>
              <h3 className="text-sm font-bold text-white mt-1">
                {currentSnapshot?.business_profile.category || "Current Market"}
              </h3>
              <p className="text-[11px] text-slate-500 font-mono">
                Captured: {currentSnapshot ? new Date(currentSnapshot.created_at).toLocaleString() : "None"}
              </p>
            </div>

            <div className="text-right flex items-center gap-3">
              <div>
                <span className="text-lg font-bold text-white">
                  {currentSnapshot?.items.length || 0}
                </span>
                <p className="text-[11px] text-slate-500">catalog items</p>
              </div>

              {currentSnapshot && !currentSnapshot.is_baseline && (
                <button
                  type="button"
                  onClick={() => onSetAsBaseline(currentSnapshot.id)}
                  disabled={isLoading}
                  className="px-2.5 py-1 rounded-lg text-[11px] font-medium bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700 transition"
                  title="Make this snapshot the new active baseline"
                >
                  Promote to Baseline
                </button>
              )}
            </div>
          </div>

          {/* Current Items Table with Highlights */}
          <div className="space-y-2 max-h-[480px] overflow-y-auto pr-1">
            {currentSnapshot?.items.map((item) => {
              // Check if item has a matched signal
              const hasPriceChange = currentSnapshot.signals.find(
                (s) => s.type === "PRICE_CHANGE" && s.evidence.some((e) => e.item_id === item.id)
              );
              const isNewProduct = currentSnapshot.signals.find(
                (s) => s.type === "NEW_PRODUCT" && s.evidence.some((e) => e.item_id === item.id)
              );
              const isPromo = currentSnapshot.signals.find(
                (s) => s.type === "PROMOTION" && s.evidence.some((e) => e.item_id === item.id)
              );

              return (
                <div
                  key={item.id}
                  className={`p-3 rounded-xl border flex items-center justify-between gap-3 text-xs transition ${
                    hasPriceChange
                      ? "bg-amber-950/30 border-amber-800/60"
                      : isNewProduct
                      ? "bg-cyan-950/30 border-cyan-800/60"
                      : isPromo
                      ? "bg-purple-950/30 border-purple-800/60"
                      : "bg-slate-950/40 border-slate-800/80"
                  }`}
                >
                  <div className="min-w-0">
                    <div className="flex items-center gap-1.5 mb-0.5">
                      <span className="font-semibold text-white">{item.competitor}</span>
                      <span className="text-slate-400">· {item.seller_or_source}</span>
                      {hasPriceChange && (
                        <span className="text-[10px] px-1.5 py-0.2 rounded bg-amber-900/80 text-amber-300 font-semibold">
                          PRICE SHIFT
                        </span>
                      )}
                      {isNewProduct && (
                        <span className="text-[10px] px-1.5 py-0.2 rounded bg-cyan-900/80 text-cyan-300 font-semibold">
                          NEW SKU
                        </span>
                      )}
                      {isPromo && (
                        <span className="text-[10px] px-1.5 py-0.2 rounded bg-purple-900/80 text-purple-300 font-semibold">
                          PROMO
                        </span>
                      )}
                    </div>
                    <p className="text-slate-300 truncate">{item.title}</p>
                  </div>

                  <div className="text-right flex-shrink-0 flex items-center gap-2">
                    <span className="font-mono font-semibold text-white">
                      {item.price !== null ? `₹${item.price.toLocaleString("en-IN")}` : "N/A"}
                    </span>
                    <a
                      href={item.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-slate-500 hover:text-cyan-400 transition"
                      title="Open source listing"
                    >
                      <ExternalLinkIcon className="w-3.5 h-3.5" />
                    </a>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </div>
    </div>
  );
}
