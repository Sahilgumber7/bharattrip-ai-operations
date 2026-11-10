"""
Generate the Official 3-Page Executive PDF Submission for BharatTrip AI Operations Associate Task.
Uses ReportLab with precise page constraints, professional styling, tables, and typography.
"""

import sys
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#718096"))
        
        # Header (pages 2 and 3)
        if self._pageNumber > 1:
            self.drawString(45, 11 * 72 - 32, "BharatTrip Refund Operations Strategy | AI Operations Screening")
            self.drawRightString(8.5 * 72 - 45, 11 * 72 - 32, "June 2026 Snapshot Audit")
            self.setStrokeColor(colors.HexColor("#E2E8F0"))
            self.setLineWidth(0.5)
            self.line(45, 11 * 72 - 36, 8.5 * 72 - 45, 11 * 72 - 36)
        
        # Footer (all pages)
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawString(45, 25, "Confidential — Prepared for BharatTrip Leadership")
        self.drawRightString(8.5 * 72 - 45, 25, page_str)
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.5)
        self.line(45, 33, 8.5 * 72 - 45, 33)
        self.restoreState()

def create_writeup_pdf(output_filename="BharatTrip_AI_Operations_WriteUp.pdf"):
    doc = SimpleDocTemplate(
        output_filename,
        pagesize=letter,
        leftMargin=40,
        rightMargin=40,
        topMargin=42,
        bottomMargin=42
    )

    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=colors.HexColor("#1A365D")
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor("#4A5568")
    )

    h1_style = ParagraphStyle(
        'SectionH1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11.5,
        leading=15,
        textColor=colors.HexColor("#1A365D"),
        spaceBefore=6,
        spaceAfter=3
    )

    h2_style = ParagraphStyle(
        'SectionH2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=12,
        textColor=colors.HexColor("#2B6CB0"),
        spaceBefore=4,
        spaceAfter=2
    )

    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.2,
        leading=11,
        textColor=colors.HexColor("#2D3748")
    )

    body_bold = ParagraphStyle(
        'BodyBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.2,
        leading=11,
        textColor=colors.HexColor("#1A202C")
    )

    bullet_style = ParagraphStyle(
        'BulletText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.0,
        leading=10.5,
        textColor=colors.HexColor("#2D3748"),
        leftIndent=12,
        spaceAfter=2
    )

    table_cell = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.5,
        leading=9.5,
        textColor=colors.HexColor("#2D3748")
    )

    table_header = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=9.5,
        textColor=colors.white
    )

    story = []

    # =========================================================================
    # PAGE 1: EXECUTIVE DIAGNOSIS & PROBLEM DEFINITION
    # =========================================================================
    story.append(Paragraph("BharatTrip Refund Operations: Diagnosis, Architecture & Measurement", title_style))
    story.append(Paragraph("<b>Role:</b> AI Operations Associate &nbsp;|&nbsp; <b>Scope:</b> Screening Take-Home Task &nbsp;|&nbsp; <b>Constraint:</b> Zero Headcount Addition", subtitle_style))
    story.append(Spacer(1, 4))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#2B6CB0"), spaceBefore=2, spaceAfter=6))

    story.append(Paragraph("1. Problem Definition: The Root Cause Behind the Escalation Surge", h1_style))
    story.append(Paragraph(
        "<b>The Symptom vs. Root Reality:</b> Leadership observed a critical escalation surge over May–June 2026 while overall refund intake volume remained flat (~145 requests/month). The standard organizational reflex is to assume an agent performance slump or understaffing. However, empirical analysis of the operational extract reveals that the escalation crisis is driven by <b>three decoupled structural failures</b> across systems, status semantics, and approval queues:",
        body_style
    ))
    story.append(Spacer(1, 3))

    story.append(Paragraph(
        "• <b>Disconnected Operational Silos & Asynchronous Trackers:</b> Support and Finance maintain separate, non-reconciled spreadsheets. Support agents mark tickets <i>'Closed'</i> the moment they respond to a travel agent or forward an email. However, <b>69 tickets logged by Support never reached Finance</b>. Travel agents are told their refund is 'done', while Finance has zero record of the request.",
        bullet_style
    ))
    story.append(Paragraph(
        "• <b>June Approval Choke-Point:</b> Finance approvals completely collapsed in June. Prior to June, pending payouts at month-end were zero. In June, <b>58 payouts stalled in <i>'Pending Payout'</i></b> (accounting for 47% of June Finance volume). Approver <i>N. Iyer</i> ceased sign-offs mid-June without a delegation failover, creating a silent queue freeze.",
        bullet_style
    ))
    story.append(Paragraph(
        "• <b>Omnichannel Shadow Leakage & Unlogged Ingestion:</b> Informal WhatsApp and email cancellation requests (e.g., <i>RF-1098</i> and <i>RF-1099</i>) were acknowledged verbally without issuing a canonical ticket ID or creating a record in either tracker. When agents chased two weeks later, Support had no reference, driving instant critical escalations.",
        bullet_style
    ))
    story.append(Paragraph(
        "• <b>Deduction Transparency & Amount Gaps:</b> Across matched completed payouts, 53 cases had a gap where requested amount exceeded paid amount. Standard cancellation deductions explain 556 of 571 matched payouts (including 50 of the 53 gap cases); only 3 cases (RF-1041, RF-1368, RF-1435) have true unexplained discrepancies (> INR 1). However, quoting gross figures without deduction breakdowns leads agents to perceive standard deductions as unexplained 'short payments'.",
        bullet_style
    ))
    story.append(Spacer(1, 4))

    # Metric Snapshot Table
    story.append(Paragraph("<b>Table 1: Macro Volume vs. Operational Friction Indicators (Feb – Jun 2026)</b>", h2_style))
    t1_data = [
        [Paragraph("<b>Month (2026)</b>", table_header), Paragraph("<b>Support Intake</b>", table_header), Paragraph("<b>Finance Intake</b>", table_header), Paragraph("<b>Completed Payouts</b>", table_header), Paragraph("<b>Pending Month-End</b>", table_header), Paragraph("<b>Escalations</b>", table_header), Paragraph("<b>Escalation %</b>", table_header)],
        [Paragraph("February", table_cell), Paragraph("150", table_cell), Paragraph("111", table_cell), Paragraph("105", table_cell), Paragraph("0", table_cell), Paragraph("2", table_cell), Paragraph("1.3%", table_cell)],
        [Paragraph("March", table_cell), Paragraph("146", table_cell), Paragraph("155", table_cell), Paragraph("148", table_cell), Paragraph("0", table_cell), Paragraph("23", table_cell), Paragraph("15.8%", table_cell)],
        [Paragraph("April", table_cell), Paragraph("145", table_cell), Paragraph("138", table_cell), Paragraph("134", table_cell), Paragraph("0", table_cell), Paragraph("25", table_cell), Paragraph("17.2%", table_cell)],
        [Paragraph("May", table_cell), Paragraph("147", table_cell), Paragraph("124", table_cell), Paragraph("115", table_cell), Paragraph("0", table_cell), Paragraph("30", table_cell), Paragraph("20.4%", table_cell)],
        [Paragraph("<b>June (Spike)</b>", table_cell), Paragraph("<b>144</b>", table_cell), Paragraph("<b>124</b>", table_cell), Paragraph("<b>60</b>", table_cell), Paragraph("<b>58</b>", table_cell), Paragraph("<b>75</b>", table_cell), Paragraph("<b>52.1%</b>", table_cell)]
    ]
    t1 = Table(t1_data, colWidths=[70, 75, 75, 80, 80, 65, 65])
    t1.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1A365D")),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E0")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor("#FFFFFF"), colors.HexColor("#F7FAFC")]),
        ('BACKGROUND', (0,5), (-1,5), colors.HexColor("#FFF5F5")), # Highlight June in light red
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t1)
    story.append(Spacer(1, 5))

    story.append(Paragraph("Key Diagnostic Takeaways", h2_style))
    story.append(Paragraph(
        "1. <b>Volume Invariance:</b> Monthly incoming refund volume is statistically constant (&mu; = 146.4, &sigma; = 2.2). Headcount is not undercapacity.<br/>"
        "2. <b>The June Payout Collapse:</b> Finance payouts completed dropped by 48% in June (60 vs 115 in May), leaving 58 refunds in limbo.<br/>"
        "3. <b>Escalation Composition:</b> Over 60% of escalations are driven solely by communication vacuums (<i>'chasing for update'</i>, <i>'no record in Finance'</i>). Eliminating information opacity resolves the majority of escalations without modifying operational staff.",
        body_style
    ))

    # =========================================================================
    # PAGE 2: DEEP-DIVE ANALYSIS & CROSS-TRACKER RECONCILIATION
    # =========================================================================
    story.append(PageBreak())
    story.append(Paragraph("2. Deep-Dive Analysis: Where the Systems Break Down", h1_style))
    story.append(Paragraph(
        "Reconciling the 755 Support rows, 689 Finance rows, and 155 Escalations with normalized identifiers reveals the precise anatomy of failure:",
        body_style
    ))
    story.append(Spacer(1, 3))

    # Reconciliation Breakdown Table
    story.append(Paragraph("<b>Table 2: Cross-Tracker Reconciliation Matrix & Failure Modes</b>", h2_style))
    t2_data = [
        [Paragraph("<b>Failure Category</b>", table_header), Paragraph("<b>Count</b>", table_header), Paragraph("<b>Root Operational Mechanism</b>", table_header), Paragraph("<b>Direct Impact on Escalations</b>", table_header)],
        [
            Paragraph("<b>Dropped Handoffs</b><br/>(Support Only)", table_cell),
            Paragraph("<b>69</b><br/>tickets", table_cell),
            Paragraph("Support marks ticket 'Closed' in their sheet upon intake/forwarding; no API or unified queue pushes it to Finance.", table_cell),
            Paragraph("32 escalations cite 'Ticket closed, Finance has no record' or 'Marked complete, nothing received'.", table_cell)
        ],
        [
            Paragraph("<b>Approval Choke</b><br/>(Finance Pending)", table_cell),
            Paragraph("<b>58</b><br/>tickets", table_cell),
            Paragraph("Approvals bottlenecked on N. Iyer (last sign-off June 13). No escalation or delegation rule exists for absences.", table_cell),
            Paragraph("37 escalations cite 'Agent chasing for status update, no response' after 2+ weeks of silence.", table_cell)
        ],
        [
            Paragraph("<b>Shadow Intake</b><br/>(Finance Only)", table_cell),
            Paragraph("<b>16</b><br/>tickets", table_cell),
            Paragraph("Refunds triggered via off-tracker finance emails/WhatsApp. Support has zero visibility, causing confusion if queried.", table_cell),
            Paragraph("Support quotes incorrect status or tells agent no request exists.", table_cell)
        ],
        [
            Paragraph("<b>Amount Gaps & Deductions</b><br/>(Gross vs Net)", table_cell),
            Paragraph("<b>53 gaps</b><br/>(3 unexpl.)", table_cell),
            Paragraph("53 completed payouts have gaps; deductions explain 50 of them (and 556 of 571 matched payouts overall). Only 3 are unexplained.", table_cell),
            Paragraph("Escalations complain of 'Short payment' or 'Received less than promised' due to lack of deduction visibility.", table_cell)
        ],
        [
            Paragraph("<b>Data Hygiene Deficit</b><br/>(Syntax & Duplication)", table_cell),
            Paragraph("<b>22 rows</b><br/>in Support", table_cell),
            Paragraph("12 exact duplicates plus 10 conflicting IDs in Support (9 duplicates in Finance). Whitespace ('Closed ') and syntax drift ('RF 1079' vs 'RF-1079').", table_cell),
            Paragraph("Agents get double-billed or lost in lookups; metrics are obscured.", table_cell)
        ]
    ]
    t2 = Table(t2_data, colWidths=[85, 45, 175, 175])
    t2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1A365D")),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E0")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor("#FFFFFF"), colors.HexColor("#F7FAFC")]),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t2)
    story.append(Spacer(1, 4))

    story.append(Paragraph("Validation of Unlogged Shadow Cases from Brief", h2_style))
    story.append(Paragraph(
        "• <b>Nomad Travel (BLR-MAA):</b> Raised on WhatsApp June 8 (<i>'Bhai refund ka kya hua? BLR-MAA wala. 2 hafte ho gaye'</i>). Present in Escalations as <b>ESC-592</b> referencing <b>RF-1098</b>. Both <i>Support_Tracker</i> and <i>Finance_Tracker</i> have <b>zero record</b> of RF-1098. The request evaporated in WhatsApp.<br/>"
        "• <b>Peak Journeys (DEL-DXB):</b> Emailed June 5 (<i>'I cancelled booking for DEL-DXB last week... no reference number'</i>). Logged in Escalations as <b>ESC-587</b> referencing <b>RF-1099</b>. Again, completely missing from both operational sheets.<br/>"
        "• <b>Internal Support Confession (June 11):</b> <i>'Finance says they never received several refunds I closed last month'</i>. Confirmed quantitatively: 69 tickets marked 'Closed' by Support are absent from Finance.",
        body_style
    ))
    story.append(Spacer(1, 4))

    story.append(Paragraph("What Would Be Validated With Additional Time & System Access", h2_style))
    story.append(Paragraph(
        "1. <b>GDS/Airline API Logs:</b> Determine whether airline cancellation credits were received by BharatTrip earlier, indicating Finance is sitting on settled airline funds.<br/>"
        "2. <b>WhatsApp & Shared Email Inboxes:</b> Audit unlogged inbound messages across support channels to measure true shadow demand volume.<br/>"
        "3. <b>Finance Sign-Off Authority Rules:</b> Clarify if sign-offs require N. Iyer due to statutory audit thresholds or if peer managers had delegation authority.",
        body_style
    ))

    # =========================================================================
    # PAGE 3: SOLUTION DESIGN, PROTOTYPE & MEASUREMENT
    # =========================================================================
    story.append(PageBreak())
    story.append(Paragraph("3. Target Solution: Unified Lifecycle Architecture (Zero-Headcount)", h1_style))
    story.append(Paragraph(
        "BharatTrip must transition from disjointed sheets to an <b>Event-Driven Single Source of Truth (SSOT)</b> with a deterministic state-machine and automated communication webhooks:",
        body_style
    ))
    story.append(Spacer(1, 2))

    story.append(Paragraph(
        "<b>State-Machine:</b> <code>1. INTAKE_CAPTURED</code> (Canonical RF-ID auto-issued) &rarr; <code>2. ELIGIBILITY_VERIFIED</code> (Auto-deduction calculated) &rarr; <code>3. FINANCE_QUEUED</code> &rarr; <code>4. PAYOUT_APPROVED</code> (Auto-batch &le; INR 25,000) &rarr; <code>5. SETTLED / DECLINED</code> (Instant agent webhook).",
        body_style
    ))
    story.append(Spacer(1, 2))

    # Trade-off table
    story.append(Paragraph("<b>Table 3: Operational Trade-Off Matrix Under Zero-Headcount Constraint</b>", h2_style))
    t3_data = [
        [Paragraph("<b>Component</b>", table_header), Paragraph("<b>Implementation</b>", table_header), Paragraph("<b>Operational Rationale & Safeguard</b>", table_header)],
        [
            Paragraph("Omnichannel Intake", table_cell),
            Paragraph("<b>Automate (Rule-Based Parser)</b>", table_cell),
            Paragraph("Extracts PNR, sector, agent from WhatsApp/Email, assigns canonical RF-NEW ID, auto-responds with acknowledgement. Prevents unlogged loss (RF-1098).", table_cell)
        ],
        [
            Paragraph("Deduction Engine", table_cell),
            Paragraph("<b>Automate (Rules Engine)</b>", table_cell),
            Paragraph("Calculates airline cancellation charges + service fee upfront. Sends itemized deduction slip, eliminating amount disputes.", table_cell)
        ],
        [
            Paragraph("Routine Approvals", table_cell),
            Paragraph("<b>Automated Batch (&le;INR 25k)</b>", table_cell),
            Paragraph("Tickets within standard cancellation window auto-approved for payment. Removes single-manager dependency (N. Iyer bottleneck).", table_cell)
        ],
        [
            Paragraph("Disputed Refunds", table_cell),
            Paragraph("<b>Manual (Finance Lead)</b>", table_cell),
            Paragraph("High-value (&gt;INR 25k) or non-refundable fare waiver requests require human scrutiny to protect cash margins.", table_cell)
        ],
        [
            Paragraph("Key Partner Relations", table_cell),
            Paragraph("<b>Manual (Senior Support)</b>", table_cell),
            Paragraph("High-tier travel agencies receive direct human outreach on exceptions while routine tickets flow through zero-touch pipeline.", table_cell)
        ]
    ]
    t3 = Table(t3_data, colWidths=[90, 105, 285])
    t3.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1A365D")),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E0")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor("#FFFFFF"), colors.HexColor("#F7FAFC")]),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
    ]))
    story.append(t3)
    story.append(Spacer(1, 4))

    story.append(Paragraph("4. Built AI Prototype: Scope & Judgement Justification", h1_style))
    story.append(Paragraph(
        "<b>Slice Selected:</b> An end-to-end <b>AI Refund Operations Copilot & Auto-Reconciler</b> combining: (1) A deterministic, rule-based Omnichannel Intake Agent that parses messy bilingual/Hinglish WhatsApp & email messages, extracts route sectors, scores escalation risk, issues stable unique reference IDs (<code>RF-NEW-&lt;HEX&gt;</code>), and drafts safe acknowledgement responses without premature payout commitments; (2) An automated cross-tracker reconciliation engine that flags dropped handoffs and approval stalls; and (3) An interactive Streamlit and HTML dashboard.<br/>"
        "<b>Judgement:</b> Building a generic chatbot would fail because the problem is structural. This prototype attacks the two primary escalation sources: unlogged shadow requests and tracker divergence.",
        body_style
    ))
    story.append(Spacer(1, 4))

    story.append(Paragraph("5. Measurement Framework & 30-Day Operational Scorecard", h1_style))
    story.append(Paragraph(
        "To verify that the process is functioning without adding staff, leadership should track two core metrics:",
        body_style
    ))
    story.append(Spacer(1, 2))

    story.append(Paragraph(
        "• <b>Primary Metric — Refund Escalation Rate (%):</b> <code>(Monthly Escalations / Total Refund Requests) &times; 100</code>.<br/>"
        "&nbsp;&nbsp;&bull; <i>Baseline (June 2026):</i> <b>52.1%</b> (75 escalations on 144 requests).<br/>"
        "&nbsp;&nbsp;&bull; <i>30-Day Target:</i> <b>&le; 8.0%</b> (&le;12 escalations). <i>60-Day Target:</i> <b>&le; 3.0%</b>.<br/>"
        "• <b>Secondary Metric — Cross-Team Handoff & Processing SLA:</b> Time from refund intake to payout execution.<br/>"
        "&nbsp;&nbsp;&bull; <i>Baseline:</i> Average handoff lag is <b>2.47 days</b>, and total turnaround lag is <b>6.23 days</b> (with 69 tickets dropped and 58 pending payouts aging 25+ days).<br/>"
        "&nbsp;&nbsp;&bull; <i>30-Day Target:</i> Handoff lag <b>&lt; 15 minutes</b> (real-time SSOT sync); End-to-end payout turnaround <b>&le; 48 hours</b>.",
        body_style
    ))
    story.append(Spacer(1, 3))

    story.append(Paragraph("Explicit Operational Assumptions", h2_style))
    story.append(Paragraph(
        "1. Standard cancellation policies carry fixed fee schedules allowing automated deduction calculation for &gt;80% of routine domestic bookings.<br/>"
        "2. Travel agents accept WhatsApp/Email automated confirmations provided a valid tracking ID and clear acknowledgment are supplied.<br/>"
        "3. Finance can execute batch payouts based on system-validated rules without manual per-item executive re-authorization.",
        body_style
    ))

    # Build document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated {output_filename}")

if __name__ == "__main__":
    create_writeup_pdf()
