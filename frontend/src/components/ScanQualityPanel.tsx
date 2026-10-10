import React from "react";
import { ScanQualityMetrics } from "../lib/types";
import { ShieldAlertIcon, CheckCircleIcon, FilterIcon, InfoIcon } from "./Icons";

interface ScanQualityPanelProps {
  metrics: ScanQualityMetrics | null;
}

export function ScanQualityPanel({ metrics }: ScanQualityPanelProps) {
  if (!metrics) return null;

  return (
    <div className="glass-panel p-4 rounded-2xl border border-slate-800 text-xs">
      <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4">
        {/* Metric Badges Bar */}
        <div className="flex flex-wrap items-center gap-4">
          <div className="flex items-center gap-2">
            <span className="text-slate-500 font-medium">SerpApi Results:</span>
            <span className="px-2 py-0.5 rounded-md bg-slate-900 border border-slate-800 text-slate-200 font-mono font-semibold">
              {metrics.total_results_fetched} fetched
            </span>
          </div>

          <div className="flex items-center gap-2">
            <span className="text-slate-500 font-medium">Deduplicated:</span>
            <span className="px-2 py-0.5 rounded-md bg-slate-900 border border-slate-800 text-indigo-300 font-mono font-semibold">
              {metrics.duplicates_removed} duplicates merged
            </span>
          </div>

          <div className="flex items-center gap-2">
            <span className="text-slate-500 font-medium">Noise Filtered:</span>
            <span className="px-2 py-0.5 rounded-md bg-slate-900 border border-slate-800 text-cyan-300 font-mono font-semibold">
              {metrics.noise_filtered} accessories filtered
            </span>
          </div>

          <div className="flex items-center gap-2">
            <span className="text-slate-500 font-medium">Clickable Sources:</span>
            <span className="px-2 py-0.5 rounded-md bg-emerald-950/70 border border-emerald-800/60 text-emerald-300 font-mono font-semibold flex items-center gap-1">
              <CheckCircleIcon className="w-3 h-3 text-emerald-400" />
              {metrics.working_links_pct}% live URLs
            </span>
          </div>
        </div>

        {/* Prototype Transparency Note */}
        <div className="flex items-start gap-1.5 text-[11px] text-slate-400 lg:max-w-md bg-slate-950/60 px-3 py-2 rounded-xl border border-slate-800">
          <ShieldAlertIcon className="w-3.5 h-3.5 text-slate-400 flex-shrink-0 mt-0.5" />
          <span>{metrics.verification_disclaimer}</span>
        </div>
      </div>
    </div>
  );
}
