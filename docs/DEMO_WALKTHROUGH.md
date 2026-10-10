# RippleWatch — Hackathon Demo Walkthrough Guide

This guide walks you through demonstrating **RippleWatch** for the SerpApi Hackathon.

---

## 🚀 Quick Setup (2 Minutes)

### 1. Backend Setup
1. Open a terminal in the project root:
   ```bash
   cd backend
   # Virtual environment is in ../.venv or create a new one:
   ..\.venv\Scripts\activate   # On Windows
   # or source .venv/bin/activate on macOS/Linux
   ```
2. Verify `.env` has your `SERPAPI_KEY`:
   ```bash
   # backend/.env contains:
   SERPAPI_KEY=your_key_here
   GEMINI_API_KEY=your_key_here  # Optional: falls back to deterministic rule engine if missing
   ```
3. Start the FastAPI backend:
   ```bash
   python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```
   Backend will be running at: `http://localhost:8000` (Swagger docs at `/docs`).

---

### 2. Frontend Setup
1. In a second terminal:
   ```bash
   cd frontend
   npm run dev
   ```
2. Open your browser at: `http://localhost:3000`

---

## 🎯 Guided Evaluation Walkthrough

### Step 1: Market Setup & Baseline (Screen 1)
1. Upon loading `http://localhost:3000`, notice the top header:
   - **SerpApi**: `Connected` (green pill).
   - **Disk Cache**: `ON` (conserves API quota with 24h TTL; toggleable in 1 click).
   - **Default Demo Niche**: `reusable steel water bottles, India` (`gl=in`, `hl=en`).
   - **Tracked Competitor Brands**: `Milton`, `Cello`, `Borosil`.
2. Notice the **"Active Baseline"** indicator:
   - A realistic sample baseline representing market data from 14 days ago is pre-loaded so that the change comparison step can be demonstrated immediately!
   - *(Optional)* Click **"Suggest Competitors"**: SerpApi queries Google Search for top category manufacturers and enriches your tracked list.

---

### Step 2: Running a Live Scan via SerpApi
1. Click the gradient **"Run Market Scan"** button.
2. What happens under the hood:
   - **Multi-Engine Execution**: Queries Google Shopping (`shopping_results`), Google News (`news_results`), and Google Search (`organic_results`) for each competitor.
   - **Disk Caching**: If results are already cached, loads in <200ms. If uncached, makes live SerpApi calls and caches them to disk.
   - **Normalization & Noise Filtering**: Accessories (bottle cleaning brushes, replacement caps, silicone boots) are automatically filtered out.
   - **Intelligent Deduplication**: Merges duplicate listings without collapsing 500ml vs 1000ml bottle variants.
   - **Delta Detection**: Compares against the baseline snapshot and emits signals (`NEW_PRODUCT`, `PRICE_CHANGE`, `PROMOTION`, `NEWS`).
   - **Action Brief Synthesis**: Synthesizes 1–3 low-cost next actions strictly grounded in the evidence.

---

### Step 3: Signal Radar (Screen 2)
1. The UI automatically transitions to the **Signal Radar** screen.
2. Observe the signal cards:
   - **Type Badges**:
     - `NEW_PRODUCT` (Cyan pill): New competitor SKU cataloged.
     - `PRICE_CHANGE` (Amber pill): Verified price movements ≥ 5%.
     - `PROMOTION` (Purple pill): Newly detected bundles (`combo`, `pack of 2`, `% off`).
     - `NEWS` (Blue pill): Industry articles or press announcements.
   - **Confidence Pills**:
     - `Confirmed`: Observed across 2+ independent retailers/platforms.
     - `Likely`: Direct listing on a major retailer.
   - **Clickable Source Evidence**:
     - Click any source pill (e.g., `Amazon IN`, `Flipkart`, `Milton.in`) to open the live retailer product listing in a new tab!
   - **Limitations Notice**:
     - Explains potential delivery fee or card-specific discount factors.
   - **Signal Quality Feedback**:
     - Click **Useful** (thumbs up) or **Irrelevant** (thumbs down).
     - Irrelevant signals persist suppression tokens to prevent future false positives!

---

### Step 4: Executive Action Brief (Screen 3 — Core Value)
1. Click the **"Action Brief"** tab in the navigation.
2. Review the 1–3 recommended actions:
   - **Action Title**: Short imperative recommendation (e.g., *"Highlight build quality and warranty over price matching against Milton"*).
   - **Decision Rationale**: Concrete business explanation of why this matters without hype.
   - **Effort Badge**: `Low`, `Medium`, or `High` effort.
   - **Verify Before Acting (Human Checklist)**: Interactive checkboxes the owner can review before making any commercial changes.
   - **Clickable Evidence Citations**: Every recommendation cites exact signal and item IDs linking to live retailer URLs.
   - **Governance Banner**: Reassures the user that recommendations require human approval and RippleWatch never auto-reprices.

---

### Step 5: Snapshot History & Diff Highlighting (Screen 4)
1. Click the **"Snapshot History"** tab.
2. View the **Baseline Snapshot** and **Current Live Scan** side-by-side.
3. Notice items with detected price drops or newly cataloged models highlighted with color badges.
4. Test the **"Promote to Baseline"** button: easily promote any past scan to be the active baseline for future comparisons.

---

### Step 6: Scan Quality & Transparency Panel
1. Look at the bottom quality panel present on all screens:
   - **Total SerpApi Results Fetched**: (e.g., 178 items)
   - **Duplicates Merged**: (e.g., 6 items)
   - **Noise Filtered**: (accessories and cleaning brushes excluded)
   - **Clickable Live URLs**: (100% verified source links)
   - **Prototype Transparency Note**: Transparently clarifies what the prototype does and does not verify.
