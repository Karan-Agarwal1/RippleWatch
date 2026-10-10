import React from "react";
import { Signal, SignalType } from "../lib/types";
import {
  TrendingDownIcon,
  TagIcon,
  PackagePlusIcon,
  NewspaperIcon,
  CheckCircleIcon,
  ExternalLinkIcon,
  ThumbsUpIcon,
  ThumbsDownIcon,
  ShieldAlertIcon,
  InfoIcon,
} from "./Icons";

interface RadarScreenProps {
  signals: Signal[];
  onFeedback: (signal: Signal, isUseful: boolean) => void;
  feedbackGiven: Record<string, boolean>;
}

export function RadarScreen({ signals, onFeedback, feedbackGiven }: RadarScreenProps) {
  if (!signals || signals.length === 0) {
    return (
      <div className="glass-panel p-12 rounded-2xl text-center space-y-4">
        <div className="w-16 h-16 mx-auto rounded-full bg-slate-900 flex items-center justify-center border border-slate-800">
          <CheckCircleIcon className="w-8 h-8 text-emerald-400" />
        </div>
        <h3 className="text-lg font-semibold text-white">Market Stable — No Outlier Shifts Detected</h3>
        <p className="text-sm text-slate-400 max-w-md mx-auto">
          Compared to the active baseline, competitor pricing, bundles, and product catalogs are currently in equilibrium.
        </p>
      </div>
    );
  }

  const getSignalBadge = (type: SignalType) => {
    switch (type) {
      case "PRICE_CHANGE":
        return {
          label: "Price Change (≥5%)",
          color: "bg-amber-950/70 text-amber-300 border-amber-800/80 badge-glow-amber",
          icon: <TrendingDownIcon className="w-4 h-4 text-amber-400" />,
        };
      case "PROMOTION":
        return {
          label: "Promotion / Bundle",
          color: "bg-purple-950/70 text-purple-300 border-purple-800/80 badge-glow-purple",
          icon: <TagIcon className="w-4 h-4 text-purple-400" />,
        };
      case "NEW_PRODUCT":
        return {
          label: "New SKU Cataloged",
          color: "bg-cyan-950/70 text-cyan-300 border-cyan-800/80 badge-glow-cyan",
          icon: <PackagePlusIcon className="w-4 h-4 text-cyan-400" />,
        };
      case "NEWS":
        return {
          label: "Industry News / PR",
          color: "bg-blue-950/70 text-blue-300 border-blue-800/80",
          icon: <NewspaperIcon className="w-4 h-4 text-blue-400" />,
        };
      default:
        return {
          label: type,
          color: "bg-slate-800 text-slate-300 border-slate-700",
          icon: <InfoIcon className="w-4 h-4 text-slate-400" />,
        };
    }
  };

  const getConfidenceBadge = (confidence: string) => {
    switch (confidence) {
      case "confirmed":
        return (
          <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[11px] font-semibold bg-emerald-950/80 text-emerald-300 border border-emerald-800/60 badge-glow-emerald">
            <CheckCircleIcon className="w-3 h-3 text-emerald-400" />
            Confirmed (2+ Sources)
          </span>
        );
      case "likely":
        return (
          <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[11px] font-medium bg-blue-950/80 text-blue-300 border border-blue-800/60">
            Likely (Direct Listing)
          </span>
        );
      case "possible":
      default:
        return (
          <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[11px] font-medium bg-slate-900 text-slate-400 border border-slate-800">
            Possible (Single Mention)
          </span>
        );
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
        <div>
          <h2 className="text-xl font-bold text-white tracking-tight">Competitor Radar Signals</h2>
          <p className="text-xs text-slate-400 mt-0.5">
            Verified shifts detected between the current live market scan and your baseline snapshot.
          </p>
        </div>
        <div className="text-xs text-slate-400 bg-slate-900/80 px-3 py-1.5 rounded-xl border border-slate-800 font-mono">
          Showing top {signals.length} prioritized signals
        </div>
      </div>

      <div className="grid grid-cols-1 gap-4">
        {signals.map((signal) => {
          const badge = getSignalBadge(signal.type);
          const feedbackStatus = feedbackGiven[signal.id];

          return (
            <div
              key={signal.id}
              className="glass-panel glass-panel-hover p-5 rounded-2xl border border-slate-800 space-y-4"
            >
              {/* Card Header: Type Badge, Competitor, Confidence */}
              <div className="flex flex-wrap items-center justify-between gap-2">
                <div className="flex items-center gap-2">
                  <span
                    className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-xl text-xs font-semibold border ${badge.color}`}
                  >
                    {badge.icon}
                    <span>{badge.label}</span>
                  </span>

                  <span className="text-sm font-bold text-white px-2.5 py-0.5 rounded-lg bg-slate-900 border border-slate-800">
                    {signal.competitor}
                  </span>
                </div>

                <div className="flex items-center gap-2">
                  {getConfidenceBadge(signal.confidence)}
                  <span className="text-[11px] text-slate-500 font-mono">
                    {new Date(signal.observed_at).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}
                  </span>
                </div>
              </div>

              {/* What Changed description */}
              <div className="text-sm font-medium text-slate-100 leading-relaxed bg-slate-950/40 p-3.5 rounded-xl border border-slate-800/80">
                {signal.what_changed}
              </div>

              {/* Verified Clickable Evidence */}
              <div>
                <div className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider mb-2 flex items-center gap-1.5">
                  <InfoIcon className="w-3.5 h-3.5 text-cyan-400" />
                  <span>Clickable Source Evidence ({signal.evidence.length} item{signal.evidence.length > 1 ? "s" : ""}):</span>
                </div>

                <div className="flex flex-wrap gap-2">
                  {signal.evidence.map((ev, i) => (
                    <a
                      key={ev.item_id || i}
                      href={ev.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-slate-900/90 hover:bg-slate-850 hover:border-cyan-500/50 border border-slate-700/80 text-xs text-slate-200 transition group"
                    >
                      <span className="font-semibold text-cyan-400 group-hover:underline">
                        {ev.seller_or_source}
                      </span>
                      {ev.price !== null && (
                        <span className="text-slate-400 font-mono">· ₹{ev.price.toLocaleString("en-IN")}</span>
                      )}
                      <ExternalLinkIcon className="w-3 h-3 text-slate-500 group-hover:text-cyan-400" />
                    </a>
                  ))}
                </div>
              </div>

              {/* Footer: Limitations and Useful/Irrelevant Feedback Buttons */}
              <div className="pt-3 border-t border-slate-800/80 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                <div className="flex items-start gap-1.5 text-[11px] text-slate-500 max-w-xl">
                  <ShieldAlertIcon className="w-3.5 h-3.5 text-slate-500 flex-shrink-0 mt-0.5" />
                  <span>{signal.limitations}</span>
                </div>

                {/* Feedback Controls */}
                <div className="flex items-center gap-2 self-end sm:self-auto">
                  <span className="text-[11px] text-slate-500 hidden sm:inline">Signal Quality:</span>
                  <button
                    onClick={() => onFeedback(signal, true)}
                    className={`inline-flex items-center gap-1 px-2.5 py-1 rounded-lg text-xs font-medium border transition ${
                      feedbackStatus === true
                        ? "bg-emerald-950 text-emerald-300 border-emerald-700"
                        : "bg-slate-900 hover:bg-slate-800 text-slate-400 hover:text-slate-200 border-slate-800"
                    }`}
                    title="Mark this signal useful"
                  >
                    <ThumbsUpIcon className="w-3.5 h-3.5 text-emerald-400" />
                    <span>Useful</span>
                  </button>

                  <button
                    onClick={() => onFeedback(signal, false)}
                    className={`inline-flex items-center gap-1 px-2.5 py-1 rounded-lg text-xs font-medium border transition ${
                      feedbackStatus === false
                        ? "bg-rose-950 text-rose-300 border-rose-700"
                        : "bg-slate-900 hover:bg-slate-800 text-slate-400 hover:text-slate-200 border-slate-800"
                    }`}
                    title="Mark irrelevant to suppress similar false positives"
                  >
                    <ThumbsDownIcon className="w-3.5 h-3.5 text-rose-400" />
                    <span>Irrelevant</span>
                  </button>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
