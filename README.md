# BharatTrip AI Operations Associate — Take-Home Submission

This repository contains the complete submission package for the **BharatTrip AI Operations Associate Take-Home Screening Task**.

---

## ⚡ Run

Place `BharatTrip_Refund_Data.xlsx` in the same folder, then run:

```bash
python run.py
```

### Options:
- **Terminal Reconciler & Intake Agent Test:**
  ```bash
  python run.py
  ```
- **Modern Executive HTML Web App (Recommended):**
  Simply double-click [`index.html`](index.html) to open directly in any browser (Chrome, Edge, Safari), or launch a local web server:
  ```bash
  python run.py --web
  ```
- **Interactive Streamlit Copilot:**
  ```bash
  streamlit run app.py
  ```

---

## 📦 Submission Deliverables Inventory

| Deliverable | File / Location | Description |
| :--- | :--- | :--- |
| **1. Official 3-Page Write-up (PDF)** | [`BharatTrip_AI_Operations_WriteUp.pdf`](BharatTrip_AI_Operations_WriteUp.pdf) | Concise, executive-ready 3-page PDF covering Problem Definition, Deep-Dive Analysis, Target Solution, Prototype Justification, and 30-Day Measurement Scorecard. |
| **2. Working AI Prototype** | [`app.py`](app.py) & [`run.py`](run.py) | Full-stack Python application featuring cross-tracker reconciliation, approval bottleneck detection, and an AI Omnichannel Intake Agent. |
| **3. AI Prompt History** | [`PROMPT_HISTORY.md`](PROMPT_HISTORY.md) | Chronological log of actual prompts used with AI tools across data analysis, problem diagnosis, solution architecture, and prototype engineering. |

---

## 🔍 Key Empirical Findings from the Operational Data

1. **The Volume Invariance Paradox:**  
   Monthly refund request intake remained flat (~145/month: Feb 150, Mar 146, Apr 145, May 147, Jun 144). The problem is **not** a surge in workload volume or an understaffing issue.
2. **The June Escalation Explosion (+150% MoM):**  
   Escalations surged from 30 in May to **75 in June** (a 52.1% escalation rate).
3. **The Silent June Approval Freeze:**  
   Prior to June, month-end pending payouts were 0. In June, **58 payouts stalled in `Pending Payout` status** (47% of June Finance intake). Primary approver *N. Iyer* recorded zero sign-offs after June 13, and *R. Menon* stopped June 12. No delegation failover existed, silently halting disbursements.
4. **Disconnected Trackers & Dropped Handoffs:**  
   **69 tickets** logged in Support were marked `"Closed"` without Finance having any record of them, directly triggering 32 customer escalations (*"Ticket closed, Finance has no record"* / *"Marked complete on Support side"*).
5. **The Unlogged "Shadow Channel" Leak:**  
   Real cases from the brief (**RF-1098** Nomad Travel WhatsApp, **RF-1099** Peak Journeys Email) exist **only in the Escalations tab**. They were acknowledged verbally by Support without issuing a ticket reference, causing agents to chase for weeks in the dark.
6. **Deduction Transparency & Amount Gaps:**  
   There are 53 gaps among completed payouts where requested amount exceeded paid amount. Standard cancellation deductions explain 556 of 571 matched payouts (including 50 of the 53 gap cases), leaving only 3 true unexplained discrepancies (RF-1041, RF-1368, RF-1435).

---

## 🏗️ Target Operating Model (Zero-Headcount Constraint)

```
[Agent Channels: WhatsApp / Email / Portal]
       │
       ▼
[AI Omnichannel Intake Agent] ──> Auto-extracts Route/Agent, assigns canonical RF-ID, calculates standard deductions
       │
       ▼
[Single Source of Truth (SSOT)] ──> Deterministic State Machine:
  1. REQUEST_CAPTURED ──> 2. ELIGIBILITY_VERIFIED ──> 3. FINANCE_QUEUED ──> 4. PAYOUT_APPROVED ──> 5. SETTLED
       │
       ├──> Unified Two-Way Sync (Support & Finance views share same underlying database)
       ├──> Automated Webhooks to Agents on State Changes (Eliminates status chasing)
       └──> Automated Batch Approvals for Routine Payouts (≤ INR 25,000)
```

### Strategic Trade-Off Summary:
* **Automate:** Omnichannel ticket creation, cancellation deduction calculation, proactive customer notifications, and cross-tracker reconciliation.
* **Keep Manual:** High-value refunds (> INR 25,000), disputed fare waivers (airline bankruptcy/medical), and key account partner escalations.

---

## 🎯 30-Day Measurement Scorecard

* **Primary Metric — Refund Escalation Rate:**  
  $$\text{Escalation Rate} = \frac{\text{Monthly Escalations}}{\text{Total Refund Requests}} \times 100$$
  * *Baseline (June 2026):* **52.1%** (75 escalations on 144 requests)
  * *30-Day Target:* **≤ 8.0%** (≤ 12 escalations)
  * *60-Day Target:* **≤ 3.0%**
* **Secondary Metric — Reconciliation & Handoff Lag:**  
  * *Baseline:* **2.47 days average handoff lag** (total turnaround lag is **6.23 days**, with 69 tickets dropped)
  * *30-Day Target:* **< 15 minutes** (Real-time SSOT queue sync)
  * *Turnaround SLA:* Payout execution reduced from 25+ days to **≤ 48 hours**

---

## 💻 Prototype Architecture

* [`app.py`](app.py): Interactive Streamlit UI featuring Executive Ops Dashboard, Cross-Tracker Reconciler, and AI Omnichannel Intake Playground.
* [`reconciler.py`](reconciler.py): Core data processing engine performing fuzzy ID normalization, outer join reconciliation, and anomaly classification.
* [`ai_intake_agent.py`](ai_intake_agent.py): Natural language processing agent that ingests messy bilingual/Hinglish messages, scores urgency, and generates instant proactive replies.
* [`generate_pdf.py`](generate_pdf.py): Script generating the exact 3-page publication PDF using ReportLab.

