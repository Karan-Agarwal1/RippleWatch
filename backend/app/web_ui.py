def get_dashboard_html() -> str:
    return """<!DOCTYPE html>
<html lang="en" class="dark">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>RippleWatch | AI Market-Change Agent for Small Businesses</title>
  <meta name="description" content="AI market-change agent for small businesses. Watches the public market, detects meaningful competitor changes, and recommends evidence-backed commercial next actions." />
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {
      darkMode: 'class',
      theme: {
        extend: {
          fontFamily: {
            sans: ['"Plus Jakarta Sans"', 'sans-serif'],
            mono: ['"JetBrains Mono"', 'monospace'],
          },
          colors: {
            brand: {
              50: '#eef2ff',
              100: '#e0e7ff',
              200: '#c7d2fe',
              300: '#a5b4fc',
              400: '#818cf8',
              500: '#6366f1',
              600: '#4f46e5',
              700: '#4338ca',
              800: '#3730a3',
              900: '#312e81',
              950: '#1e1b4b',
            }
          }
        }
      }
    }
  </script>
  <style>
    body {
      background-color: #090d16;
      color: #f1f5f9;
      font-family: 'Plus Jakarta Sans', sans-serif;
    }
    .glass-panel {
      background: rgba(15, 23, 42, 0.72);
      backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
      border: 1px solid rgba(255, 255, 255, 0.08);
    }
    .glass-card:hover {
      background: rgba(26, 36, 61, 0.85);
      border-color: rgba(99, 102, 241, 0.35);
      transform: translateY(-2px);
      box-shadow: 0 12px 30px -10px rgba(0, 0, 0, 0.5), 0 0 20px -5px rgba(99, 102, 241, 0.15);
    }
    .badge-glow-cyan {
      box-shadow: 0 0 15px -2px rgba(6, 182, 212, 0.4);
    }
    .badge-glow-amber {
      box-shadow: 0 0 15px -2px rgba(245, 158, 11, 0.4);
    }
    .badge-glow-emerald {
      box-shadow: 0 0 15px -2px rgba(16 declared, 185, 129, 0.4);
    }
  </style>
</head>
<body class="min-h-screen flex flex-col bg-[#090d16] text-slate-100 antialiased selection:bg-indigo-500 selection:text-white">

  <!-- Header -->
  <header class="border-b border-slate-800 bg-slate-950/80 backdrop-blur-md sticky top-0 z-50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex items-center justify-between h-20">
        
        <!-- Brand -->
        <div class="flex items-center gap-3">
          <div class="relative flex items-center justify-center w-11 h-11 rounded-xl bg-gradient-to-tr from-indigo-600 via-indigo-500 to-cyan-400 p-[1px] shadow-lg shadow-indigo-500/20">
            <div class="w-full h-full bg-slate-950 rounded-xl flex items-center justify-center">
              <svg class="w-6 h-6 text-cyan-400 animate-pulse" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="9" /><circle cx="12" cy="12" r="6" /><circle cx="12" cy="12" r="3" />
                <path d="M12 3v9l4 4" />
              </svg>
            </div>
            <span class="absolute -top-1 -right-1 flex h-3 w-3">
              <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-cyan-400 opacity-75"></span>
              <span class="relative inline-flex rounded-full h-3 w-3 bg-cyan-500"></span>
            </span>
          </div>

          <div>
            <div class="flex items-center gap-2">
              <span class="text-xl font-bold tracking-tight text-white">
                Ripple<span class="text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-indigo-400">Watch</span>
              </span>
              <span class="text-[10px] font-semibold uppercase tracking-wider px-2 py-0.5 rounded-full bg-indigo-950/80 text-indigo-300 border border-indigo-800/60">
                SerpApi Hackathon MVP
              </span>
            </div>
            <p class="text-xs text-slate-400">
              AI Market-Change Agent for Small Businesses
            </p>
          </div>
        </div>

        <!-- Navigation Tabs -->
        <nav class="hidden md:flex items-center space-x-1 bg-slate-900/80 p-1 rounded-xl border border-slate-800">
          <button onclick="switchView('setup')" id="tab-setup" class="px-3.5 py-1.5 rounded-lg text-xs font-medium transition-all bg-indigo-600 text-white shadow-sm shadow-indigo-500/20">
            Market Setup
          </button>
          <button onclick="switchView('radar')" id="tab-radar" class="px-3.5 py-1.5 rounded-lg text-xs font-medium text-slate-400 hover:text-slate-200 hover:bg-slate-800/60 transition-all">
            Signal Radar
          </button>
          <button onclick="switchView('brief')" id="tab-brief" class="px-3.5 py-1.5 rounded-lg text-xs font-medium text-slate-400 hover:text-slate-200 hover:bg-slate-800/60 transition-all">
            Action Brief
          </button>
          <button onclick="switchView('history')" id="tab-history" class="px-3.5 py-1.5 rounded-lg text-xs font-medium text-slate-400 hover:text-slate-200 hover:bg-slate-800/60 transition-all">
            Snapshot History
          </button>
        </nav>

        <!-- Status & Controls -->
        <div class="flex items-center gap-3">
          <!-- Cache Toggle -->
          <div class="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-slate-900 border border-slate-800 text-xs">
            <span class="text-slate-400 font-medium hidden sm:inline">Disk Cache:</span>
            <button onclick="toggleCache()" id="cache-toggle-btn" class="relative inline-flex h-5 w-9 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out bg-emerald-600">
              <span id="cache-toggle-ball" class="pointer-events-none inline-block h-4 w-4 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out translate-x-4"></span>
            </button>
            <span id="cache-toggle-label" class="text-[11px] font-semibold text-emerald-400">ON</span>
          </div>

          <!-- SerpApi Connected Pill -->
          <div class="hidden lg:flex items-center gap-1.5 px-2.5 py-1 rounded-md bg-slate-900/80 border border-slate-800 text-[11px]">
            <span class="w-2 h-2 rounded-full bg-emerald-400 shadow-sm shadow-emerald-400"></span>
            <span class="text-slate-300">SerpApi:</span>
            <span class="font-semibold text-emerald-400">Connected</span>
          </div>

          <!-- Reset Sample Baseline -->
          <button onclick="seedSampleBaseline()" id="reset-baseline-btn" class="text-xs px-3 py-1.5 rounded-lg bg-indigo-950/70 hover:bg-indigo-900 text-indigo-300 border border-indigo-800/60 font-medium transition flex items-center gap-1.5">
            <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M3 12a9 9 0 0 1 15-6.7L21 8" /><path d="M21 3v5h-5" /><path d="M21 12a9 9 0 0 1-15 6.7L3 16" /><path d="M3 21v-5h5" />
            </svg>
            <span class="hidden sm:inline">Reset Baseline</span>
          </button>
        </div>

      </div>
    </div>
  </header>

  <!-- Main Content Container -->
  <main class="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-6">

    <!-- Global Toast Alert -->
    <div id="toast-banner" class="hidden p-3.5 rounded-xl bg-emerald-950/90 border border-emerald-700/80 text-emerald-200 text-xs flex items-center justify-between gap-3 shadow-lg shadow-emerald-950/40">
      <div class="flex items-center gap-2">
        <svg class="w-4 h-4 text-emerald-400 flex-shrink-0" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14" /><polyline points="22 4 12 14.01 9 11.01" /></svg>
        <span id="toast-message" class="font-medium"></span>
      </div>
      <button onclick="hideToast()" class="text-emerald-400 hover:text-white font-bold">×</button>
    </div>

    <!-- Error Banner -->
    <div id="error-banner" class="hidden p-4 rounded-xl bg-rose-950/80 border border-rose-800 text-rose-200 text-xs flex items-center justify-between gap-3">
      <div class="flex items-center gap-2">
        <span class="font-bold">Error:</span>
        <span id="error-message"></span>
      </div>
      <button onclick="hideError()" class="text-rose-400 hover:text-white font-bold">Dismiss</button>
    </div>

    <!-- Mobile View Switcher -->
    <div class="flex md:hidden items-center justify-between bg-slate-900/90 p-1.5 rounded-xl border border-slate-800 text-xs overflow-x-auto">
      <button onclick="switchView('setup')" id="m-tab-setup" class="px-3 py-1.5 rounded-lg font-medium bg-indigo-600 text-white">Setup</button>
      <button onclick="switchView('radar')" id="m-tab-radar" class="px-3 py-1.5 rounded-lg font-medium text-slate-400">Radar</button>
      <button onclick="switchView('brief')" id="m-tab-brief" class="px-3 py-1.5 rounded-lg font-medium text-slate-400">Brief</button>
      <button onclick="switchView('history')" id="m-tab-history" class="px-3 py-1.5 rounded-lg font-medium text-slate-400">History</button>
    </div>

    <!-- VIEW 1: SETUP SCREEN -->
    <div id="view-setup" class="space-y-6">
      <!-- Niche Banner -->
      <div class="p-4 rounded-2xl bg-gradient-to-r from-indigo-950/60 via-slate-900 to-slate-900 border border-indigo-900/40 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <div class="flex items-center gap-2">
            <span class="text-xs font-semibold px-2 py-0.5 rounded-full bg-cyan-950 text-cyan-400 border border-cyan-800/50">Target Demo Niche</span>
            <span class="text-xs text-slate-400">Market Context: India (gl=in, hl=en)</span>
          </div>
          <h2 class="text-base font-semibold text-white mt-1">
            Watching: <span id="display-category">reusable steel water bottles</span> in India
          </h2>
          <p class="text-xs text-slate-400 mt-0.5">
            Ingests catalog items, promotional bundles, and industry news via Google Shopping, News & Search.
          </p>
        </div>
        <div class="flex items-center gap-2 self-stretch sm:self-auto bg-slate-950/60 px-3 py-2 rounded-xl border border-slate-800 text-xs">
          <div class="w-2 h-2 rounded-full bg-emerald-400"></div>
          <div class="text-left">
            <div class="text-[10px] text-slate-400 uppercase font-semibold">Active Baseline</div>
            <div id="baseline-status-label" class="text-xs font-medium text-slate-200">Sample Baseline (14d)</div>
          </div>
        </div>
      </div>

      <!-- Main Form Card -->
      <div class="glass-panel p-6 rounded-2xl space-y-6">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div>
            <label class="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2">Your Business Name</label>
            <input type="text" id="input-biz-name" value="EcoVessel India" class="w-full px-3.5 py-2.5 rounded-xl bg-slate-900/90 border border-slate-700 text-sm text-white focus:outline-none focus:border-indigo-500 transition" />
            <p class="text-[11px] text-slate-500 mt-1">Contextualizes the decision brief.</p>
          </div>
          <div>
            <label class="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2">Product Category</label>
            <input type="text" id="input-category" value="reusable steel water bottles" class="w-full px-3.5 py-2.5 rounded-xl bg-slate-900/90 border border-slate-700 text-sm text-white focus:outline-none focus:border-indigo-500 transition" />
            <p class="text-[11px] text-slate-500 mt-1">Used to filter accessories and noise.</p>
          </div>
          <div>
            <label class="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2">Market & Location</label>
            <div class="grid grid-cols-2 gap-2">
              <input type="text" value="India" disabled class="w-full px-3.5 py-2.5 rounded-xl bg-slate-950/70 border border-slate-800 text-sm text-slate-400 cursor-not-allowed" />
              <div class="flex items-center px-3 py-2.5 rounded-xl bg-slate-950/70 border border-slate-800 text-xs text-cyan-400 font-mono">gl=in, hl=en</div>
            </div>
            <p class="text-[11px] text-slate-500 mt-1">Google India regional index.</p>
          </div>
        </div>

        <!-- Competitors Tracking -->
        <div class="pt-2 border-t border-slate-800/80">
          <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 mb-3">
            <div>
              <label class="block text-xs font-semibold text-slate-300 uppercase tracking-wider">
                Tracked Competitor Brands (<span id="comp-count">3</span> / 5)
              </label>
              <p class="text-xs text-slate-400">RippleWatch scans these brands across Shopping, News, and Search.</p>
            </div>
            <button onclick="suggestCompetitors()" id="suggest-btn" class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium bg-slate-800 hover:bg-slate-700 text-indigo-300 border border-slate-700 transition">
              <svg class="w-3.5 h-3.5 text-indigo-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 3l1.9 5.8a2 2 0 0 0 1.3 1.3L21 12l-5.8 1.9a2 2 0 0 0 -1.3 1.3L12 21l-1.9 -5.8a2 2 0 0 0 -1.3 -1.3L3 12l5.8 -1.9a2 2 0 0 0 1.3 -1.3L12 3z" /></svg>
              <span id="suggest-btn-text">Suggest Competitors</span>
            </button>
          </div>

          <!-- Competitor Chips -->
          <div id="competitors-container" class="flex flex-wrap items-center gap-2 mb-4">
            <!-- Chips rendered by JS -->
          </div>
        </div>

        <!-- Actions -->
        <div class="pt-4 border-t border-slate-800/80 flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-4">
          <div class="flex items-center gap-2">
            <button onclick="seedSampleBaseline()" class="px-4 py-2.5 rounded-xl text-xs font-medium bg-slate-900 hover:bg-slate-800 text-slate-300 border border-slate-700/80 transition flex items-center justify-center gap-2">
              <svg class="w-4 h-4 text-slate-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 12a9 9 0 0 1 15-6.7L21 8" /><path d="M21 3v5h-5" /><path d="M21 12a9 9 0 0 1-15 6.7L3 16" /><path d="M3 21v-5h5" /></svg>
              <span>Load Sample Baseline</span>
            </button>
            <button onclick="runScan(true)" class="px-4 py-2.5 rounded-xl text-xs font-medium bg-slate-900 hover:bg-slate-800 text-slate-300 border border-slate-700/80 transition flex items-center justify-center gap-2">
              <svg class="w-4 h-4 text-emerald-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14" /><polyline points="22 4 12 14.01 9 11.01" /></svg>
              <span>Save Real Baseline</span>
            </button>
          </div>

          <button onclick="runScan(false)" id="scan-btn" class="px-6 py-3 rounded-xl font-semibold text-sm text-white bg-gradient-to-r from-indigo-600 via-indigo-500 to-cyan-500 hover:from-indigo-500 hover:to-cyan-400 shadow-lg shadow-indigo-500/25 transition-all flex items-center justify-center gap-2">
            <svg id="scan-spinner" class="w-5 h-5 text-white" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="9" /><circle cx="12" cy="12" r="6" /><circle cx="12" cy="12" r="3" />
            </svg>
            <span id="scan-btn-text">Run Market Scan</span>
          </button>
        </div>
      </div>
    </div>

    <!-- VIEW 2: RADAR SCREEN -->
    <div id="view-radar" class="hidden space-y-6">
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
        <div>
          <h2 class="text-xl font-bold text-white tracking-tight">Competitor Radar Signals</h2>
          <p class="text-xs text-slate-400 mt-0.5">Verified shifts detected between current live scan and baseline snapshot.</p>
        </div>
        <div id="radar-count-badge" class="text-xs text-slate-400 bg-slate-900/80 px-3 py-1.5 rounded-xl border border-slate-800 font-mono">
          0 signals
        </div>
      </div>

      <!-- Signals Container -->
      <div id="signals-container" class="grid grid-cols-1 gap-4">
        <!-- Rendered by JS -->
      </div>

      <!-- Quick Link to Action Brief -->
      <div id="radar-brief-cta" class="hidden p-4 rounded-2xl bg-indigo-950/40 border border-indigo-800/40 flex items-center justify-between">
        <div>
          <h4 class="text-sm font-semibold text-white">Recommended Actions Synthesized</h4>
          <p class="text-xs text-slate-400">Review actionable, low-cost commercial responses backed by verified evidence.</p>
        </div>
        <button onclick="switchView('brief')" class="px-4 py-2 rounded-xl text-xs font-semibold bg-indigo-600 hover:bg-indigo-500 text-white transition flex items-center gap-1.5">
          <span>View Action Brief</span>
          <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14" /><polyline points="12 5 19 12 12 19" /></svg>
        </button>
      </div>
    </div>

    <!-- VIEW 3: ACTION BRIEF SCREEN -->
    <div id="view-brief" class="hidden space-y-6">
      <div class="p-5 rounded-2xl bg-gradient-to-r from-indigo-950/70 via-slate-900 to-slate-900 border border-indigo-900/40 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <div class="flex items-center gap-2">
            <span class="text-xs font-semibold px-2 py-0.5 rounded-full bg-indigo-900/80 text-indigo-300 border border-indigo-700/60">Executive Decision Brief</span>
            <span id="brief-engine-label" class="text-xs text-slate-400 font-mono">Engine: Rule-Based Fallback</span>
          </div>
          <h2 class="text-lg font-bold text-white mt-1">Recommended Commercial Next Actions</h2>
          <p class="text-xs text-slate-400 mt-0.5">Low-overhead actions designed to counter competitor moves without sacrificing unit margins.</p>
        </div>
        <div class="flex items-center gap-2 bg-slate-950/60 px-3.5 py-2 rounded-xl border border-slate-800 text-xs">
          <svg class="w-4 h-4 text-emerald-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10" /><path d="M12 8v4" /><path d="M12 16h.01" /></svg>
          <div class="text-slate-300 text-[11px] leading-tight">
            <span class="font-semibold text-emerald-400">Human Approval Only</span><br />
            No autonomous repricing or sales speculation
          </div>
        </div>
      </div>

      <!-- Action Cards Container -->
      <div id="actions-container" class="space-y-6">
        <!-- Rendered by JS -->
      </div>
    </div>

    <!-- VIEW 4: HISTORY SCREEN -->
    <div id="view-history" class="hidden space-y-6">
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
        <div>
          <h2 class="text-xl font-bold text-white tracking-tight">Snapshot Comparison & History</h2>
          <p class="text-xs text-slate-400 mt-0.5">Compare your baseline position side-by-side with the latest live scan.</p>
        </div>
        <div class="flex items-center gap-2">
          <span class="text-xs text-slate-400">Past Scans:</span>
          <select id="history-select" onchange="loadSelectedSnapshot(this.value)" class="px-3 py-1.5 rounded-xl bg-slate-900 border border-slate-700 text-xs text-white focus:outline-none">
            <!-- Options by JS -->
          </select>
        </div>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <!-- Baseline Column -->
        <div class="glass-panel p-5 rounded-2xl border border-slate-800 space-y-4">
          <div class="flex items-center justify-between pb-3 border-b border-slate-800">
            <div>
              <span id="baseline-chip" class="text-xs font-semibold px-2 py-0.5 rounded-md bg-slate-800 text-slate-300">Active Baseline Snapshot</span>
              <h3 id="baseline-cat" class="text-sm font-bold text-white mt-1">reusable steel water bottles</h3>
              <p id="baseline-date" class="text-[11px] text-slate-500 font-mono">Captured: 14 days ago</p>
            </div>
            <div class="text-right">
              <span id="baseline-items-count" class="text-lg font-bold text-slate-200">7</span>
              <p class="text-[11px] text-slate-500">catalog items</p>
            </div>
          </div>
          <div id="baseline-items-list" class="space-y-2 max-h-[480px] overflow-y-auto pr-1">
            <!-- Items by JS -->
          </div>
        </div>

        <!-- Current Column -->
        <div class="glass-panel p-5 rounded-2xl border border-indigo-900/40 space-y-4">
          <div class="flex items-center justify-between pb-3 border-b border-slate-800">
            <div>
              <span class="text-xs font-semibold px-2 py-0.5 rounded-md bg-indigo-950 text-indigo-300 border border-indigo-800/50">Current Live Scan</span>
              <h3 id="current-cat" class="text-sm font-bold text-white mt-1">reusable steel water bottles</h3>
              <p id="current-date" class="text-[11px] text-slate-500 font-mono">Captured: Just now</p>
            </div>
            <div class="text-right flex items-center gap-3">
              <div>
                <span id="current-items-count" class="text-lg font-bold text-white">0</span>
                <p class="text-[11px] text-slate-500">catalog items</p>
              </div>
              <button onclick="promoteCurrentToBaseline()" id="promote-btn" class="hidden px-2.5 py-1 rounded-lg text-[11px] font-medium bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700 transition">
                Promote to Baseline
              </button>
            </div>
          </div>
          <div id="current-items-list" class="space-y-2 max-h-[480px] overflow-y-auto pr-1">
            <!-- Items by JS -->
          </div>
        </div>
      </div>
    </div>

    <!-- Scan Quality Panel (Bottom) -->
    <div id="quality-panel" class="hidden pt-4">
      <div class="glass-panel p-4 rounded-2xl border border-slate-800 text-xs">
        <div class="flex flex-col lg:flex-row lg:items-center justify-between gap-4">
          <div class="flex flex-wrap items-center gap-4">
            <div class="flex items-center gap-2">
              <span class="text-slate-500 font-medium">SerpApi Results:</span>
              <span id="qp-total" class="px-2 py-0.5 rounded-md bg-slate-900 border border-slate-800 text-slate-200 font-mono font-semibold">0 fetched</span>
            </div>
            <div class="flex items-center gap-2">
              <span class="text-slate-500 font-medium">Deduplicated:</span>
              <span id="qp-dedup" class="px-2 py-0.5 rounded-md bg-slate-900 border border-slate-800 text-indigo-300 font-mono font-semibold">0 merged</span>
            </div>
            <div class="flex items-center gap-2">
              <span class="text-slate-500 font-medium">Noise Filtered:</span>
              <span id="qp-noise" class="px-2 py-0.5 rounded-md bg-slate-900 border border-slate-800 text-cyan-300 font-mono font-semibold">0 accessories</span>
            </div>
            <div class="flex items-center gap-2">
              <span class="text-slate-500 font-medium">Clickable Sources:</span>
              <span id="qp-links" class="px-2 py-0.5 rounded-md bg-emerald-950/70 border border-emerald-800/60 text-emerald-300 font-mono font-semibold flex items-center gap-1">
                <svg class="w-3 h-3 text-emerald-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14" /><polyline points="22 4 12 14.01 9 11.01" /></svg>
                100% live URLs
              </span>
            </div>
          </div>
          <div class="flex items-start gap-1.5 text-[11px] text-slate-400 lg:max-w-md bg-slate-950/60 px-3 py-2 rounded-xl border border-slate-800">
            <svg class="w-3.5 h-3.5 text-slate-400 flex-shrink-0 mt-0.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10" /><path d="M12 8v4" /><path d="M12 16h.01" /></svg>
            <span id="qp-disclaimer">What this prototype does NOT verify: Regional delivery fee variations, cart-level bank instant discounts, or warehouse stockout states.</span>
          </div>
        </div>
      </div>
    </div>

  </main>

  <!-- Footer -->
  <footer class="border-t border-slate-900 bg-slate-950 py-6 text-center text-xs text-slate-500">
    <div class="max-w-7xl mx-auto px-4 flex flex-col sm:flex-row items-center justify-between gap-3">
      <div>RippleWatch · Built for the SerpApi Hackathon · Decision Intelligence over Price Tracking</div>
      <div class="flex items-center gap-4 text-slate-400">
        <span>Google Shopping</span><span>·</span><span>Google News</span><span>·</span><span>Google Search</span>
      </div>
    </div>
  </footer>

  <!-- Application Logic -->
  <script>
    let appState = {
      activeView: 'setup',
      useCache: true,
      profile: {
        business_name: 'EcoVessel India',
        category: 'reusable steel water bottles',
        market: 'India',
        gl: 'in',
        hl: 'en',
        competitors: ['Milton', 'Cello', 'Borosil']
      },
      currentSnapshot: null,
      baselineSnapshot: null,
      snapshotsList: [],
      feedbackGiven: {},
      isScanning: false,
      isSuggesting: false
    };

    async function init() {
      try {
        renderCompetitorChips();
        const baseRes = await fetch('/api/baseline/current?category=' + encodeURIComponent(appState.profile.category) + '&market=' + encodeURIComponent(appState.profile.market));
        if (baseRes.ok) {
          appState.baselineSnapshot = await baseRes.json();
          updateBaselineStatus();
        }

        const listRes = await fetch('/api/snapshots');
        if (listRes.ok) {
          appState.snapshotsList = await listRes.json();
          renderHistoryDropdown();
          if (appState.snapshotsList.length > 0) {
            const latestId = appState.snapshotsList[0].id;
            const snapRes = await fetch('/api/snapshots/' + latestId);
            if (snapRes.ok) {
              appState.currentSnapshot = await snapRes.json();
              renderCurrentSnapshot();
              if (appState.currentSnapshot.signals && appState.currentSnapshot.signals.length > 0) {
                switchView('radar');
              }
            }
          }
        }
      } catch (err) {
        console.error('Init error:', err);
      }
    }

    function switchView(viewName) {
      appState.activeView = viewName;
      ['setup', 'radar', 'brief', 'history'].forEach(v => {
        const el = document.getElementById('view-' + v);
        const tab = document.getElementById('tab-' + v);
        const mTab = document.getElementById('m-tab-' + v);
        if (el) el.classList.toggle('hidden', v !== viewName);
        if (tab) {
          if (v === viewName) {
            tab.className = 'px-3.5 py-1.5 rounded-lg text-xs font-medium transition-all bg-indigo-600 text-white shadow-sm shadow-indigo-500/20';
          } else {
            tab.className = 'px-3.5 py-1.5 rounded-lg text-xs font-medium text-slate-400 hover:text-slate-200 hover:bg-slate-800/60 transition-all';
          }
        }
        if (mTab) {
          if (v === viewName) {
            mTab.className = 'px-3 py-1.5 rounded-lg font-medium bg-indigo-600 text-white';
          } else {
            mTab.className = 'px-3 py-1.5 rounded-lg font-medium text-slate-400';
          }
        }
      });
      if (viewName === 'history') {
        renderHistoryScreen();
      }
    }

    function toggleCache() {
      appState.useCache = !appState.useCache;
      const btn = document.getElementById('cache-toggle-btn');
      const ball = document.getElementById('cache-toggle-ball');
      const label = document.getElementById('cache-toggle-label');
      if (appState.useCache) {
        btn.className = 'relative inline-flex h-5 w-9 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out bg-emerald-600';
        ball.className = 'pointer-events-none inline-block h-4 w-4 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out translate-x-4';
        label.innerText = 'ON';
        label.className = 'text-[11px] font-semibold text-emerald-400';
      } else {
        btn.className = 'relative inline-flex h-5 w-9 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out bg-slate-700';
        ball.className = 'pointer-events-none inline-block h-4 w-4 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out translate-x-0';
        label.innerText = 'OFF';
        label.className = 'text-[11px] font-semibold text-slate-400';
      }
    }

    function renderCompetitorChips() {
      const container = document.getElementById('competitors-container');
      const countEl = document.getElementById('comp-count');
      if (countEl) countEl.innerText = appState.profile.competitors.length;

      let html = '';
      appState.profile.competitors.forEach(comp => {
        html += `
          <div class="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-xl bg-indigo-950/50 border border-indigo-700/60 text-sm font-medium text-white shadow-sm">
            <span class="w-1.5 h-1.5 rounded-full bg-cyan-400"></span>
            <span>${comp}</span>
            <button onclick="removeCompetitor('${comp}')" class="text-slate-400 hover:text-rose-400 transition ml-1">×</button>
          </div>
        `;
      });
      html += `
        <div class="inline-flex items-center gap-1">
          <input type="text" id="new-comp-input" placeholder="+ Add brand name..." onkeydown="if(event.key==='Enter'){event.preventDefault();addCompetitor();}" class="px-3 py-1.5 rounded-xl bg-slate-900 border border-slate-700 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500 w-36 sm:w-44" />
          <button onclick="addCompetitor()" class="p-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 transition">+</button>
        </div>
      `;
      container.innerHTML = html;
    }

    function addCompetitor() {
      const input = document.getElementById('new-comp-input');
      const val = input ? input.value.trim() : '';
      if (val && !appState.profile.competitors.includes(val)) {
        if (appState.profile.competitors.length >= 6) {
          alert('Maximum 5-6 competitors recommended.');
          return;
        }
        appState.profile.competitors.push(val);
        renderCompetitorChips();
      }
    }

    function removeCompetitor(name) {
      if (appState.profile.competitors.length <= 1) {
        alert('At least 1 competitor required.');
        return;
      }
      appState.profile.competitors = appState.profile.competitors.filter(c => c !== name);
      renderCompetitorChips();
    }

    async function suggestCompetitors() {
      const btnText = document.getElementById('suggest-btn-text');
      btnText.innerText = 'Searching SerpApi...';
      try {
        const res = await fetch('/api/competitors/suggest', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({ category: appState.profile.category, market: appState.profile.market })
        });
        if (res.ok) {
          const data = await res.json();
          if (data.suggested_competitors) {
            appState.profile.competitors = Array.from(new Set([...appState.profile.competitors, ...data.suggested_competitors])).slice(0, 5);
            renderCompetitorChips();
            showToast('Discovered top brands: ' + data.suggested_competitors.join(', '));
          }
        }
      } catch (e) {
        showError('Competitor search error: ' + e.message);
      } finally {
        btnText.innerText = 'Suggest Competitors';
      }
    }

    async function seedSampleBaseline() {
      try {
        const res = await fetch('/api/baseline/sample', { method: 'POST' });
        if (res.ok) {
          appState.baselineSnapshot = await res.json();
          updateBaselineStatus();
          showToast('Sample 14-day baseline active. Run a live scan to view market changes.');
          refreshSnapshotsList();
        }
      } catch (e) {
        showError('Failed to seed baseline: ' + e.message);
      }
    }

    function updateBaselineStatus() {
      const label = document.getElementById('baseline-status-label');
      if (label && appState.baselineSnapshot) {
        label.innerText = appState.baselineSnapshot.is_sample ? 'Sample Baseline (14d)' : 'Custom Real Baseline';
      }
    }

    async function runScan(isBaselineCreation = false) {
      const scanBtnText = document.getElementById('scan-btn-text');
      const scanSpinner = document.getElementById('scan-spinner');
      scanBtnText.innerText = isBaselineCreation ? 'Creating Real Baseline...' : 'Scanning SerpApi & Detecting Changes...';
      scanSpinner.classList.add('animate-spin');

      // Update profile from inputs
      appState.profile.business_name = document.getElementById('input-biz-name').value;
      appState.profile.category = document.getElementById('input-category').value;

      try {
        const res = await fetch('/api/scan', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({
            business_profile: appState.profile,
            use_cache: appState.useCache,
            compare_with_snapshot_id: appState.baselineSnapshot ? appState.baselineSnapshot.id : null,
            is_baseline_creation: isBaselineCreation
          })
        });

        if (!res.ok) {
          const errData = await res.json().catch(() => ({}));
          throw new Error(errData.detail || 'Market scan failed');
        }

        const newSnap = await res.json();
        appState.currentSnapshot = newSnap;

        if (isBaselineCreation) {
          appState.baselineSnapshot = newSnap;
          updateBaselineStatus();
          showToast('Real baseline snapshot successfully created from live market data.');
          switchView('history');
        } else {
          showToast('Scan completed! Detected ' + (newSnap.signals ? newSnap.signals.length : 0) + ' market changes.');
          renderCurrentSnapshot();
          switchView('radar');
        }

        refreshSnapshotsList();
      } catch (err) {
        showError(err.message);
      } finally {
        scanBtnText.innerText = 'Run Market Scan';
        scanSpinner.classList.remove('animate-spin');
      }
    }

    async function refreshSnapshotsList() {
      const listRes = await fetch('/api/snapshots');
      if (listRes.ok) {
        appState.snapshotsList = await listRes.json();
        renderHistoryDropdown();
      }
    }

    function renderCurrentSnapshot() {
      if (!appState.currentSnapshot) return;
      renderSignals();
      renderBrief();
      renderQualityPanel();
    }

    function renderSignals() {
      const container = document.getElementById('signals-container');
      const badgeCount = document.getElementById('radar-count-badge');
      const cta = document.getElementById('radar-brief-cta');
      const signals = appState.currentSnapshot.signals || [];

      badgeCount.innerText = 'Showing ' + signals.length + ' signals';
      cta.classList.toggle('hidden', !appState.currentSnapshot.brief || appState.currentSnapshot.brief.actions.length === 0);

      if (signals.length === 0) {
        container.innerHTML = `
          <div class="glass-panel p-12 rounded-2xl text-center space-y-4">
            <div class="w-16 h-16 mx-auto rounded-full bg-slate-900 flex items-center justify-center border border-slate-800">
              <svg class="w-8 h-8 text-emerald-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14" /><polyline points="22 4 12 14.01 9 11.01" /></svg>
            </div>
            <h3 class="text-lg font-semibold text-white">Market Stable — No Outlier Shifts Detected</h3>
            <p class="text-sm text-slate-400 max-w-md mx-auto">Compared to your active baseline, competitor pricing, bundles, and product catalogs are currently in equilibrium.</p>
          </div>
        `;
        return;
      }

      let html = '';
      signals.forEach(sig => {
        let badgeColor = 'bg-slate-800 text-slate-300 border-slate-700';
        let badgeLabel = sig.type;
        if (sig.type === 'PRICE_CHANGE') {
          badgeColor = 'bg-amber-950/70 text-amber-300 border-amber-800/80 badge-glow-amber';
          badgeLabel = 'Price Change (≥5%)';
        } else if (sig.type === 'PROMOTION') {
          badgeColor = 'bg-purple-950/70 text-purple-300 border-purple-800/80';
          badgeLabel = 'Promotion / Bundle';
        } else if (sig.type === 'NEW_PRODUCT') {
          badgeColor = 'bg-cyan-950/70 text-cyan-300 border-cyan-800/80 badge-glow-cyan';
          badgeLabel = 'New SKU Cataloged';
        } else if (sig.type === 'NEWS') {
          badgeColor = 'bg-blue-950/70 text-blue-300 border-blue-800/80';
          badgeLabel = 'Industry News / PR';
        }

        let confPill = '<span class="px-2 py-0.5 rounded-full text-[11px] bg-slate-900 text-slate-400 border border-slate-800 font-medium">Possible</span>';
        if (sig.confidence === 'confirmed') {
          confPill = '<span class="px-2 py-0.5 rounded-full text-[11px] bg-emerald-950/80 text-emerald-300 border border-emerald-800/60 font-semibold flex items-center gap-1">● Confirmed (2+ Sources)</span>';
        } else if (sig.confidence === 'likely') {
          confPill = '<span class="px-2 py-0.5 rounded-full text-[11px] bg-blue-950/80 text-blue-300 border border-blue-800/60 font-medium">● Likely</span>';
        }

        let evHtml = '';
        sig.evidence.forEach(ev => {
          evHtml += `
            <a href="${ev.url}" target="_blank" rel="noopener noreferrer" class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-slate-900/90 hover:bg-slate-800 hover:border-cyan-500/50 border border-slate-700/80 text-xs text-slate-200 transition">
              <span class="font-semibold text-cyan-400">${ev.seller_or_source}</span>
              ${ev.price !== null ? `<span class="text-slate-400 font-mono">· ₹${ev.price.toLocaleString('en-IN')}</span>` : ''}
              <svg class="w-3 h-3 text-slate-500" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6" /><polyline points="15 3 21 3 21 9" /><line x1="10" y1="14" x2="21" y2="3" /></svg>
            </a>
          `;
        });

        html += `
          <div class="glass-panel glass-card p-5 rounded-2xl border border-slate-800 space-y-4">
            <div class="flex flex-wrap items-center justify-between gap-2">
              <div class="flex items-center gap-2">
                <span class="inline-flex items-center gap-1.5 px-3 py-1 rounded-xl text-xs font-semibold border ${badgeColor}">
                  ${badgeLabel}
                </span>
                <span class="text-sm font-bold text-white px-2.5 py-0.5 rounded-lg bg-slate-900 border border-slate-800">
                  ${sig.competitor}
                </span>
              </div>
              <div class="flex items-center gap-2">
                ${confPill}
                <span class="text-[11px] text-slate-500 font-mono">${new Date(sig.observed_at).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}</span>
              </div>
            </div>

            <div class="text-sm font-medium text-slate-100 leading-relaxed bg-slate-950/40 p-3.5 rounded-xl border border-slate-800/80">
              ${sig.what_changed}
            </div>

            <div>
              <div class="text-[11px] font-semibold text-slate-400 uppercase tracking-wider mb-2 flex items-center gap-1.5">
                <svg class="w-3.5 h-3.5 text-cyan-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10" /><path d="M12 16v-4" /><path d="M12 8h.01" /></svg>
                <span>Clickable Source Evidence (${sig.evidence.length} items):</span>
              </div>
              <div class="flex flex-wrap gap-2">
                ${evHtml}
              </div>
            </div>

            <div class="pt-3 border-t border-slate-800/80 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
              <div class="flex items-start gap-1.5 text-[11px] text-slate-500 max-w-xl">
                <svg class="w-3.5 h-3.5 text-slate-500 flex-shrink-0 mt-0.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10" /><path d="M12 8v4" /><path d="M12 16h.01" /></svg>
                <span>${sig.limitations}</span>
              </div>
              <div class="flex items-center gap-2 self-end sm:self-auto">
                <button onclick="submitFeedback('${sig.id}', '${sig.competitor}', '${sig.type}', true)" class="inline-flex items-center gap-1 px-2.5 py-1 rounded-lg text-xs font-medium bg-slate-900 hover:bg-slate-800 text-slate-400 hover:text-emerald-400 border border-slate-800 transition">
                  <svg class="w-3.5 h-3.5 text-emerald-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M7 10v12" /><path d="M15 5.88 14 10h5.83a2 2 0 0 1 1.92 2.56l-2.33 8A2 2 0 0 1 17.5 22H4a2 2 0 0 1-2-2v-8a2 2 0 0 1 2-2h3Z" /></svg>
                  <span>Useful</span>
                </button>
                <button onclick="submitFeedback('${sig.id}', '${sig.competitor}', '${sig.type}', false)" class="inline-flex items-center gap-1 px-2.5 py-1 rounded-lg text-xs font-medium bg-slate-900 hover:bg-slate-800 text-slate-400 hover:text-rose-400 border border-slate-800 transition">
                  <svg class="w-3.5 h-3.5 text-rose-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17 14V2" /><path d="M9 18.12 10 14H4.17a2 2 0 0 1-1.92-2.56l2.33-8A2 2 0 0 1 6.5 2H20a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2h-3Z" /></svg>
                  <span>Irrelevant</span>
                </button>
              </div>
            </div>
          </div>
        `;
      });
      container.innerHTML = html;
    }

    async function submitFeedback(signalId, competitor, signalType, isUseful) {
      try {
        await fetch('/api/signals/feedback', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({
            signal_id: signalId,
            competitor: competitor,
            signal_type: signalType,
            item_title: '',
            is_useful: isUseful
          })
        });
        showToast(isUseful ? 'Signal marked Useful. Saved for decision history.' : 'Signal marked Irrelevant. Suppressing similar patterns in future scans.');
      } catch (e) {
        showError('Feedback error: ' + e.message);
      }
    }

    function renderBrief() {
      const container = document.getElementById('actions-container');
      const engineLabel = document.getElementById('brief-engine-label');
      const brief = appState.currentSnapshot.brief;

      if (!brief || !brief.actions || brief.actions.length === 0) {
        container.innerHTML = `
          <div class="glass-panel p-12 rounded-2xl text-center space-y-4">
            <div class="w-16 h-16 mx-auto rounded-full bg-slate-900 flex items-center justify-center border border-slate-800">
              <svg class="w-8 h-8 text-indigo-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 3l1.9 5.8a2 2 0 0 0 1.3 1.3L21 12l-5.8 1.9a2 2 0 0 0 -1.3 1.3L12 21l-1.9 -5.8a2 2 0 0 0 -1.3 -1.3L3 12l5.8 -1.9a2 2 0 0 0 1.3 -1.3L12 3z" /></svg>
            </div>
            <h3 class="text-lg font-semibold text-white">No Action Brief Available Yet</h3>
            <p class="text-sm text-slate-400 max-w-md mx-auto">Run a market scan to synthesize low-cost, evidence-backed next actions tailored to your niche.</p>
          </div>
        `;
        return;
      }

      engineLabel.innerText = 'Engine: ' + (brief.generated_by === 'gemini' ? 'Gemini 2.5 Flash' : 'Deterministic Rule Engine');

      let html = '';
      brief.actions.forEach((act, idx) => {
        let effortBadge = 'bg-emerald-950/80 text-emerald-300 border-emerald-800/80';
        if (act.effort === 'medium') effortBadge = 'bg-amber-950/80 text-amber-300 border-amber-800/80';
        if (act.effort === 'high') effortBadge = 'bg-rose-950/80 text-rose-300 border-rose-800/80';

        let checkHtml = '';
        act.verify_before_acting.forEach(chk => {
          checkHtml += `
            <label class="flex items-start gap-2.5 text-xs text-slate-300 select-none cursor-pointer">
              <input type="checkbox" class="mt-0.5 rounded border-slate-700 bg-slate-800 text-indigo-600 focus:ring-0" />
              <span>${chk}</span>
            </label>
          `;
        });

        html += `
          <div class="glass-panel p-6 rounded-2xl border border-slate-800 space-y-5 transition-all hover:border-indigo-500/30">
            <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-3 border-b border-slate-800/80">
              <div class="flex items-start gap-3">
                <span class="flex items-center justify-center w-7 h-7 rounded-xl bg-indigo-900/60 text-indigo-300 font-bold text-xs border border-indigo-700/60 flex-shrink-0 mt-0.5">
                  #${idx + 1}
                </span>
                <h3 class="text-base font-bold text-white tracking-tight">${act.title}</h3>
              </div>
              <div class="flex items-center gap-2 self-start sm:self-auto">
                <span class="px-2.5 py-1 rounded-lg text-xs font-semibold uppercase tracking-wider border ${effortBadge}">
                  ${act.effort} Effort
                </span>
                <span class="px-2.5 py-1 rounded-lg text-xs bg-slate-900 border border-slate-800 text-slate-300">
                  Confidence: <span class="text-emerald-400 font-semibold">${act.confidence}</span>
                </span>
              </div>
            </div>

            <div class="space-y-1.5">
              <h4 class="text-xs font-semibold text-slate-400 uppercase tracking-wider">Why this matters (Decision Rationale)</h4>
              <p class="text-sm text-slate-200 leading-relaxed bg-slate-950/40 p-3.5 rounded-xl border border-slate-800/70">
                ${act.rationale}
              </p>
            </div>

            <div class="space-y-2">
              <h4 class="text-xs font-semibold text-slate-400 uppercase tracking-wider flex items-center gap-1.5">
                <svg class="w-3.5 h-3.5 text-cyan-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14" /><polyline points="22 4 12 14.01 9 11.01" /></svg>
                <span>Verify Before Acting (Human Checklist)</span>
              </h4>
              <div class="space-y-2 bg-slate-900/60 p-3.5 rounded-xl border border-slate-800">
                ${checkHtml}
              </div>
            </div>

            <div class="pt-2">
              <h4 class="text-[11px] font-semibold text-slate-500 uppercase tracking-wider mb-2">Supporting Evidence Citations (${act.evidence_ids.length}):</h4>
              <div class="flex flex-wrap gap-2">
                ${act.evidence_ids.map(id => `<span class="px-2.5 py-1 rounded-lg bg-slate-900 border border-slate-800 text-[11px] font-mono text-cyan-400">#${id}</span>`).join('')}
              </div>
            </div>
          </div>
        `;
      });
      container.innerHTML = html;
    }

    function renderHistoryDropdown() {
      const select = document.getElementById('history-select');
      if (!select) return;
      select.innerHTML = appState.snapshotsList.map(s => `
        <option value="${s.id}" ${appState.currentSnapshot && appState.currentSnapshot.id === s.id ? 'selected' : ''}>
          ${new Date(s.created_at).toLocaleDateString()} ${new Date(s.created_at).toLocaleTimeString([], {hour:'2-digit', minute:'2-digit'})}
          ${s.is_baseline ? ' [Baseline]' : ''} ${s.is_sample ? ' (Sample)' : ''}
        </option>
      `).join('');
    }

    async function loadSelectedSnapshot(id) {
      const res = await fetch('/api/snapshots/' + id);
      if (res.ok) {
        appState.currentSnapshot = await res.json();
        renderCurrentSnapshot();
        renderHistoryScreen();
      }
    }

    function renderHistoryScreen() {
      const bItems = document.getElementById('baseline-items-list');
      const cItems = document.getElementById('current-items-list');
      const bCount = document.getElementById('baseline-items-count');
      const cCount = document.getElementById('current-items-count');
      const promoteBtn = document.getElementById('promote-btn');

      if (appState.baselineSnapshot) {
        bCount.innerText = appState.baselineSnapshot.items.length;
        bItems.innerHTML = appState.baselineSnapshot.items.map(it => `
          <div class="p-3 rounded-xl bg-slate-950/40 border border-slate-800/80 flex items-center justify-between gap-3 text-xs">
            <div class="min-w-0">
              <div class="flex items-center gap-1.5 mb-0.5">
                <span class="font-semibold text-slate-300">${it.competitor}</span>
                <span class="text-slate-500">· ${it.seller_or_source}</span>
              </div>
              <p class="text-slate-400 truncate">${it.title}</p>
            </div>
            <div class="text-right flex-shrink-0 font-mono font-semibold text-slate-200">
              ${it.price !== null ? `₹${it.price.toLocaleString('en-IN')}` : 'N/A'}
            </div>
          </div>
        `).join('');
      }

      if (appState.currentSnapshot) {
        cCount.innerText = appState.currentSnapshot.items.length;
        promoteBtn.classList.toggle('hidden', appState.currentSnapshot.is_baseline);
        cItems.innerHTML = appState.currentSnapshot.items.map(it => {
          return `
            <div class="p-3 rounded-xl bg-slate-950/40 border border-slate-800/80 flex items-center justify-between gap-3 text-xs">
              <div class="min-w-0">
                <div class="flex items-center gap-1.5 mb-0.5">
                  <span class="font-semibold text-white">${it.competitor}</span>
                  <span class="text-slate-400">· ${it.seller_or_source}</span>
                </div>
                <p class="text-slate-300 truncate">${it.title}</p>
              </div>
              <div class="text-right flex-shrink-0 flex items-center gap-2">
                <span class="font-mono font-semibold text-white">
                  ${it.price !== null ? `₹${it.price.toLocaleString('en-IN')}` : 'N/A'}
                </span>
                <a href="${it.url}" target="_blank" class="text-slate-500 hover:text-cyan-400">
                  <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6" /><polyline points="15 3 21 3 21 9" /><line x1="10" y1="14" x2="21" y2="3" /></svg>
                </a>
              </div>
            </div>
          `;
        }).join('');
      }
    }

    async function promoteCurrentToBaseline() {
      if (!appState.currentSnapshot) return;
      try {
        await fetch('/api/baseline/set/' + appState.currentSnapshot.id, { method: 'POST' });
        appState.baselineSnapshot = appState.currentSnapshot;
        updateBaselineStatus();
        showToast('Snapshot promoted to active baseline.');
        refreshSnapshotsList();
        renderHistoryScreen();
      } catch (e) {
        showError('Promote error: ' + e.message);
      }
    }

    function renderQualityPanel() {
      const qp = document.getElementById('quality-panel');
      const q = appState.currentSnapshot.quality_metrics;
      if (!q) {
        qp.classList.add('hidden');
        return;
      }
      qp.classList.remove('hidden');
      document.getElementById('qp-total').innerText = q.total_results_fetched + ' fetched';
      document.getElementById('qp-dedup').innerText = q.duplicates_removed + ' merged';
      document.getElementById('qp-noise').innerText = q.noise_filtered + ' accessories';
      document.getElementById('qp-links').innerHTML = `
        <svg class="w-3 h-3 text-emerald-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14" /><polyline points="22 4 12 14.01 9 11.01" /></svg>
        ${q.working_links_pct}% live URLs
      `;
      document.getElementById('qp-disclaimer').innerText = q.verification_disclaimer;
    }

    function showToast(msg) {
      const banner = document.getElementById('toast-banner');
      const msgEl = document.getElementById('toast-message');
      msgEl.innerText = msg;
      banner.classList.remove('hidden');
      setTimeout(hideToast, 4000);
    }
    function hideToast() {
      document.getElementById('toast-banner').classList.add('hidden');
    }
    function showError(msg) {
      const banner = document.getElementById('error-banner');
      document.getElementById('error-message').innerText = msg;
      banner.classList.remove('hidden');
    }
    function hideError() {
      document.getElementById('error-banner').classList.add('hidden');
    }

    // Auto-init on page load
    window.addEventListener('DOMContentLoaded', init);
  </script>
</body>
</html>
"""
