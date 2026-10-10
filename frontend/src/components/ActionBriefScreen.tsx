import React, { useState } from "react";
import { ActionBrief, MarketItem, Signal } from "../lib/types";
import {
  SparklesIcon,
  CheckCircleIcon,
  ShieldAlertIcon,
  ArrowRightIcon,
  CheckIcon,
  ExternalLinkIcon,
  InfoIcon,
} from "./Icons";

interface ActionBriefScreenProps {
  brief: ActionBrief | null;
  items: MarketItem[];
  signals: Signal[];
  businessCategory: string;
}

export function ActionBriefScreen({ brief, items, signals, businessCategory }: ActionBriefScreenProps) {
  // Map of verified checklist items toggled by the owner
  const [completedChecks, setCompletedChecks] = useState<Record<string, boolean>>({});

  const toggleCheck = (checkKey: string) => {
    setCompletedChecks((prev) => ({
      ...prev,
      [checkKey]: !prev[checkKey],
    }));
  };

  // Build lookup maps for evidence items
  const itemLookup = new Map<string, MarketItem>();
  items.forEach((it) => itemLookup.set(it.id, it));

  const signalLookup = new Map<string, Signal>();
  signals.forEach((s) => signalLookup.set(s.id, s));

  if (!brief || !brief.actions || brief.actions.length === 0) {
    return (
      <div className="glass-panel p-12 rounded-2xl text-center space-y-4">
        <div className="w-16 h-16 mx-auto rounded-full bg-slate-900 flex items-center justify-center border border-slate-800">
          <SparklesIcon className="w-8 h-8 text-indigo-400" />
        </div>
        <h3 className="text-lg font-semibold text-white">No Action Brief Available Yet</h3>
        <p className="text-sm text-slate-400 max-w-md mx-auto">
          Run a market scan to synthesize low-cost, evidence-backed next actions tailored to your niche.
        </p>
      </div>
    );
  }

  const getEffortBadge = (effort: string) => {
    switch (effort.toLowerCase()) {
      case "low":
        return "bg-emerald-950/80 text-emerald-300 border-emerald-800/80 badge-glow-emerald";
      case "medium":
        return "bg-amber-950/80 text-amber-300 border-amber-800/80 badge-glow-amber";
      case "high":
        return "bg-rose-950/80 text-rose-300 border-rose-800/80";
      default:
        return "bg-slate-800 text-slate-300 border-slate-700";
    }
  };

  const getConfidencePill = (conf: string) => {
    switch (conf.toLowerCase()) {
      case "high":
        return "text-emerald-400 font-semibold";
      case "medium":
        return "text-indigo-400 font-medium";
      case "low":
        return "text-slate-400 font-normal";
      default:
        return "text-slate-400";
    }
  };

  return (
    <div className="space-y-6">
      {/* Strategic Header & Governance Guardrail Banner */}
      <div className="p-5 rounded-2xl bg-gradient-to-r from-indigo-950/70 via-slate-900 to-slate-900 border border-indigo-900/40 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <span className="text-xs font-semibold px-2 py-0.5 rounded-full bg-indigo-900/80 text-indigo-300 border border-indigo-700/60">
              Executive Decision Brief
            </span>
            <span className="text-xs text-slate-400 font-mono">
              Engine: {brief.generated_by === "gemini" ? "Gemini 2.5 Flash" : "Deterministic Rule Engine"}
            </span>
          </div>
          <h2 className="text-lg font-bold text-white mt-1">
            Recommended Commercial Next Actions ({brief.actions.length})
          </h2>
          <p className="text-xs text-slate-400 mt-0.5">
            Low-overhead actions designed to counter observed competitor moves without degrading product margins.
          </p>
        </div>

        {/* Human in the loop reassurance tag */}
        <div className="flex items-center gap-2 bg-slate-950/60 px-3.5 py-2 rounded-xl border border-slate-800 text-xs self-stretch sm:self-auto">
          <ShieldAlertIcon className="w-4 h-4 text-emerald-400 flex-shrink-0" />
          <div className="text-slate-300 text-[11px] leading-tight">
            <span className="font-semibold text-emerald-400">Human Approval Only</span>
            <br />
            No automated repricing or inventory assumptions
          </div>
        </div>
      </div>

      {/* Action Cards */}
      <div className="space-y-6">
        {brief.actions.map((action, index) => (
          <div
            key={action.id || index}
            className="glass-panel p-6 rounded-2xl border border-slate-800 space-y-5 transition-all hover:border-indigo-500/30"
          >
            {/* Card Header: Numbering, Title, Effort & Confidence */}
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-3 border-b border-slate-800/80">
              <div className="flex items-start gap-3">
                <span className="flex items-center justify-center w-7 h-7 rounded-xl bg-indigo-900/60 text-indigo-300 font-bold text-xs border border-indigo-700/60 flex-shrink-0 mt-0.5">
                  #{index + 1}
                </span>
                <div>
                  <h3 className="text-base font-bold text-white tracking-tight">
                    {action.title}
                  </h3>
                </div>
              </div>

              <div className="flex items-center gap-2 self-start sm:self-auto">
                {/* Effort Badge */}
                <span
                  className={`px-2.5 py-1 rounded-lg text-xs font-semibold uppercase tracking-wider border ${getEffortBadge(
                    action.effort
                  )}`}
                >
                  {action.effort} Effort
                </span>

                {/* Confidence */}
                <span className="px-2.5 py-1 rounded-lg text-xs bg-slate-900 border border-slate-800 text-slate-300">
                  Confidence: <span className={getConfidencePill(action.confidence)}>{action.confidence}</span>
                </span>
              </div>
            </div>

            {/* Rationale Section */}
            <div className="space-y-1.5">
              <h4 className="text-xs font-semibold text-slate-400 uppercase tracking-wider">
                Why this matters (Decision Rationale)
              </h4>
              <p className="text-sm text-slate-200 leading-relaxed bg-slate-950/40 p-3.5 rounded-xl border border-slate-800/70">
                {action.rationale}
              </p>
            </div>

            {/* Verify Before Acting Checklist */}
            <div className="space-y-2">
              <h4 className="text-xs font-semibold text-slate-400 uppercase tracking-wider flex items-center gap-1.5">
                <CheckCircleIcon className="w-3.5 h-3.5 text-cyan-400" />
                <span>Verify Before Acting (Human Verification Checklist)</span>
              </h4>

              <div className="space-y-1.5 bg-slate-900/60 p-3.5 rounded-xl border border-slate-800">
                {action.verify_before_acting.map((check, cIdx) => {
                  const checkKey = `${action.id}_check_${cIdx}`;
                  const isChecked = !!completedChecks[checkKey];

                  return (
                    <label
                      key={cIdx}
                      className="flex items-start gap-2.5 cursor-pointer text-xs text-slate-300 hover:text-white select-none transition group"
                    >
                      <button
                        type="button"
                        onClick={() => toggleCheck(checkKey)}
                        className={`flex items-center justify-center w-4 h-4 rounded border mt-0.5 transition ${
                          isChecked
                            ? "bg-emerald-500 border-emerald-500 text-slate-950"
                            : "border-slate-600 bg-slate-800 group-hover:border-slate-500"
                        }`}
                      >
                        {isChecked && <CheckIcon className="w-3 h-3 stroke-[3]" />}
                      </button>
                      <span className={`leading-relaxed ${isChecked ? "line-through text-slate-500" : ""}`}>
                        {check}
                      </span>
                    </label>
                  );
                })}
              </div>
            </div>

            {/* Clickable Evidence Citations */}
            <div className="pt-2">
              <h4 className="text-[11px] font-semibold text-slate-500 uppercase tracking-wider mb-2 flex items-center gap-1.5">
                <InfoIcon className="w-3 h-3 text-indigo-400" />
                <span>Supporting Evidence Citations ({action.evidence_ids.length}):</span>
              </h4>

              <div className="flex flex-wrap gap-2">
                {action.evidence_ids.map((eid, eIdx) => {
                  const matchedItem = itemLookup.get(eid);
                  const matchedSignal = signalLookup.get(eid);

                  if (matchedItem) {
                    return (
                      <a
                        key={eid || eIdx}
                        href={matchedItem.url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-slate-900 hover:bg-slate-850 hover:border-cyan-500/50 border border-slate-800 text-xs text-slate-300 transition group"
                      >
                        <span className="w-1.5 h-1.5 rounded-full bg-cyan-400" />
                        <span className="font-semibold text-cyan-400 group-hover:underline">
                          {matchedItem.seller_or_source}
                        </span>
                        <span className="text-slate-400 max-w-xs truncate">
                          · {matchedItem.title}
                        </span>
                        <ExternalLinkIcon className="w-3 h-3 text-slate-500 group-hover:text-cyan-400 ml-1" />
                      </a>
                    );
                  }

                  if (matchedSignal) {
                    return (
                      <div
                        key={eid || eIdx}
                        className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-slate-900 border border-slate-800 text-xs text-slate-300"
                      >
                        <span className="w-1.5 h-1.5 rounded-full bg-indigo-400" />
                        <span className="font-medium text-indigo-300">
                          Signal [{matchedSignal.type}]
                        </span>
                        <span className="text-slate-400">· {matchedSignal.competitor}</span>
                      </div>
                    );
                  }

                  return (
                    <span
                      key={eid || eIdx}
                      className="inline-flex items-center gap-1 px-2.5 py-1 rounded-lg bg-slate-900 border border-slate-800 text-[11px] font-mono text-slate-400"
                    >
                      Evidence ID: {eid}
                    </span>
                  );
                })}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
