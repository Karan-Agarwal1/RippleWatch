import React, { useState } from "react";
import { BusinessProfile } from "../lib/types";
import { SparklesIcon, PlusIcon, XIcon, RadarIcon, RefreshCwIcon, CheckCircleIcon, InfoIcon } from "./Icons";

interface SetupFormProps {
  profile: BusinessProfile;
  onChangeProfile: (profile: BusinessProfile) => void;
  onRunScan: (isBaselineCreation: boolean) => void;
  onSuggestCompetitors: () => void;
  onLoadSampleBaseline: () => void;
  isScanning: boolean;
  isSuggesting: boolean;
  hasActiveBaseline: boolean;
  activeBaselineId: string | null;
}

export function SetupForm({
  profile,
  onChangeProfile,
  onRunScan,
  onSuggestCompetitors,
  onLoadSampleBaseline,
  isScanning,
  isSuggesting,
  hasActiveBaseline,
  activeBaselineId,
}: SetupFormProps) {
  const [newCompetitorInput, setNewCompetitorInput] = useState("");

  const handleAddCompetitor = () => {
    const trimmed = newCompetitorInput.trim();
    if (trimmed && !profile.competitors.includes(trimmed)) {
      if (profile.competitors.length >= 6) {
        alert("Maximum 5-6 competitors recommended to keep scans focused.");
        return;
      }
      onChangeProfile({
        ...profile,
        competitors: [...profile.competitors, trimmed],
      });
      setNewCompetitorInput("");
    }
  };

  const handleRemoveCompetitor = (name: string) => {
    if (profile.competitors.length <= 1) {
      alert("At least 1 competitor must be monitored.");
      return;
    }
    onChangeProfile({
      ...profile,
      competitors: profile.competitors.filter((c) => c !== name),
    });
  };

  return (
    <div className="space-y-6">
      {/* Top Banner: Niche Context */}
      <div className="p-4 rounded-2xl bg-gradient-to-r from-indigo-950/60 via-slate-900 to-slate-900 border border-indigo-900/40 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <span className="text-xs font-semibold px-2 py-0.5 rounded-full bg-cyan-950 text-cyan-400 border border-cyan-800/50">
              Target Demo Niche
            </span>
            <span className="text-xs text-slate-400">Market Context: India (gl=in, hl=en)</span>
          </div>
          <h2 className="text-base font-semibold text-white mt-1">
            Watching: {profile.category} in {profile.market}
          </h2>
          <p className="text-xs text-slate-400 mt-0.5">
            Targeting competitor catalogs, promotional bundles, and industry news via Google Shopping, News & Search.
          </p>
        </div>

        {/* Baseline status chip */}
        <div className="flex items-center gap-2 self-stretch sm:self-auto bg-slate-950/60 px-3 py-2 rounded-xl border border-slate-800 text-xs">
          <div className={`w-2 h-2 rounded-full ${hasActiveBaseline ? "bg-emerald-400" : "bg-amber-400 animate-ping"}`} />
          <div className="text-left">
            <div className="text-[10px] text-slate-400 uppercase font-semibold">Active Baseline</div>
            <div className="text-xs font-medium text-slate-200">
              {hasActiveBaseline ? (activeBaselineId?.includes("sample") ? "Sample Baseline (14d)" : "Custom Baseline") : "None Set"}
            </div>
          </div>
        </div>
      </div>

      {/* Main Setup Card */}
      <div className="glass-panel p-6 rounded-2xl space-y-6">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {/* Business Profile Name */}
          <div>
            <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2">
              Your Business / Brand
            </label>
            <input
              type="text"
              value={profile.business_name}
              onChange={(e) => onChangeProfile({ ...profile, business_name: e.target.value })}
              className="w-full px-3.5 py-2.5 rounded-xl bg-slate-900/90 border border-slate-700 text-sm text-white focus:outline-none focus:border-indigo-500 transition"
              placeholder="e.g. EcoVessel India"
            />
            <p className="text-[11px] text-slate-500 mt-1">Used to contextualize the decision brief.</p>
          </div>

          {/* Category */}
          <div>
            <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2">
              Product Category
            </label>
            <input
              type="text"
              value={profile.category}
              onChange={(e) => onChangeProfile({ ...profile, category: e.target.value })}
              className="w-full px-3.5 py-2.5 rounded-xl bg-slate-900/90 border border-slate-700 text-sm text-white focus:outline-none focus:border-indigo-500 transition"
              placeholder="e.g. reusable steel water bottles"
            />
            <p className="text-[11px] text-slate-500 mt-1">Used to filter noise and accessories.</p>
          </div>

          {/* Market / Region */}
          <div>
            <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2">
              Geography & Market
            </label>
            <div className="grid grid-cols-2 gap-2">
              <input
                type="text"
                value={profile.market}
                disabled
                className="w-full px-3.5 py-2.5 rounded-xl bg-slate-950/70 border border-slate-800 text-sm text-slate-400 cursor-not-allowed"
              />
              <div className="flex items-center px-3 py-2.5 rounded-xl bg-slate-950/70 border border-slate-800 text-xs text-cyan-400 font-mono">
                gl=in, hl=en
              </div>
            </div>
            <p className="text-[11px] text-slate-500 mt-1">Configured for Google India regional index.</p>
          </div>
        </div>

        {/* Competitor Brands Tracking Section */}
        <div className="pt-2 border-t border-slate-800/80">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 mb-3">
            <div>
              <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider">
                Tracked Competitor Brands ({profile.competitors.length} / 5)
              </label>
              <p className="text-xs text-slate-400">
                RippleWatch monitors these brands across Shopping SKUs, news articles, and promotional deals.
              </p>
            </div>

            <button
              type="button"
              onClick={onSuggestCompetitors}
              disabled={isSuggesting}
              className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium bg-slate-800 hover:bg-slate-700 text-indigo-300 border border-slate-700 transition"
            >
              <SparklesIcon className={`w-3.5 h-3.5 ${isSuggesting ? "animate-spin text-cyan-400" : "text-indigo-400"}`} />
              <span>{isSuggesting ? "Searching SerpApi..." : "Suggest Competitors"}</span>
            </button>
          </div>

          {/* Competitor Chips */}
          <div className="flex flex-wrap items-center gap-2 mb-4">
            {profile.competitors.map((comp) => (
              <div
                key={comp}
                className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-xl bg-indigo-950/50 border border-indigo-700/60 text-sm font-medium text-white shadow-sm"
              >
                <span className="w-1.5 h-1.5 rounded-full bg-cyan-400" />
                <span>{comp}</span>
                <button
                  type="button"
                  onClick={() => handleRemoveCompetitor(comp)}
                  className="text-slate-400 hover:text-rose-400 transition ml-1"
                  title="Remove competitor"
                >
                  <XIcon className="w-3.5 h-3.5" />
                </button>
              </div>
            ))}

            {/* Add Competitor Input */}
            <div className="inline-flex items-center gap-1">
              <input
                type="text"
                value={newCompetitorInput}
                onChange={(e) => setNewCompetitorInput(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === "Enter") {
                    e.preventDefault();
                    handleAddCompetitor();
                  }
                }}
                placeholder="+ Add brand name..."
                className="px-3 py-1.5 rounded-xl bg-slate-900 border border-slate-700 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500 w-36 sm:w-44"
              />
              <button
                type="button"
                onClick={handleAddCompetitor}
                className="p-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 transition"
                title="Add competitor"
              >
                <PlusIcon className="w-4 h-4" />
              </button>
            </div>
          </div>
        </div>

        {/* Scan Actions & Demo Controls */}
        <div className="pt-4 border-t border-slate-800/80 flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-4">
          <div className="flex items-center gap-2">
            <button
              type="button"
              onClick={onLoadSampleBaseline}
              disabled={isScanning}
              className="px-4 py-2.5 rounded-xl text-xs font-medium bg-slate-900 hover:bg-slate-800 text-slate-300 border border-slate-700/80 transition flex items-center justify-center gap-2"
              title="Loads realistic sample baseline dataset from 14 days ago"
            >
              <RefreshCwIcon className="w-4 h-4 text-slate-400" />
              <span>Load Sample Baseline</span>
            </button>

            <button
              type="button"
              onClick={() => onRunScan(true)}
              disabled={isScanning}
              className="px-4 py-2.5 rounded-xl text-xs font-medium bg-slate-900 hover:bg-slate-800 text-slate-300 border border-slate-700/80 transition flex items-center justify-center gap-2"
              title="Runs a live scan now and saves it as the new baseline snapshot"
            >
              <CheckCircleIcon className="w-4 h-4 text-emerald-400" />
              <span>Save Real Baseline</span>
            </button>
          </div>

          {/* Primary Run Scan Button */}
          <button
            type="button"
            onClick={() => onRunScan(false)}
            disabled={isScanning}
            className="px-6 py-3 rounded-xl font-semibold text-sm text-white bg-gradient-to-r from-indigo-600 via-indigo-500 to-cyan-500 hover:from-indigo-500 hover:to-cyan-400 shadow-lg shadow-indigo-500/25 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
          >
            <RadarIcon className={`w-5 h-5 ${isScanning ? "animate-spin text-white" : ""}`} />
            <span>{isScanning ? "Scanning SerpApi & Detecting Changes..." : "Run Market Scan"}</span>
          </button>
        </div>
      </div>
    </div>
  );
}
