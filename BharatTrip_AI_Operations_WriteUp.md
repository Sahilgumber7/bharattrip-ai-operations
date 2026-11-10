# BharatTrip Refund Operations: Diagnosis, Architecture & Measurement

**Role:** AI Operations Associate  
**Scope:** Screening Take-Home Task  
**Constraint:** Zero Headcount Addition  

---

## 1. Problem Definition: The Root Cause Behind the Escalation Surge

**The Symptom vs. Root Reality:** Leadership observed customer and agent escalations climbing over May–June 2026 while overall refund intake volume remained flat (~145 requests/month). The standard organizational reflex is to assume agent underperformance or understaffing. However, empirical analysis of the operational extract reveals that the escalation crisis is driven by three decoupled structural failures across systems, status semantics, and approval queues:

* **Disconnected Operational Silos & Asynchronous Trackers:** Support and Finance maintain separate, non-reconciled spreadsheets. Support agents mark tickets *'Closed'* the moment they respond to a travel agent or forward an email. However, **69 tickets logged by Support never reached Finance**. Travel agents are told their refund is 'done', while Finance has zero record of the request.
* **June Approval Choke-Point:** Finance approvals completely collapsed in June. Prior to June, pending payouts at month-end were zero. In June, **58 payouts stalled in *'Pending Payout'*** (accounting for 47% of June Finance volume). Approver *N. Iyer* ceased sign-offs mid-June without a delegation failover, creating a silent queue freeze.
* **Omnichannel Shadow Leakage & Unlogged Ingestion:** Informal WhatsApp and email cancellation requests (e.g., *RF-1098* and *RF-1099*) were acknowledged verbally without issuing a canonical ticket ID or creating a record in either tracker. When agents chased two weeks later, Support had no reference, driving instant critical escalations.
* **Deduction Transparency & Amount Gaps:** Across matched completed payouts, 53 cases had a gap where requested amount exceeded paid amount. Standard cancellation deductions explain 556 of 571 matched payouts (including 50 of the 53 gap cases); only 3 cases (RF-1041, RF-1368, RF-1435) have true unexplained discrepancies (> INR 1). However, because Support quotes gross booking figures without deduction visibility, agents perceive standard deductions as unexplained 'short payments'.

### Table 1: Macro Volume vs. Operational Friction Indicators (Feb – Jun 2026)

| Month (2026) | Support Intake | Finance Intake | Completed Payouts | Pending Month-End | Escalations | Escalation % |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| February | 150 | 111 | 105 | 0 | 2 | 1.3% |
| March | 146 | 155 | 148 | 0 | 23 | 15.8% |
| April | 145 | 138 | 134 | 0 | 25 | 17.2% |
| May | 147 | 124 | 115 | 0 | 30 | 20.4% |
| **June (Spike)** | **144** | **124** | **60** | **58** | **75** | **52.1%** |

### Key Diagnostic Takeaways
1. **Volume Invariance:** Monthly incoming refund volume is statistically constant ($\mu = 146.4$, $\sigma = 2.2$). Headcount is not undercapacity.
2. **The June Payout Collapse:** Finance payouts completed dropped by 48% in June (60 vs 115 in May), leaving 58 refunds in limbo.
3. **Escalation Composition:** Over 60% of escalations are driven solely by communication vacuums (*'chasing for update'*, *'no record in Finance'*). Eliminating information opacity resolves the majority of escalations without modifying operational staff.

---

## 2. Deep-Dive Analysis: Where the Systems Break Down

Reconciling the 755 Support rows, 689 Finance rows, and 155 Escalations with normalized identifiers reveals the precise anatomy of failure:

### Table 2: Cross-Tracker Reconciliation Matrix & Failure Modes

| Failure Category | Count | Root Operational Mechanism | Direct Impact on Escalations |
| :--- | :---: | :--- | :--- |
| **Dropped Handoffs**<br/>(Support Only) | **69**<br/>tickets | Support marks ticket 'Closed' in their sheet upon intake/forwarding; no API or unified queue pushes it to Finance. | 32 escalations cite 'Ticket closed, Finance has no record' or 'Marked complete, nothing received'. |
| **Approval Choke**<br/>(Finance Pending) | **58**<br/>tickets | Approvals bottlenecked on N. Iyer (last sign-off June 13). No escalation or delegation rule exists for absences. | 37 escalations cite 'Agent chasing for status update, no response' after 2+ weeks of silence. |
| **Shadow Intake**<br/>(Finance Only) | **16**<br/>tickets | Refunds triggered via off-tracker finance emails/WhatsApp. Support has zero visibility, causing confusion if queried. | Support quotes incorrect status or tells agent no request exists. |
| **Amount Gaps & Deductions**<br/>(Gross vs Net) | **53 gaps**<br/>(3 unexpl.) | 53 completed payouts have gaps; deductions explain 50 of them (and 556 of 571 matched payouts overall). Only 3 are unexplained. | Escalations complain of 'Short payment' or 'Received less than promised' due to lack of deduction visibility. |
| **Data Hygiene Deficit**<br/>(Syntax & Duplication) | **22 rows**<br/>in Support | 12 exact duplicates plus 10 conflicting IDs in Support (9 duplicates in Finance). Whitespace ('Closed ') and syntax drift ('RF 1079' vs 'RF-1079'). | Agents get double-billed or lost in lookups; metrics are obscured. |

### Validation of Unlogged Shadow Cases from Brief
* **Nomad Travel (BLR-MAA):** Raised on WhatsApp June 8 (*'Bhai refund ka kya hua? BLR-MAA wala. 2 hafte ho gaye'*). Present in Escalations as **ESC-592** referencing **RF-1098**. Both *Support_Tracker* and *Finance_Tracker* have **zero record** of RF-1098. The request evaporated in WhatsApp.
* **Peak Journeys (DEL-DXB):** Emailed June 5 (*'I cancelled booking for DEL-DXB last week... no reference number'*). Logged in Escalations as **ESC-587** referencing **RF-1099**. Again, completely missing from both operational sheets.
* **Internal Support Confession (June 11):** *'Finance says they never received several refunds I closed last month'*. Confirmed quantitatively: 69 tickets marked 'Closed' by Support are absent from Finance.

### What Would Be Validated With Additional Time & System Access
1. **GDS/Airline API Logs:** Determine whether airline cancellation credits were received by BharatTrip earlier, indicating Finance is sitting on settled airline funds.
2. **WhatsApp & Shared Email Inboxes:** Audit unlogged inbound messages across support channels to measure true shadow demand volume.
3. **Finance Sign-Off Authority Rules:** Clarify if sign-offs require N. Iyer due to statutory audit thresholds or if peer managers had delegation authority.

---

## 3. Target Solution: Unified Lifecycle Architecture (Zero-Headcount)

BharatTrip must transition from disjointed sheets to an **Event-Driven Single Source of Truth (SSOT)** with a deterministic state-machine and automated communication webhooks:

**State-Machine:**  
`1. INTAKE_CAPTURED` (Canonical RF-ID auto-issued) $\rightarrow$ `2. ELIGIBILITY_VERIFIED` (Auto-deduction calculated) $\rightarrow$ `3. FINANCE_QUEUED` $\rightarrow$ `4. PAYOUT_APPROVED` (Auto-batch $\le$ INR 25,000) $\rightarrow$ `5. SETTLED / DECLINED` (Instant agent webhook).

### Table 3: Operational Trade-Off Matrix Under Zero-Headcount Constraint

| Component | Implementation | Operational Rationale & Safeguard |
| :--- | :--- | :--- |
| **Omnichannel Intake** | **Automate (Rule-Based Parser)** | Extracts PNR, sector, agent from WhatsApp/Email, assigns canonical RF-NEW ID, auto-responds with acknowledgement. Prevents unlogged loss (RF-1098). |
| **Deduction Engine** | **Automate (Rules Engine)** | Calculates airline cancellation charges + service fee upfront. Sends itemized deduction slip, eliminating amount disputes. |
| **Routine Approvals** | **Automated Batch (&le; INR 25k)** | Tickets within standard cancellation window auto-approved for payment. Removes single-manager dependency (N. Iyer bottleneck). |
| **Disputed Refunds** | **Manual (Finance Lead)** | High-value (> INR 25k) or non-refundable fare waiver requests require human scrutiny to protect cash margins. |
| **Key Partner Relations** | **Manual (Senior Support)** | High-tier travel agencies receive direct human outreach on exceptions while routine tickets flow through zero-touch pipeline. |

---

## 4. Built AI Prototype: Scope & Judgement Justification

**Slice Selected:** An end-to-end **AI Refund Operations Copilot & Auto-Reconciler** combining: (1) A deterministic, rule-based Omnichannel Intake Agent that parses messy bilingual/Hinglish WhatsApp & email messages, extracts route sectors, scores escalation risk, issues stable unique reference IDs (`RF-NEW-<HEX>`), and drafts safe acknowledgement responses without premature payout commitments; (2) An automated cross-tracker reconciliation engine that flags dropped handoffs and approval stalls; and (3) An interactive Streamlit and HTML dashboard.  
**Judgement:** Building a generic chatbot would fail because the problem is structural. This prototype attacks the two primary escalation sources: unlogged shadow requests and tracker divergence.

---

## 5. Measurement Framework & 30-Day Operational Scorecard

To verify that the process is functioning without adding staff, leadership should track two core metrics:

* **Primary Metric — Refund Escalation Rate (%):**  
  $$\text{Escalation Rate} = \frac{\text{Monthly Escalations}}{\text{Total Refund Requests}} \times 100$$
  * *Baseline (June 2026):* **52.1%** (75 escalations on 144 requests).
  * *30-Day Target:* **$\le$ 8.0%** ($\le$ 12 escalations). *60-Day Target:* **$\le$ 3.0%**.
* **Secondary Metric — Cross-Team Handoff & Processing SLA:** Time from refund intake to payout execution.
  * *Baseline:* Average handoff lag is **2.47 days**, and total end-to-end turnaround lag is **6.23 days** (with 69 tickets dropped and 58 pending payouts aging 25+ days).
  * *30-Day Target:* Handoff lag **< 15 minutes** (real-time SSOT sync); End-to-end payout turnaround **$\le$ 48 hours**.

### Explicit Operational Assumptions
1. Standard cancellation policies carry fixed fee schedules allowing automated deduction calculation for >80% of routine domestic bookings.
2. Travel agents accept WhatsApp/Email automated confirmations provided a valid tracking ID and clear acknowledgment are supplied.
3. Finance can execute batch payouts based on system-validated rules without manual per-item executive re-authorization.

