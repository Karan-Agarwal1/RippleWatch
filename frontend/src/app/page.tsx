"use client";

import React, { useState, useEffect } from "react";
import { Header } from "../components/Header";
import { SetupForm } from "../components/SetupForm";
import { RadarScreen } from "../components/RadarScreen";
import { ActionBriefScreen } from "../components/ActionBriefScreen";
import { HistoryScreen } from "../components/HistoryScreen";
import { ScanQualityPanel } from "../components/ScanQualityPanel";
import {
  Snapshot,
  SnapshotSummary,
  BusinessProfile,
  AppStatusResponse,
  Signal,
} from "../lib/types";
import {
  fetchSystemStatus,
  runScan,
  listSnapshots,
  getSnapshot,
  getCurrentBaseline,
  seedSampleBaseline,
  setBaseline,
  suggestCompetitors,
  submitSignalFeedback,
} from "../lib/api";
import {
  RadarIcon,
  SparklesIcon,
  HistoryIcon,
  CheckCircleIcon,
  InfoIcon,
  RefreshCwIcon,
} from "../components/Icons";

export default function Home() {
  const [activeView, setActiveView] = useState<string>("setup");
  const [profile, setProfile] = useState<BusinessProfile>({
    business_name: "EcoVessel India",
    category: "reusable steel water bottles",
    market: "India",
    gl: "in",
    hl: "en",
    competitors: ["Milton", "Cello", "Borosil"],
  });

  const [useCache, setUseCache] = useState<boolean>(true);
  const [status, setStatus] = useState<AppStatusResponse | null>(null);
  const [currentSnapshot, setCurrentSnapshot] = useState<Snapshot | null>(null);
  const [baselineSnapshot, setBaselineSnapshot] = useState<Snapshot | null>(null);
  const [snapshotsList, setSnapshotsList] = useState<SnapshotSummary[]>([]);

  const [isScanning, setIsScanning] = useState<boolean>(false);
  const [isSuggesting, setIsSuggesting] = useState<boolean>(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [successToast, setSuccessToast] = useState<string | null>(null);
  const [feedbackGiven, setFeedbackGiven] = useState<Record<string, boolean>>({});

  // Display toast helper
  const showToast = (msg: string) => {
    setSuccessToast(msg);
    setTimeout(() => setSuccessToast(null), 4000);
  };

  // Initial data loading
  useEffect(() => {
    async function init() {
      try {
        const sysStatus = await fetchSystemStatus();
        setStatus(sysStatus);

        const baseline = await getCurrentBaseline(profile.category, profile.market);
        setBaselineSnapshot(baseline);

        const list = await listSnapshots();
        setSnapshotsList(list);

        if (list.length > 0) {
          // If latest snapshot is not the baseline, load it as current
          const latestId = list[0].id;
          const fullSnap = await getSnapshot(latestId);
          setCurrentSnapshot(fullSnap);
          if (fullSnap.signals && fullSnap.signals.length > 0) {
            setActiveView("radar");
          }
        }
      } catch (err: any) {
        console.error("Initialization error:", err);
      }
    }
    init();
  }, []);

  // Run Market Scan
  const handleRunScan = async (isBaselineCreation: boolean = false) => {
    setIsScanning(true);
    setErrorMessage(null);

    try {
      const snap = await runScan(
        profile,
        useCache,
        baselineSnapshot?.id,
        isBaselineCreation
      );

      setCurrentSnapshot(snap);
      const updatedList = await listSnapshots();
      setSnapshotsList(updatedList);

      const sysStatus = await fetchSystemStatus();
      setStatus(sysStatus);

      if (isBaselineCreation) {
        setBaselineSnapshot(snap);
        showToast("Baseline snapshot successfully created from live market data.");
        setActiveView("history");
      } else {
        showToast(
          `Scan completed! Detected ${snap.signals.length} market changes across ${profile.competitors.length} competitors.`
        );
        setActiveView("radar");
      }
    } catch (err: any) {
      setErrorMessage(err.message || "Market scan execution failed");
    } finally {
      setIsScanning(false);
    }
  };

  // Suggest competitors via SerpApi
  const handleSuggestCompetitors = async () => {
    setIsSuggesting(true);
    setErrorMessage(null);
    try {
      const suggestions = await suggestCompetitors(profile.category, profile.market);
      if (suggestions && suggestions.length > 0) {
        const merged = Array.from(new Set([...profile.competitors, ...suggestions])).slice(0, 5);
        setProfile({ ...profile, competitors: merged });
        showToast(`Discovered top brands via SerpApi: ${suggestions.join(", ")}`);
      }
    } catch (err: any) {
      setErrorMessage("Could not retrieve competitor suggestions: " + err.message);
    } finally {
      setIsSuggesting(false);
    }
  };

  // Seed sample baseline for quick comparison demo
  const handleSeedSampleBaseline = async () => {
    try {
      const sample = await seedSampleBaseline();
      setBaselineSnapshot(sample);
      const updatedList = await listSnapshots();
      setSnapshotsList(updatedList);
      showToast("Sample 14-day baseline active. Run a live scan to view market changes.");
    } catch (err: any) {
      setErrorMessage("Failed to seed sample baseline: " + err.message);
    }
  };

  // Submit Useful / Irrelevant feedback
  const handleSignalFeedback = async (signal: Signal, isUseful: boolean) => {
    try {
      await submitSignalFeedback(
        signal.id,
        signal.competitor,
        signal.type,
        signal.evidence[0]?.title,
        isUseful
      );
      setFeedbackGiven((prev) => ({ ...prev, [signal.id]: isUseful }));
      showToast(
        isUseful
          ? "Signal marked Useful. Preserved for decision context."
          : "Signal marked Irrelevant. Suppressing similar patterns in future scans."
      );
    } catch (err: any) {
      setErrorMessage("Could not record feedback: " + err.message);
    }
  };

  // Select historical snapshot
  const handleSelectSnapshot = async (id: string) => {
    try {
      const full = await getSnapshot(id);
      setCurrentSnapshot(full);
    } catch (err: any) {
      setErrorMessage("Failed to load snapshot details: " + err.message);
    }
  };

  // Promote a past snapshot to active baseline
  const handleSetAsBaseline = async (id: string) => {
    try {
      await setBaseline(id);
      const updatedBaseline = await getCurrentBaseline(profile.category, profile.market);
      setBaselineSnapshot(updatedBaseline);
      const updatedList = await listSnapshots();
      setSnapshotsList(updatedList);
      showToast("Selected snapshot promoted to active baseline.");
    } catch (err: any) {
      setErrorMessage("Failed to set baseline: " + err.message);
    }
  };

  return (
    <div className="min-h-screen flex flex-col bg-[#090d16] text-slate-100">
      {/* App Header with navigation & live status */}
      <Header
        status={status}
        useCache={useCache}
        onToggleCache={setUseCache}
        activeView={activeView}
        onSelectView={setActiveView}
        onSeedSampleBaseline={handleSeedSampleBaseline}
        isLoading={isScanning}
      />

      {/* Main Container */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-6">
        {/* Global Toast Alert */}
        {successToast && (
          <div className="p-3.5 rounded-xl bg-emerald-950/90 border border-emerald-700/80 text-emerald-200 text-xs flex items-center justify-between gap-3 shadow-lg shadow-emerald-950/40 animate-fade-in">
            <div className="flex items-center gap-2">
              <CheckCircleIcon className="w-4 h-4 text-emerald-400 flex-shrink-0" />
              <span className="font-medium">{successToast}</span>
            </div>
            <button
              onClick={() => setSuccessToast(null)}
              className="text-emerald-400 hover:text-white"
            >
              ×
            </button>
          </div>
        )}

        {/* Global Error Banner */}
        {errorMessage && (
          <div className="p-4 rounded-xl bg-rose-950/80 border border-rose-800 text-rose-200 text-xs flex items-center justify-between gap-3">
            <div className="flex items-center gap-2">
              <span className="font-bold">Error:</span>
              <span>{errorMessage}</span>
            </div>
            <button
              onClick={() => setErrorMessage(null)}
              className="text-rose-400 hover:text-white font-bold"
            >
              Dismiss
            </button>
          </div>
        )}

        {/* Mobile View Navigation Pills */}
        <div className="flex md:hidden items-center justify-between bg-slate-900/90 p-1.5 rounded-xl border border-slate-800 text-xs overflow-x-auto">
          {[
            { id: "setup", label: "Setup" },
            { id: "radar", label: `Radar (${currentSnapshot?.signals.length || 0})` },
            { id: "brief", label: `Brief (${currentSnapshot?.brief?.actions.length || 0})` },
            { id: "history", label: "History" },
          ].map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveView(tab.id)}
              className={`px-3 py-1.5 rounded-lg font-medium whitespace-nowrap transition ${
                activeView === tab.id
                  ? "bg-indigo-600 text-white"
                  : "text-slate-400 hover:text-slate-200"
              }`}
            >
              {tab.label}
            </button>
          ))}
        </div>

        {/* Screen 1: Setup */}
        {activeView === "setup" && (
          <SetupForm
            profile={profile}
            onChangeProfile={setProfile}
            onRunScan={handleRunScan}
            onSuggestCompetitors={handleSuggestCompetitors}
            onLoadSampleBaseline={handleSeedSampleBaseline}
            isScanning={isScanning}
            isSuggesting={isSuggesting}
            hasActiveBaseline={!!baselineSnapshot}
            activeBaselineId={baselineSnapshot?.id || null}
          />
        )}

        {/* Screen 2: Radar */}
        {activeView === "radar" && (
          <div className="space-y-6">
            <RadarScreen
              signals={currentSnapshot?.signals || []}
              onFeedback={handleSignalFeedback}
              feedbackGiven={feedbackGiven}
            />

            {/* Quick Link to Action Brief */}
            {currentSnapshot?.brief && currentSnapshot.brief.actions.length > 0 && (
              <div className="p-4 rounded-2xl bg-indigo-950/40 border border-indigo-800/40 flex items-center justify-between">
                <div>
                  <h4 className="text-sm font-semibold text-white">
                    {currentSnapshot.brief.actions.length} Recommended Actions Available
                  </h4>
                  <p className="text-xs text-slate-400">
                    Review actionable, low-cost commercial responses backed by verified evidence.
                  </p>
                </div>
                <button
                  onClick={() => setActiveView("brief")}
                  className="px-4 py-2 rounded-xl text-xs font-semibold bg-indigo-600 hover:bg-indigo-500 text-white transition flex items-center gap-1.5"
                >
                  <span>View Action Brief</span>
                  <SparklesIcon className="w-3.5 h-3.5" />
                </button>
              </div>
            )}
          </div>
        )}

        {/* Screen 3: Action Brief */}
        {activeView === "brief" && (
          <ActionBriefScreen
            brief={currentSnapshot?.brief || null}
            items={currentSnapshot?.items || []}
            signals={currentSnapshot?.signals || []}
            businessCategory={profile.category}
          />
        )}

        {/* Screen 4: History */}
        {activeView === "history" && (
          <HistoryScreen
            currentSnapshot={currentSnapshot}
            baselineSnapshot={baselineSnapshot}
            snapshotsList={snapshotsList}
            onSelectSnapshot={handleSelectSnapshot}
            onSetAsBaseline={handleSetAsBaseline}
            isLoading={isScanning}
          />
        )}

        {/* Scan Quality Panel (Always Visible at bottom) */}
        {currentSnapshot?.quality_metrics && (
          <div className="pt-4">
            <ScanQualityPanel metrics={currentSnapshot.quality_metrics} />
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="border-t border-slate-900 bg-slate-950 py-6 text-center text-xs text-slate-500">
        <div className="max-w-7xl mx-auto px-4 flex flex-col sm:flex-row items-center justify-between gap-3">
          <div>
            RippleWatch · Built for the SerpApi Hackathon · Focus on Decision Intelligence
          </div>
          <div className="flex items-center gap-4 text-slate-400">
            <span>Google Shopping</span>
            <span>·</span>
            <span>Google News</span>
            <span>·</span>
            <span>Google Search</span>
          </div>
        </div>
      </footer>
    </div>
  );
}
