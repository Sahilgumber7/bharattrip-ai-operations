# AI Prompt History & Working Notes

This is an informal log of the prompts, queries, and iterative reasoning I used while working through the BharatTrip task with AI. Rather than polishing this into a formal corporate report, I've kept it as an authentic working diary showing how I used AI to explore the data, test hypotheses, catch discrepancies, write scripts, and build the prototype.

---

### 1. Understanding the Brief & Setting Guardrails

I started by feeding the PDF brief and the problem context to the AI to make sure I wasn't missing any hidden requirements or unstated constraints.

**Prompt to AI:**
> "I'm working on a take-home screening task for BharatTrip (a B2B travel company). Agents cancel bookings and ask for refunds. Two separate teams handle this: Support tracks requests in one sheet, Finance pays out and tracks in another sheet.
> 
> The core problem: Escalations have climbed over the last two months, but refund volume has stayed roughly flat. Leadership wants escalations brought down without adding headcount.
> 
> Can you extract the core deliverables, constraints, and evaluate what leadership is really asking for here? Be direct—no fluff."

**What came out of this:**
The AI summarized the strict constraints:
- Max 3-page PDF write-up covering Problem Definition, Analysis, Solution Design, and Measurement.
- Working prototype with a one-line run instruction.
- Zero new headcount (so any solution that says "hire 3 more support reps" is an immediate fail).
- The brief is deliberately incomplete (e.g. no SLA docs, no written refund policy), so I need to state my assumptions clearly.

---

### 2. Initial Data Inspection (Sanity Checking the Spreadsheets)

Before jumping to conclusions, I wanted to see what the data actually looked like. The brief mentioned four tabs: `Read_Me`, `Support_Tracker`, `Finance_Tracker`, and `Escalations`.

**Prompt to AI:**
> "Write a quick Python script using pandas to inspect `BharatTrip_Refund_Data_final (5).xlsx`. Load all sheets, print out column headers, row counts, null values, and check for basic hygiene issues like duplicate IDs or weird formatting."

**What we found:**
- `Support_Tracker`: 755 rows, but only 733 unique Ticket IDs (12 exact duplicates plus 10 conflicting IDs). The `Status` column had trailing spaces in places like `'Closed '` vs `'Closed'`.
- `Finance_Tracker`: 689 rows, 680 unique Ref Nos (9 duplicates). Ref numbers were formatted inconsistently (`RF 1079` with a space vs `RF-1079` with a hyphen).
- `Escalations`: 155 rows, started March 1, 2026.

---

### 3. Testing the Volume Hypothesis (Did demand actually spike?)

Leadership's natural suspicion when complaints rise is usually "we got slammed with too many requests." I wanted to verify if that was true or if volume was actually flat.

**Prompt to AI:**
> "Let's group Support requests, Finance payouts, and Escalations by month from February to June 2026. Parse the dates carefully (dayfirst=True). Show me the monthly counts side-by-side so we can see the exact trajectory."

**The numbers:**
- Support Intake: Feb (150), Mar (146), Apr (145), May (147), Jun (144). It is almost perfectly flat at ~146 requests a month.
- Escalations: Feb (2), Mar (23), Apr (25), May (30), **June (75)**.
- June completed payouts collapsed to 60 (down from 115 in May).

**My takeaway:**
The volume hypothesis is completely false. The demand didn't change at all. Something internally broke down hard in May and June.

---

### 4. Reconciling the Two Sheets (Where are the dropped tickets?)

The brief noted that Support and Finance built their trackers independently and never reconciled them. I wanted to see how many tickets were in one sheet but not the other.

**Prompt to AI:**
> "Write a script to normalize the ticket IDs (strip whitespace, make regex match `RF\s*[-]?\s*(\d+)` to `RF-\1`), deduplicate both sheets, and do a full outer join between Support_Tracker and Finance_Tracker. 
> 
> How many tickets are in both? How many exist ONLY in Support? How many exist ONLY in Finance? And how many of the 155 escalations match these missing tickets?"

**What came back:**
- Overlapping in both: 664 unique tickets.
- **Support Only: 69 unique tickets** (Support marked them closed, but Finance never even received them!).
- **Finance Only: 16 unique tickets**. Finance processed tickets that Support never logged (shadow requests).
- **Direct escalations link:** 32 escalations specifically matched tickets that Support logged and closed, but Finance had zero record of.

**My takeaway:**
This explains the "Ticket shows closed, Finance has no record" complaint. Support agents were marking tickets "Closed" as soon as they replied to an email or agent, assuming someone else would take care of the payout. "Closed" to Support did not mean "Refund Paid".

---

### 5. Finding the Smoking Gun: Why did June explode?

Escalations were hovering around 25–30 in March, April, and May, then spiked to 75 in June. Why June specifically?

**Prompt to AI:**
> "Look closely at `Finance_Tracker` across the months. Check `Approved By`, `Payout Status`, and `Remarks`. Is there an approval bottleneck? Did someone leave or stop approving in June?"

**The discovery:**
- In February, March, April, and May, pending payouts at month-end were **0**.
- In June, **55 payouts were stuck in `Pending Payout` status** (accounting for 47% of all June refunds received by Finance!).
- Looking at `Approved By`:
  - `N. Iyer` approved 21 in Feb, 30 in Mar, 24 in Apr, 21 in May.
  - In June: `N. Iyer`'s last approval was on **June 13**, and then zero.
  - `R. Menon`'s last approval was on **June 12**, and then zero.
  - `S. Bhatt` approved only 1 payout in June.

**My takeaway:**
This was the smoking gun. The entire finance payout workflow relied on one or two individuals manually signing off tickets. When N. Iyer was away or stopped signing off after mid-June, the queue ground to a halt with no backup or automated delegation rule. Because nobody told the travel agents why their money was delayed, the agents followed up repeatedly and then escalated.

---

### 6. Checking the Brief's Real Examples (The WhatsApp & Email Ghost Requests)

The brief included three real-world quotes:
1. Nomad Travel on WhatsApp: *"Bhai refund ka kya hua? BLR-MAA wala. 2 hafte ho gaye..."* (referenced as RF-1098).
2. Peak Journeys on Email: *"DEL-DXB last week... no reference number..."* (referenced as RF-1099).
3. Support agent note: *"Finance says they never received several refunds I closed last month..."*

**Prompt to AI:**
> "Search the Excel workbook specifically for RF-1098 and RF-1099 across all sheets. Are they in Support? Are they in Finance? Where do they show up?"

**Result:**
- `RF-1098` and `RF-1099` are **completely missing** from both `Support_Tracker` and `Finance_Tracker`.
- They appear **only** in the `Escalations` sheet (`ESC-592` and `ESC-587`).

**My takeaway:**
This confirms the "Shadow Channel" leak. When agents pinged Support on WhatsApp or personal email, Support agents verbally acknowledged the cancellation but never created a ticket in the tracker. The customer waited two weeks, had no reference ID, and escalated.

---

### 7. Amount Discrepancies (Gross vs. Net)

Another common complaint in the Escalations tab was *"refund received is less than promised"* or *"two different figures quoted"*.

**Prompt to AI:**
> "Compare `Refund Amount (INR)` in Support against `Amount Paid (INR)` + `Deduction (INR)` in Finance for overlapping tickets. How many have differences, and what do the remarks say?"

**Result:**
- 53 gaps among completed payouts where requested amount exceeded paid amount. Standard cancellation deductions explain 556 of 571 matched payouts (including 50 of the 53 gap cases), leaving only 3 true unexplained discrepancies (RF-1041, RF-1368, RF-1435).
- When Support quotes gross booking price without deduction visibility, agents perceive standard airline cancellation charges as unexplained short payments.

---

### 8. Designing the Solution (Under Zero Headcount)

Now that the root causes were clear, I worked with the AI to map out a target workflow that fixes these issues without hiring more people.

**Prompt to AI:**
> "Let's design the target operating model for BharatTrip refunds. Keep the zero-headcount constraint front and center.
> 
> 1. We need a Single Source of Truth (SSOT) instead of two sheets.
> 2. What should the lifecycle states be? Replace 'Closed' with real states so agents don't get misled.
> 3. Create an explicit trade-off table: what do we automate, and what do we keep manual?
> 4. How do we prevent the N. Iyer approval choke from happening again?"

**Key decisions made:**
- **Deterministic 5-stage lifecycle:** `INTAKE_CAPTURED` $\rightarrow$ `ELIGIBILITY_VERIFIED` $\rightarrow$ `FINANCE_QUEUED` $\rightarrow$ `PAYOUT_APPROVED` $\rightarrow$ `SETTLED / DECLINED`.
- **Auto-batch approvals:** Automatically approve routine cancellations under INR 25,000 that fall within published policy rules. Only high-value (>INR 25,000) or disputed edge cases go to a manager's manual queue.
- **Automated outbound updates:** Send automated WhatsApp/Email confirmations on state changes so agents don't have to chase for status.

---

### 9. Prototyping: What should we actually build?

I wanted to make sure the prototype wasn't just a generic chatbot or a dashboard that nobody uses.

**Prompt to AI:**
> "The brief says: 'A rough prototype that solves the right problem beats a slick one that solves the wrong problem. We care that it runs and that the choice of what to build shows judgement.'
> 
> What slice of the problem should we build to show real operational judgement?
> Option A: An AI chatbot for agents to ask refund questions.
> Option B: A reconciliation script that joins the sheets and finds dropped tickets.
> Option C: A dual tool: (1) An intake parser that ingests messy Hinglish WhatsApp/Email messages, creates canonical RF-IDs, and drafts transparent replies; and (2) An automated cross-tracker reconciliation engine with a visual UI."

**My takeaway:**
Option C is clearly the best. A chatbot doesn't solve dropped spreadsheets or approval freezes. But an intake parser prevents unlogged ghost requests (like RF-1098), and a reconciler catches dropped tickets before agents complain.

---

### 10. Building the Prototype Modules

**Prompt to AI (Building the parser):**
> "Write `ai_intake_agent.py`. It should take unstructured text—including colloquial Hinglish like the Nomad Travel message ('Bhai refund ka kya hua? BLR-MAA wala. 2 hafte ho gaye')—and extract:
> - Travel Agent name
> - Route/Sector
> - Intent (status inquiry vs new cancellation)
> - Urgency & wait duration
> - Assign a canonical ticket ID
> - Draft an immediate, professional outbound reply with tracking reference and 24-48h turnaround time."

**Prompt to AI (Building the reconciler):**
> "Write `reconciler.py` to ingest the Excel file, clean IDs, do the outer join, categorize the records into `DROPPED_HANDOFF`, `APPROVAL_BOTTLENECK`, `AMOUNT_MISMATCH`, `SHADOW_INTAKE`, and `RECONCILED_OK`, and export summary stats."

**Prompt to AI (Building the UI):**
> "Build a clean, high-density HTML frontend (`index.html`) that embeds all 749 records so it runs 100% offline in any browser without needing a server. Make it look like a real internal operations tool (Linear/Stripe style), not AI marketing slop. Include:
> - Executive summary numbers
> - A step-by-step visual diagnostic flow showing how we arrived at the solution
> - Searchable and filterable reconciliation table with CSV export
> - An interactive message parser where someone can test the Nomad Travel and Peak Journeys cases
> - The target workflow and 30-day scorecard."

---

### 11. Drafting the 3-Page PDF Write-Up

Finally, I needed to compile the analysis into a strict 3-page PDF.

**Prompt to AI:**
> "Write a Python script using ReportLab to generate `BharatTrip_AI_Operations_WriteUp.pdf`. 
> Strict requirement: It must be EXACTLY 3 pages. No overflow onto page 4.
> - Page 1: Problem Definition, macro volume table, and why flat volume + surging complaints = internal breakdown.
> - Page 2: Deep dive analysis, tracker reconciliation table, validation of the unlogged cases (RF-1098 & RF-1099), and what we'd validate with more time.
> - Page 3: Target solution architecture, automation vs manual trade-off matrix, prototype scope, and 30-day measurement scorecard.
> - Replace unicode rupee symbols with 'INR' so Helvetica doesn't render glyph boxes."

**Verification:**
The script generated `BharatTrip_AI_Operations_WriteUp.pdf` at exactly 3 pages with clean typography and zero overflow.

---

### Summary of What Worked Well with AI

1. **Fast forensic queries:** Using AI to quickly write pandas scripts let me test and discard false hypotheses (like volume overload) in minutes.
2. **Finding needles in haystacks:** Pinpointing `N. Iyer`'s last approval date on June 13 and discovering that `RF-1098` existed only in Escalations would have taken hours of manual scanning in Excel.
3. **Iterative refinement:** When the initial HTML output had too much marketing buzzword fluff, I asked the AI to strip the fluff and build a dense, legible internal operations tool with a visual diagnostic flow.
