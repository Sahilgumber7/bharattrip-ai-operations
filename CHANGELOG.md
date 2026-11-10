# Changelog

All notable changes made to the BharatTrip AI Operations take-home screening submission are documented below.

---

### Latest Iteration: Stale Figures Elimination & Write-Up Alignment

1. **`reconciler.py` & `reconciled_data.json`:**
   - Removed confusing legacy keys (`support_duplicates: 22`, which was extra rows sharing an ID rather than exact duplicates, and ambiguous `amount_mismatches: 3`).
   - Cleanly separated `exact_duplicate_rows_support` (12) and `conflicting_id_rows_support` (10).
   - Preserved all 10 standard named metrics: `exact_duplicate_rows_support` (12), `exact_duplicate_rows_finance` (0), `conflicting_id_rows_support` (10), `dropped_handoffs` (69), `shadow_finance_intakes` (16), `june_pending_payouts` (58), `completed_payouts_with_gap` (53), `gap_explained_by_deduction` (556), `unexplained_gaps` (`['RF-1041', 'RF-1368', 'RF-1435']`), and `avg_total_lag_days` (6.23).
   - Added `completed_gaps_explained_by_deduction: 50` so that both the total matched explained count (556 of 571) and the gap-specific explained count (50 of 53) are reported with complete mathematical transparency.

2. **`build_frontend.py` & `index.html`:**
   - Updated dropped tickets copy to 69 tickets (removing the stale "111 tickets 'Closed'" and "78 tickets" references).
   - Updated amount gap copy to reflect the exact empirical breakdown: 53 completed payouts with gaps, 556 of 571 matched payouts explained by deduction (including 50 of the 53 gap cases), and 3 unexplained cases (`RF-1041`, `RF-1368`, `RF-1435`).
   - Explicitly distinguished between the **2.47 days average handoff lag** and the **6.23 days total end-to-end turnaround lag**.
   - Regenerated `reconciled_data.json` and compiled clean `index.html` with snapshot footer.

3. **`README.md` & `app.py`:**
   - `README.md`: Corrected dropped handoffs to 69 tickets and 32 linked customer escalations; updated amount opacity to 53 gaps with 3 unexplained; labeled 2.47 days as handoff lag and 6.23 days as total lag.
   - `app.py`: Replaced stale "78 tickets" with 69, updated root cause 4 to state the 53 completed gaps and 3 unexplained cases, and updated secondary SLA metrics to distinguish handoff lag (2.47 days) from total turnaround lag (6.23 days).

4. **`PROMPT_HISTORY.md`:**
   - Corrected line 35 to note 12 exact duplicates plus 10 conflicting IDs in Support Tracker.
   - Corrected line 71 to 32 direct escalations linked to dropped tickets.
   - Corrected line 126 to replace stale "88 cases" with 53 completed gaps (556 of 571 explained, 3 unexplained).

5. **`BharatTrip_AI_Operations_WriteUp.md`, PDF & DOCX:**
   - **Amounts Section:** Rewrote Section 1 and Table 2 to explain that among completed payouts, 53 had gaps; standard deductions explain 50 of them (and 556 of 571 matched payouts overall), leaving only 3 true unexplained discrepancies (`RF-1041`, `RF-1368`, `RF-1435`). Support quoting gross amounts without itemized deduction slips is what creates agent escalations.
   - **Dropped Tickets:** Standardized dropped handoffs to 69 tickets and 32 customer escalations across all narrative and tabular sections.
   - **Intake Agent:** Clarified in Section 3 and Section 4 that the intake agent is a deterministic, rule-based NLP parser (not an LLM), issuing unique stable reference IDs (`RF-NEW-<HEX>`) and safe status confirmations without premature financial or timeline commitments.
   - **Page Count Verification:** Regenerated `BharatTrip_AI_Operations_WriteUp.pdf` via `generate_pdf.py` and confirmed exact page count is **3 pages**. Regenerated Word document via `generate_docx.py`.

---

### Previous Fixes Summary

1. **`ai_intake_agent.py`:**
   - Unique reference IDs generated via SHA-256 hex suffix (`RF-NEW-<6 uppercase hex chars>`). Stable across runs for identical inputs; distinct across different inputs.
   - Proactive draft response stripped of promises, timelines, or verification claims.
   - Retained pure rule-based regex extraction, intent parsing, and urgency scoring; 0 LLM dependencies.

2. **`reconciler.py`:**
   - Resolves `BharatTrip_Refund_Data.xlsx` dynamically with CLI and env var overrides.
   - Reports all 10 required named summary metrics with 100% precision.
   - Unified June pending payouts and bottleneck metric to 58.

3. **Relative Paths & Clean Terminology:**
   - Replaced all absolute `file:///c:/...` links with relative paths.
   - Eliminated all occurrences claiming live data across documentation and frontend.
