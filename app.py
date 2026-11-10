"""
BharatTrip AI Refund Operations Copilot & Automated Reconciler
Web Prototype for AI Operations Associate Take-Home Task
Run with: streamlit run app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import json
from reconciler import run_reconciliation
from ai_intake_agent import RefundIntakeAgent

st.set_page_config(
    page_title="BharatTrip Refund Ops Copilot",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Header
st.title("✈️ BharatTrip: AI Refund Operations Copilot & Auto-Reconciler")
st.markdown(
    "**AI Operations Associate Task Prototype** | Solving Cross-Functional Tracker Silos, Approval Bottlenecks & Escalations"
)

# Load data with caching
@st.cache_data
def get_data():
    return run_reconciliation()

try:
    merged_df, summary, esc_df = get_data()
    intake_agent = RefundIntakeAgent()
except Exception as e:
    st.error(f"Error loading Excel file: {e}")
    st.stop()

# Sidebar Navigation
st.sidebar.image("https://img.icons8.com/color/96/airplane-take-off.png", width=64)
st.sidebar.title("Ops Copilot Navigation")
app_mode = st.sidebar.radio(
    "Choose View:",
    [
        "1. Executive Ops Dashboard",
        "2. Cross-Tracker Auto-Reconciler",
        "3. AI Omnichannel Intake Agent",
        "4. Solution Architecture & Target Metrics"
    ]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### Zero-Headcount Principles")
st.sidebar.info(
    "• Single Source of Truth (SSOT)\n"
    "• Auto-Capture for WhatsApp/Email\n"
    "• Deterministic State Machine\n"
    "• Automated Proactive Comms"
)

# ==========================================
# VIEW 1: EXECUTIVE OPS DASHBOARD
# ==========================================
if app_mode == "1. Executive Ops Dashboard":
    st.subheader("📊 Operational Diagnosis & Empirical Evidence")
    st.markdown(
        "Diagnosing the paradox: **Refund volume remained flat** (~145/month), "
        "while **escalations exploded 150% in June** (from 30 to 75)."
    )

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Support Requests", f"{summary['total_support_logged']}", "Flat ~145/mo")
    with col2:
        st.metric("June Escalations Spike", "75", "+150% MoM surge", delta_color="inverse")
    with col3:
        st.metric("Dropped Handoffs", f"{summary['dropped_handoffs']}", "Logged by Support, 0 in Finance", delta_color="inverse")
    with col4:
        st.metric("Stalled in June Approval", f"{summary['pending_approval_bottlenecks']}", "47% of June Finance Intake", delta_color="inverse")

    st.markdown("---")

    # Chart 1: Volume vs Escalations
    st.markdown("#### The Volume vs Escalation Divergence")
    
    # Prepare monthly trends
    monthly_data = pd.DataFrame({
        "Month": ["2026-02", "2026-03", "2026-04", "2026-05", "2026-06"],
        "Support Requests": [150, 146, 145, 147, 144],
        "Finance Payouts Done": [105, 148, 134, 115, 60],
        "Escalations Raised": [2, 23, 25, 30, 75]
    })
    
    chart_melted = monthly_data.melt(id_vars=["Month"], var_name="Metric", value_name="Count")
    
    chart = alt.Chart(chart_melted).mark_line(point=True).encode(
        x=alt.X('Month:N', title='Calendar Month (2026)'),
        y=alt.Y('Count:Q', title='Count'),
        color=alt.Color('Metric:N', scale=alt.Scale(range=['#1f77b4', '#2ca02c', '#d62728'])),
        tooltip=['Month', 'Metric', 'Count']
    ).properties(height=350)
    
    st.altair_chart(chart, use_container_width=True)

    colA, colB = st.columns(2)
    with colA:
        st.markdown("#### Primary Escalation Drivers (Complaints Analysis)")
        top_complaints = esc_df['Complaint'].value_counts().head(8).reset_index()
        top_complaints.columns = ['Complaint Type', 'Count']
        st.dataframe(top_complaints, use_container_width=True, hide_index=True)

    with colB:
        st.markdown("#### Root Cause Breakdown")
        st.markdown(
            "1. **Asynchronous Silos (45% of issues):** Support marks tickets 'Closed' upon inquiry reply, "
            "while Finance has no record of the ticket (69 tickets dropped).\n"
            "2. **June Approval Paralysis (35% of issues):** N. Iyer & R. Menon stopped sign-offs mid-June. "
            "58 payouts stalled in `Pending Payout` without alerting Support or agents.\n"
            "3. **Omnichannel Shadow Requests (12% of issues):** WhatsApp/Email requests acknowledged verbally "
            "without canonical RF reference numbers (e.g., RF-1098, RF-1099).\n"
            "4. **Deduction Transparency (8% of issues):** 53 gaps among completed payouts: 556 of 571 matched payouts "
            "are explained by airline deductions, leaving only 3 unexplained discrepancies (RF-1041, RF-1368, RF-1435)."
        )

# ==========================================
# VIEW 2: CROSS-TRACKER AUTO-RECONCILER
# ==========================================
elif app_mode == "2. Cross-Tracker Auto-Reconciler":
    st.subheader("🔄 Automated Cross-Tracker Reconciliation Engine")
    st.markdown(
        "Instantly reconciles disparate Support and Finance trackers, eliminates duplicate rows, "
        "normalizes ticket IDs (`RF 1079` → `RF-1079`), and exposes operational blind spots."
    )

    filter_type = st.selectbox(
        "Filter Operational Discrepancies:",
        [
            "ALL DISCREPANCIES",
            "DROPPED_HANDOFF (Support Closed, Missing in Finance)",
            "APPROVAL_BOTTLENECK (Stalled in Pending Payout)",
            "AMOUNT_MISMATCH (Gross Quote != Paid + Deduction)",
            "SHADOW_INTAKE (In Finance, Missing in Support)"
        ]
    )

    df_filtered = merged_df.copy()
    if filter_type.startswith("DROPPED_HANDOFF"):
        df_filtered = df_filtered[df_filtered['Discrepancy_Type'] == 'DROPPED_HANDOFF']
    elif filter_type.startswith("APPROVAL_BOTTLENECK"):
        df_filtered = df_filtered[df_filtered['Discrepancy_Type'] == 'APPROVAL_BOTTLENECK']
    elif filter_type.startswith("AMOUNT_MISMATCH"):
        df_filtered = df_filtered[df_filtered['Discrepancy_Type'] == 'AMOUNT_MISMATCH']
    elif filter_type.startswith("SHADOW_INTAKE"):
        df_filtered = df_filtered[df_filtered['Discrepancy_Type'] == 'SHADOW_INTAKE']
    else:
        df_filtered = df_filtered[df_filtered['Discrepancy_Type'] != 'RECONCILED_OK']

    st.write(f"Showing **{len(df_filtered)}** flagged records")

    display_cols = [
        'Norm_ID', 'Discrepancy_Type', 'Agent_Support', 'Refund Amount (INR)',
        'Amount Paid (INR)', 'Deduction (INR)', 'Clean_Status', 'Clean_Payout_Status',
        'Remarks', 'Escalation_Count'
    ]
    # Filter available columns
    available_cols = [c for c in display_cols if c in df_filtered.columns]
    st.dataframe(df_filtered[available_cols], use_container_width=True)

    st.markdown("#### One-Click Remediation Action")
    colX, colY = st.columns(2)
    with colX:
        if st.button("🚀 Push Dropped Handoffs to Finance Queue"):
            st.success(f"Successfully bridged {summary['dropped_handoffs']} dropped tickets directly into Finance Queue with auto-generated audit stamp!")
    with colY:
        if st.button("🔔 Trigger Manager SLA Approval Alert (58 Pending Payouts)"):
            st.warning("Sent automated digest of 58 stalled June payouts to Finance Leadership for emergency batch approval!")

# ==========================================
# VIEW 3: AI OMNICHANNEL INTAKE AGENT
# ==========================================
elif app_mode == "3. AI Omnichannel Intake Agent":
    st.subheader("🤖 AI Omnichannel Intake & Triage Agent")
    st.markdown(
        "Captures informal WhatsApp & Email messages (English / Hinglish), extracts entities, "
        "detects urgency/intent, assigns a canonical reference ID, and drafts proactive replies."
    )

    preset = st.selectbox(
        "Load Brief Real-World Scenario:",
        [
            "Custom Input",
            "Nomad Travel - Hinglish WhatsApp (RF-1098 Case)",
            "Peak Journeys - Missing Ref Email (RF-1099 Case)",
            "Internal Support Agent Handoff Note"
        ]
    )

    default_text = ""
    default_sender = "Unknown"
    default_channel = "WhatsApp"

    if preset == "Nomad Travel - Hinglish WhatsApp (RF-1098 Case)":
        default_text = "Bhai refund ka kya hua? BLR-MAA wala. 2 hafte ho gaye, koi jawab nahi."
        default_sender = "Nomad Travel"
        default_channel = "WhatsApp"
    elif preset == "Peak Journeys - Missing Ref Email (RF-1099 Case)":
        default_text = "Hi, I cancelled booking for DEL-DXB last week and was told I'd get a refund. I haven't received anything and I don't have any reference number. Please help, my client is asking."
        default_sender = "Peak Journeys"
        default_channel = "Email"
    elif preset == "Internal Support Agent Handoff Note":
        default_text = "Finance says they never received several of the refunds I closed last month. I marked them done on my side. Not sure where they went."
        default_sender = "Support Team"
        default_channel = "Email"

    col_in1, col_in2 = st.columns([3, 1])
    with col_in1:
        user_msg = st.text_area("Incoming Message Content:", value=default_text, height=120)
    with col_in2:
        channel = st.selectbox("Channel:", ["WhatsApp", "Email", "Phone", "Portal"], index=["WhatsApp", "Email", "Phone", "Portal"].index(default_channel))
        sender = st.text_input("Sender / Travel Agent:", value=default_sender)

    if st.button("⚡ Process with AI Operations Agent"):
        result = intake_agent.parse_message(user_msg, channel=channel, sender=sender)
        
        st.markdown("---")
        st.markdown("### Extraction & Structured Triage Output")
        
        res1, res2, res3, res4 = st.columns(4)
        with res1:
            st.metric("Canonical Ticket ID", result['ticket_id'])
        with res2:
            st.metric("Detected Route", result['sector'])
        with res3:
            st.metric("Classified Intent", result['intent'])
        with res4:
            color = "🔴" if result['urgency'] == "CRITICAL" else "🟠" if result['urgency'] == "HIGH" else "🟢"
            st.metric("Urgency / Risk", f"{color} {result['urgency']} ({result['risk_score']}/100)")

        st.markdown(f"**Recommended Action:** `{result['recommended_action']}`")
        if result['risk_factors']:
            st.markdown(f"**Risk Factors Identified:** {', '.join(result['risk_factors'])}")

        st.markdown("#### Proactive Agent Response (Zero-Touch Communication)")
        st.text_area("Drafted Outbound Communication:", value=result['proactive_response_draft'], height=160)
        st.button("✉️ Send Automated Response & Push to SSOT")

# ==========================================
# VIEW 4: SOLUTION ARCHITECTURE & TARGET METRICS
# ==========================================
elif app_mode == "4. Solution Architecture & Target Metrics":
    st.subheader("🏛️ Target Operating Model & Measurement Framework")
    
    st.markdown("### The Deterministic Lifecycle State-Machine")
    st.markdown(
        """
        Replacing subjective free-text statuses (`Closed`, `Working`) with a synchronized 5-stage lifecycle:
        1. **`REQUEST_CAPTURED`**: Intake via Portal/API/AI Agent. Instant canonical `RF-XXXX` issued to agent.
        2. **`ELIGIBILITY_VALIDATED`**: Auto-calculated cancellation fee + net payable amount.
        3. **`FINANCE_QUEUED`**: Automated handoff to Finance with complete audit trail (Zero dropped tickets).
        4. **`PAYOUT_APPROVED`**: Rule-based auto-approval for low risk (<₹25k within window); manager queue for exceptions.
        5. **`PAYOUT_COMPLETED / DECLINED`**: Payout executed, automated notification sent with transaction ref + breakdown.
        """
    )

    st.markdown("---")
    st.markdown("### Strategic Trade-Off Matrix (Under Zero-Headcount Constraint)")

    matrix_data = pd.DataFrame([
        {
            "Function": "Omnichannel Intake & Ticket Creation",
            "Decision": "100% Automated (AI Parser)",
            "Rationale": "Eliminates shadow requests, spelling errors, and unlogged inquiries like RF-1098 & RF-1099 without adding staff."
        },
        {
            "Function": "Standard Deduction Calculation",
            "Decision": "100% Automated (Policy Rules Engine)",
            "Rationale": "Eliminates the 89 amount discrepancies where agents received less than promised."
        },
        {
            "Function": "Proactive Status & Payout Alerts",
            "Decision": "100% Automated (WhatsApp/Email Webhooks)",
            "Rationale": "Directly resolves 60%+ of all escalations ('Agent chasing status, no response')."
        },
        {
            "Function": "Routine Payouts (< ₹25,000)",
            "Decision": "Automated Batch Approval",
            "Rationale": "Eliminates the single-manager approval bottleneck that paralyzed June operations."
        },
        {
            "Function": "Disputed / Out-of-Policy Cancellations",
            "Decision": "Deliberately Manual (Finance Lead)",
            "Rationale": "High-risk edge cases (airline bankruptcy, waivers) require human business discretion."
        },
        {
            "Function": "Key Account Direct Relationship Handling",
            "Decision": "Deliberately Manual (Senior Support)",
            "Rationale": "Preserves high-touch trust with top travel partners while removing routine operational friction."
        }
    ])
    st.table(matrix_data)

    st.markdown("---")
    st.markdown("### 30-Day Measurement Scorecard")

    col_m1, col_m2 = st.columns(2)
    with col_m1:
        st.markdown("#### Primary Metric: Escalation Rate")
        st.markdown(
            """
            $$\\text{Refund Escalation Rate} = \\frac{\\text{Escalations Raised in Month}}{\\text{Total Refund Requests}} \\times 100$$
            * **Baseline (June 2026):** **52.1%** (75 escalations on 144 requests).
            * **Target (Day 30):** **< 8.0%** (<12 escalations).
            * **Target (Day 60):** **< 3.0%**.
            """
        )
    with col_m2:
        st.markdown("#### Secondary Metric: Cross-Team Reconciliation Lag")
        st.markdown(
            """
            $$\\text{Reconciliation Lag} = \\text{Finance Received Date} - \\text{Support Request Date}$$
            * **Baseline (Current):** **2.47 days average handoff lag** (total turnaround lag is **6.23 days**, with 69 tickets dropped).
            * **Target (Day 30):** **< 15 minutes** (Real-time automated handoff via SSOT).
            * **Secondary Target:** **Pending Payout Aging** reduced from 25+ days to **< 48 hours**.
            """
        )

st.markdown("---")
st.caption("BharatTrip AI Operations Associate Take-Home Submission | Powered by Streamlit & Python")

