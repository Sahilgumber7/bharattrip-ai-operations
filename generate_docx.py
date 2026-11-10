"""
Generate editable Microsoft Word document (.docx) of the BharatTrip Write-Up.
"""

import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, hex_color):
    tcPr = cell._element.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=80, bottom=80, left=120, right=120):
    tcPr = cell._element.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def create_docx(filename="BharatTrip_AI_Operations_WriteUp.docx"):
    doc = docx.Document()

    # Set 0.6 inch margins
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(0.6)
        section.bottom_margin = Inches(0.6)
        section.left_margin = Inches(0.6)
        section.right_margin = Inches(0.6)

    # Styles
    navy = RGBColor(26, 54, 93)      # #1A365D
    slate_dark = RGBColor(45, 55, 72) # #2D3748
    blue_accent = RGBColor(43, 108, 176) # #2B6CB0

    # Title
    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_after = Pt(2)
    run_title = p_title.add_run("BharatTrip Refund Operations: Diagnosis, Architecture & Measurement")
    run_title.font.name = "Arial"
    run_title.font.size = Pt(16)
    run_title.font.bold = True
    run_title.font.color.rgb = navy

    # Subtitle / Metadata
    p_sub = doc.add_paragraph()
    p_sub.paragraph_format.space_after = Pt(8)
    run_sub = p_sub.add_run("Role: AI Operations Associate  |  Scope: Screening Take-Home Task  |  Constraint: Zero Headcount Addition")
    run_sub.font.name = "Arial"
    run_sub.font.size = Pt(9)
    run_sub.font.color.rgb = RGBColor(113, 128, 150)

    # Helper for Headings
    def add_h1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(3)
        run = p.add_run(text)
        run.font.name = "Arial"
        run.font.size = Pt(11.5)
        run.font.bold = True
        run.font.color.rgb = navy
        return p

    def add_h2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(6)
        p.paragraph_format.space_after = Pt(2)
        run = p.add_run(text)
        run.font.name = "Arial"
        run.font.size = Pt(10)
        run.font.bold = True
        run.font.color.rgb = blue_accent
        return p

    def add_body(text, bold_prefix=""):
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.15
        if bold_prefix:
            r_b = p.add_run(bold_prefix)
            r_b.font.name = "Arial"
            r_b.font.size = Pt(9)
            r_b.font.bold = True
            r_b.font.color.rgb = slate_dark
        r = p.add_run(text)
        r.font.name = "Arial"
        r.font.size = Pt(9)
        r.font.color.rgb = slate_dark
        return p

    def add_bullet(bold_prefix, text):
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_after = Pt(2.5)
        p.paragraph_format.line_spacing = 1.15
        r_b = p.add_run(bold_prefix + " ")
        r_b.font.name = "Arial"
        r_b.font.size = Pt(9)
        r_b.font.bold = True
        r_b.font.color.rgb = slate_dark
        r = p.add_run(text)
        r.font.name = "Arial"
        r.font.size = Pt(9)
        r.font.color.rgb = slate_dark
        return p

    # --- SECTION 1 ---
    add_h1("1. Problem Definition: The Root Cause Behind the Escalation Surge")
    add_body(
        "Leadership observed customer and agent escalations climbing over May–June 2026 while overall refund intake volume remained flat (~145 requests/month). The standard organizational reflex is to assume agent underperformance or understaffing. However, empirical analysis of the operational extract reveals that the escalation crisis is driven by three decoupled structural failures across systems, status semantics, and approval queues:",
        bold_prefix="The Symptom vs. Root Reality: "
    )

    add_bullet("Disconnected Operational Silos & Asynchronous Trackers:", "Support and Finance maintain separate, non-reconciled spreadsheets. Support agents mark tickets 'Closed' the moment they respond to a travel agent or forward an email. However, 69 tickets logged by Support never reached Finance. Travel agents are told their refund is 'done', while Finance has zero record of the request.")
    add_bullet("June Approval Choke-Point:", "Finance approvals completely collapsed in June. Prior to June, pending payouts at month-end were zero. In June, 58 payouts stalled in 'Pending Payout' (accounting for 47% of June Finance volume). Approver N. Iyer ceased sign-offs mid-June without a delegation failover, creating a silent queue freeze.")
    add_bullet("Omnichannel Shadow Leakage & Unlogged Ingestion:", "Informal WhatsApp and email cancellation requests (e.g., RF-1098 and RF-1099) were acknowledged verbally without issuing a canonical ticket ID or creating a record in either tracker. When agents chased two weeks later, Support had no reference, driving instant critical escalations.")
    add_bullet("Deduction Transparency & Amount Gaps:", "Across matched completed payouts, 53 cases had a gap where requested amount exceeded paid amount. Standard cancellation deductions explain 556 of 571 matched payouts (including 50 of the 53 gap cases); only 3 cases (RF-1041, RF-1368, RF-1435) have true unexplained discrepancies (> INR 1). However, quoting gross figures without deduction breakdowns leads agents to perceive standard deductions as unexplained 'short payments'.")

    # Table 1
    add_h2("Table 1: Macro Volume vs. Operational Friction Indicators (Feb – Jun 2026)")
    t1_data = [
        ["Month (2026)", "Support Intake", "Finance Intake", "Completed Payouts", "Pending Month-End", "Escalations", "Escalation %"],
        ["February", "150", "111", "105", "0", "2", "1.3%"],
        ["March", "146", "155", "148", "0", "23", "15.8%"],
        ["April", "145", "138", "134", "0", "25", "17.2%"],
        ["May", "147", "124", "115", "0", "30", "20.4%"],
        ["June (Spike)", "144", "124", "60", "58", "75", "52.1%"]
    ]
    t1 = doc.add_table(rows=len(t1_data), cols=len(t1_data[0]))
    t1.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, row in enumerate(t1_data):
        for j, val in enumerate(row):
            cell = t1.cell(i, j)
            cell.text = val
            set_cell_margins(cell, 60, 60, 80, 80)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.runs[0].font.name = "Arial"
            p.runs[0].font.size = Pt(8)
            if i == 0:
                set_cell_background(cell, "1A365D")
                p.runs[0].font.bold = True
                p.runs[0].font.color.rgb = RGBColor(255, 255, 255)
            elif i == 5:
                set_cell_background(cell, "FFF5F5")
                p.runs[0].font.bold = True
                p.runs[0].font.color.rgb = RGBColor(153, 27, 27)
            else:
                if i % 2 == 1:
                    set_cell_background(cell, "FFFFFF")
                else:
                    set_cell_background(cell, "F7FAFC")
                p.runs[0].font.color.rgb = slate_dark

    add_h2("Key Diagnostic Takeaways")
    add_bullet("1. Volume Invariance:", "Monthly incoming refund volume is statistically constant (μ = 146.4, σ = 2.2). Headcount is not undercapacity.")
    add_bullet("2. The June Payout Collapse:", "Finance payouts completed dropped by 48% in June (60 vs 115 in May), leaving 58 refunds in limbo.")
    add_bullet("3. Escalation Composition:", "Over 60% of escalations are driven solely by communication vacuums ('chasing for update', 'no record in Finance'). Eliminating information opacity resolves the majority of escalations without modifying operational staff.")

    doc.add_page_break()

    # --- SECTION 2 ---
    add_h1("2. Deep-Dive Analysis: Where the Systems Break Down")
    add_body("Reconciling the 755 Support rows, 689 Finance rows, and 155 Escalations with normalized identifiers reveals the precise anatomy of failure:")

    add_h2("Table 2: Cross-Tracker Reconciliation Matrix & Failure Modes")
    t2_data = [
        ["Failure Category", "Count", "Root Operational Mechanism", "Direct Impact on Escalations"],
        ["Dropped Handoffs\n(Support Only)", "69\ntickets", "Support marks ticket 'Closed' in their sheet upon intake/forwarding; no API or unified queue pushes it to Finance.", "32 escalations cite 'Ticket closed, Finance has no record' or 'Marked complete, nothing received'."],
        ["Approval Choke\n(Finance Pending)", "58\ntickets", "Approvals bottlenecked on N. Iyer (last sign-off June 13). No escalation or delegation rule exists for absences.", "37 escalations cite 'Agent chasing for status update, no response' after 2+ weeks of silence."],
        ["Shadow Intake\n(Finance Only)", "16\ntickets", "Refunds triggered via off-tracker finance emails/WhatsApp. Support has zero visibility, causing confusion if queried.", "Support quotes incorrect status or tells agent no request exists."],
        ["Amount Gaps & Deductions\n(Gross vs Net)", "53 gaps\n(3 unexpl.)", "53 completed payouts have gaps; deductions explain 50 of them (and 556 of 571 matched payouts overall). Only 3 are unexplained.", "Escalations complain of 'Short payment' or 'Received less than promised' due to lack of deduction visibility."],
        ["Data Hygiene Deficit\n(Syntax & Duplication)", "22 rows\nin Support", "12 exact duplicates plus 10 conflicting IDs in Support (9 duplicates in Finance). Whitespace ('Closed ') and syntax drift ('RF 1079' vs 'RF-1079').", "Agents get double-billed or lost in lookups; metrics are obscured."]
    ]
    t2 = doc.add_table(rows=len(t2_data), cols=len(t2_data[0]))
    t2.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, row in enumerate(t2_data):
        for j, val in enumerate(row):
            cell = t2.cell(i, j)
            cell.text = val
            set_cell_margins(cell, 60, 60, 80, 80)
            p = cell.paragraphs[0]
            p.runs[0].font.name = "Arial"
            p.runs[0].font.size = Pt(8)
            if i == 0:
                set_cell_background(cell, "1A365D")
                p.runs[0].font.bold = True
                p.runs[0].font.color.rgb = RGBColor(255, 255, 255)
            else:
                if i % 2 == 1:
                    set_cell_background(cell, "FFFFFF")
                else:
                    set_cell_background(cell, "F7FAFC")
                p.runs[0].font.color.rgb = slate_dark
                if j == 0:
                    p.runs[0].font.bold = True

    add_h2("Validation of Unlogged Shadow Cases from Brief")
    add_bullet("• Nomad Travel (BLR-MAA):", "Raised on WhatsApp June 8 ('Bhai refund ka kya hua? BLR-MAA wala. 2 hafte ho gaye'). Present in Escalations as ESC-592 referencing RF-1098. Both Support_Tracker and Finance_Tracker have zero record of RF-1098. The request evaporated in WhatsApp.")
    add_bullet("• Peak Journeys (DEL-DXB):", "Emailed June 5 ('I cancelled booking for DEL-DXB last week... no reference number'). Logged in Escalations as ESC-587 referencing RF-1099. Again, completely missing from both operational sheets.")
    add_bullet("• Internal Support Confession (June 11):", "'Finance says they never received several refunds I closed last month'. Confirmed quantitatively: 69 tickets marked 'Closed' by Support are absent from Finance.")

    add_h2("What Would Be Validated With Additional Time & System Access")
    add_bullet("1. GDS/Airline API Logs:", "Determine whether airline cancellation credits were received by BharatTrip earlier, indicating Finance is sitting on settled airline funds.")
    add_bullet("2. WhatsApp & Shared Email Inboxes:", "Audit unlogged inbound messages across support channels to measure true shadow demand volume.")
    add_bullet("3. Finance Sign-Off Authority Rules:", "Clarify if sign-offs require N. Iyer due to statutory audit thresholds or if peer managers had delegation authority.")

    doc.add_page_break()

    # --- SECTION 3 ---
    add_h1("3. Target Solution: Unified Lifecycle Architecture (Zero-Headcount)")
    add_body("BharatTrip must transition from disjointed sheets to an Event-Driven Single Source of Truth (SSOT) with a deterministic state-machine and automated communication webhooks:")
    add_body("1. INTAKE_CAPTURED (Canonical RF-ID auto-issued) → 2. ELIGIBILITY_VERIFIED (Auto-deduction calculated) → 3. FINANCE_QUEUED → 4. PAYOUT_APPROVED (Auto-batch ≤ INR 25,000) → 5. SETTLED / DECLINED (Instant agent webhook).", bold_prefix="State-Machine: ")

    add_h2("Table 3: Operational Trade-Off Matrix Under Zero-Headcount Constraint")
    t3_data = [
        ["Component", "Implementation", "Operational Rationale & Safeguard"],
        ["Omnichannel Intake", "Automate (Rule-Based Parser)", "Extracts PNR, sector, agent from WhatsApp/Email, assigns canonical RF-NEW ID, auto-responds with acknowledgement. Prevents unlogged loss (RF-1098)."],
        ["Deduction Engine", "Automate (Rules Engine)", "Calculates airline cancellation charges + service fee upfront. Sends itemized deduction slip, eliminating amount disputes."],
        ["Routine Approvals", "Automated Batch (≤ INR 25k)", "Tickets within standard cancellation window auto-approved for payment. Removes single-manager dependency (N. Iyer bottleneck)."],
        ["Disputed Refunds", "Manual (Finance Lead)", "High-value (> INR 25k) or non-refundable fare waiver requests require human scrutiny to protect cash margins."],
        ["Key Partner Relations", "Manual (Senior Support)", "High-tier travel agencies receive direct human outreach on exceptions while routine tickets flow through zero-touch pipeline."]
    ]
    t3 = doc.add_table(rows=len(t3_data), cols=len(t3_data[0]))
    t3.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, row in enumerate(t3_data):
        for j, val in enumerate(row):
            cell = t3.cell(i, j)
            cell.text = val
            set_cell_margins(cell, 60, 60, 80, 80)
            p = cell.paragraphs[0]
            p.runs[0].font.name = "Arial"
            p.runs[0].font.size = Pt(8)
            if i == 0:
                set_cell_background(cell, "1A365D")
                p.runs[0].font.bold = True
                p.runs[0].font.color.rgb = RGBColor(255, 255, 255)
            else:
                if i % 2 == 1:
                    set_cell_background(cell, "FFFFFF")
                else:
                    set_cell_background(cell, "F7FAFC")
                p.runs[0].font.color.rgb = slate_dark
                if j == 0:
                    p.runs[0].font.bold = True

    add_h1("4. Built AI Prototype: Scope & Judgement Justification")
    add_body("An end-to-end AI Refund Operations Copilot & Auto-Reconciler combining: (1) A deterministic, rule-based Omnichannel Intake Agent that parses messy bilingual/Hinglish WhatsApp & email messages, extracts route sectors, scores escalation risk, issues stable unique reference IDs (RF-NEW-<HEX>), and drafts safe acknowledgement responses without premature payout commitments; (2) An automated cross-tracker reconciliation engine that flags dropped handoffs and approval stalls; and (3) An interactive Streamlit and HTML dashboard.", bold_prefix="Slice Selected: ")
    add_body("Building a generic chatbot would fail because the problem is structural. This prototype attacks the two primary escalation sources: unlogged shadow requests and tracker divergence.", bold_prefix="Judgement: ")

    add_h1("5. Measurement Framework & 30-Day Operational Scorecard")
    add_body("To verify that the process is functioning without adding staff, leadership should track two core metrics:")
    add_bullet("• Primary Metric — Refund Escalation Rate (%):", "(Monthly Escalations / Total Refund Requests) × 100. Baseline (June 2026): 52.1% (75 escalations on 144 requests). 30-Day Target: ≤ 8.0% (≤ 12 escalations). 60-Day Target: ≤ 3.0%.")
    add_bullet("• Secondary Metric — Cross-Team Handoff & Processing SLA:", "Time from refund intake to payout execution. Baseline: Average handoff lag is 2.47 days, and total end-to-end turnaround lag is 6.23 days (with 69 tickets dropped and 58 pending payouts aging 25+ days). 30-Day Target: Handoff lag < 15 minutes (real-time SSOT sync); End-to-end payout turnaround ≤ 48 hours.")

    add_h2("Explicit Operational Assumptions")
    add_bullet("1.", "Standard cancellation policies carry fixed fee schedules allowing automated deduction calculation for >80% of routine domestic bookings.")
    add_bullet("2.", "Travel agents accept WhatsApp/Email automated confirmations provided a valid tracking ID and clear acknowledgment are supplied.")
    add_bullet("3.", "Finance can execute batch payouts based on system-validated rules without manual per-item executive re-authorization.")

    doc.save(filename)
    print(f"Successfully generated {filename}")

if __name__ == "__main__":
    create_docx()

