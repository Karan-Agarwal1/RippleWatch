import React from "react";
import { RadarIcon, SparklesIcon, RefreshCwIcon } from "./Icons";
import { AppStatusResponse } from "../lib/types";

interface HeaderProps {
  status: AppStatusResponse | null;
  useCache: boolean;
  onToggleCache: (value: boolean) => void;
  activeView: string;
  onSelectView: (view: string) => void;
  onSeedSampleBaseline: () => void;
  isLoading: boolean;
}

export function Header({
  status,
  useCache,
  onToggleCache,
  activeView,
  onSelectView,
  onSeedSampleBaseline,
  isLoading
}: HeaderProps) {
  return (
    <header className="border-b border-slate-800 bg-slate-950/80 backdrop-blur-md sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-20">
          {/* Logo & Brand Identity */}
          <div className="flex items-center gap-3">
            <div className="relative flex items-center justify-center w-11 h-11 rounded-xl bg-gradient-to-tr from-indigo-600 via-indigo-500 to-cyan-400 p-[1px] shadow-lg shadow-indigo-500/20">
              <div className="w-full h-full bg-slate-950 rounded-xl flex items-center justify-center">
                <RadarIcon className="w-6 h-6 text-cyan-400 animate-pulse" />
              </div>
              <span className="absolute -top-1 -right-1 flex h-3 w-3">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-cyan-400 opacity-75"></span>
                <span className="relative inline-flex rounded-full h-3 w-3 bg-cyan-500"></span>
              </span>
            </div>

            <div>
              <div className="flex items-center gap-2">
                <span className="text-xl font-bold tracking-tight text-white">
                  Ripple<span className="text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-indigo-400">Watch</span>
                </span>
                <span className="text-[10px] font-semibold uppercase tracking-wider px-2 py-0.5 rounded-full bg-indigo-950/80 text-indigo-300 border border-indigo-800/60">
                  SerpApi Hackathon MVP
                </span>
              </div>
              <p className="text-xs text-slate-400">
                AI Market-Change Agent for Small Businesses
              </p>
            </div>
          </div>

          {/* Navigation Tabs */}
          <nav className="hidden md:flex items-center space-x-1 bg-slate-900/80 p-1 rounded-xl border border-slate-800">
            {[
              { id: "setup", label: "Market Setup" },
              { id: "radar", label: "Signal Radar" },
              { id: "brief", label: "Action Brief" },
              { id: "history", label: "Snapshot History" },
            ].map((tab) => (
              <button
                key={tab.id}
                onClick={() => onSelectView(tab.id)}
                className={`px-3.5 py-1.5 rounded-lg text-xs font-medium transition-all ${
                  activeView === tab.id
                    ? "bg-indigo-600 text-white shadow-sm shadow-indigo-500/20"
                    : "text-slate-400 hover:text-slate-200 hover:bg-slate-800/60"
                }`}
              >
                {tab.label}
              </button>
            ))}
          </nav>

          {/* Status Indicators & Cache Toggle */}
          <div className="flex items-center gap-3">
            {/* Cache Toggle */}
            <div className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-slate-900 border border-slate-800 text-xs">
              <span className="text-slate-400 font-medium hidden sm:inline">Disk Cache:</span>
              <button
                onClick={() => onToggleCache(!useCache)}
                title="Cache raw SerpApi responses on disk with 24h TTL to conserve API quota"
                className={`relative inline-flex h-5 w-9 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none ${
                  useCache ? "bg-emerald-600" : "bg-slate-700"
                }`}
              >
                <span
                  className={`pointer-events-none inline-block h-4 w-4 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out ${
                    useCache ? "translate-x-4" : "translate-x-0"
                  }`}
                />
              </button>
              <span className={`text-[11px] font-semibold ${useCache ? "text-emerald-400" : "text-slate-400"}`}>
                {useCache ? "ON" : "OFF"}
              </span>
            </div>

            {/* SerpApi Status Pill */}
            <div className="hidden lg:flex items-center gap-1.5 px-2.5 py-1 rounded-md bg-slate-900/80 border border-slate-800 text-[11px]">
              <span className={`w-2 h-2 rounded-full ${status?.serpapi_configured ? "bg-emerald-400 shadow-sm shadow-emerald-400" : "bg-amber-400"}`} />
              <span className="text-slate-300">SerpApi:</span>
              <span className={`font-semibold ${status?.serpapi_configured ? "text-emerald-400" : "text-amber-400"}`}>
                {status?.serpapi_configured ? "Connected" : "Demo / Key Needed"}
              </span>
            </div>

            {/* Gemini LLM Status Pill */}
            <div className="hidden lg:flex items-center gap-1.5 px-2.5 py-1 rounded-md bg-slate-900/80 border border-slate-800 text-[11px]">
              <SparklesIcon className="w-3.5 h-3.5 text-indigo-400" />
              <span className="text-slate-300">Brief:</span>
              <span className="font-medium text-indigo-300">
                {status?.gemini_configured ? "Gemini 2.5" : "Rule Engine Fallback"}
              </span>
            </div>

            {/* Sample Baseline Quick Trigger */}
            <button
              onClick={onSeedSampleBaseline}
              disabled={isLoading}
              className="text-xs px-3 py-1.5 rounded-lg bg-indigo-950/70 hover:bg-indigo-900 text-indigo-300 border border-indigo-800/60 font-medium transition flex items-center gap-1.5"
              title="Seed 14-day old sample baseline data to immediately demonstrate change comparison"
            >
              <RefreshCwIcon className={`w-3.5 h-3.5 ${isLoading ? "animate-spin" : ""}`} />
              <span className="hidden sm:inline">Reset Baseline</span>
            </button>
          </div>
        </div>
      </div>
    </header>
  );
}
