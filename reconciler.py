"""
BharatTrip Refund Operations: Core Reconciliation & Analysis Engine
Author: AI Operations Associate Candidate
Purpose: Automated cross-tracker reconciliation, anomaly detection, and operational triage.
"""

import os
import sys
import re
import pandas as pd
import numpy as np

DEFAULT_WORKBOOK = "BharatTrip_Refund_Data.xlsx"

def resolve_workbook_path(path=None):
    """
    Resolves workbook path from argument, environment variable, or default.
    Raises clear FileNotFoundError if the file cannot be found.
    """
    if path:
        target = path
    elif os.environ.get("BHARATTRIP_WORKBOOK"):
        target = os.environ.get("BHARATTRIP_WORKBOOK")
    elif os.environ.get("BHARATTRIP_DATA_PATH"):
        target = os.environ.get("BHARATTRIP_DATA_PATH")
    else:
        target = DEFAULT_WORKBOOK

    if not os.path.exists(target):
        abs_target = os.path.abspath(target)
        raise FileNotFoundError(
            f"Workbook not found at '{abs_target}'. "
            f"Please place '{DEFAULT_WORKBOOK}' in this directory or provide path via argument/environment variable."
        )

    return target

def normalize_ticket_id(val):
    """Normalize ticket IDs to standard 'RF-XXXX' format."""
    if pd.isna(val):
        return None
    s = str(val).strip().upper()
    match = re.search(r'RF\s*[-]?\s*(\d+)', s)
    if match:
        return f"RF-{match.group(1)}"
    return s

def clean_status(val):
    if pd.isna(val):
        return "Unknown"
    return str(val).strip().title()

def run_reconciliation(excel_path=None):
    """
    Ingests Support_Tracker, Finance_Tracker, and Escalations sheets,
    performs normalization, reconciliation, and computes operational triage metrics.
    """
    excel_path = resolve_workbook_path(excel_path)

    st_raw = pd.read_excel(excel_path, sheet_name="Support_Tracker")
    ft_raw = pd.read_excel(excel_path, sheet_name="Finance_Tracker")
    esc_raw = pd.read_excel(excel_path, sheet_name="Escalations")

    # 1. Exact duplicates before normalisation
    exact_duplicate_rows_support = int(st_raw.duplicated().sum())
    exact_duplicate_rows_finance = int(ft_raw.duplicated().sum())

    # 2. Conflicting ID rows in Support (share normalized ID but differ in amount or status)
    st_no_exact = st_raw.drop_duplicates().copy()
    st_no_exact['Norm_ID'] = st_no_exact['Ticket ID'].apply(normalize_ticket_id)
    conflicts = st_no_exact[st_no_exact['Norm_ID'].duplicated(keep=False)]
    conflicting_id_rows_support = int(conflicts['Norm_ID'].nunique())

    # Working copies for normalisation and reconciliation
    st = st_raw.copy()
    ft = ft_raw.copy()
    esc = esc_raw.copy()

    st['Norm_ID'] = st['Ticket ID'].apply(normalize_ticket_id)
    ft['Norm_ID'] = ft['Ref No'].apply(normalize_ticket_id)
    esc['Norm_ID'] = esc['Related Ticket / Ref'].apply(normalize_ticket_id)

    st['Clean_Status'] = st['Status'].apply(clean_status)
    ft['Clean_Payout_Status'] = ft['Payout Status'].apply(clean_status)
    esc['Clean_Status'] = esc['Status'].apply(clean_status)

    # Dates
    st['Req_Date'] = pd.to_datetime(st['Request Date'], dayfirst=True, errors='coerce')
    ft['Rec_Date'] = pd.to_datetime(ft['Received On'], format='mixed', dayfirst=True, errors='coerce')
    ft['Proc_Date'] = pd.to_datetime(ft['Processed On'], dayfirst=True, errors='coerce')
    esc['Raised_Date'] = pd.to_datetime(esc['Raised On'], dayfirst=True, errors='coerce')

    # Deduplicate trackers keeping first row for reconciliation join
    st_dup_count = st['Norm_ID'].duplicated().sum()
    ft_dup_count = ft['Norm_ID'].duplicated().sum()

    st_unique = st.drop_duplicates(subset=['Norm_ID'], keep='first').copy()
    ft_unique = ft.drop_duplicates(subset=['Norm_ID'], keep='first').copy()

    # Outer join to reconcile
    merged = pd.merge(
        st_unique,
        ft_unique,
        on='Norm_ID',
        how='outer',
        suffixes=('_Support', '_Finance'),
        indicator=True
    )

    # 3. dropped_handoffs: Support closed, no Finance record
    dropped_handoffs = int(((merged['_merge'] == 'left_only') & (merged['Clean_Status'] == 'Closed')).sum())

    # 4. shadow_finance_intakes: Finance has record, Support does not
    shadow_finance_intakes = int((merged['_merge'] == 'right_only').sum())

    # 5. june_pending_payouts: every Pending Payout row received in June
    june_pending_payouts = int(((ft['Clean_Payout_Status'] == 'Pending Payout') & (ft['Rec_Date'].dt.month == 6)).sum())

    # Completed payouts with gap & deduction explanation (Refund Done rows)
    both = merged[merged['_merge'] == 'both'].copy()
    refund_done = both[both['Clean_Payout_Status'] == 'Refund Done'].copy()

    # 6. completed_payouts_with_gap: requested amount exceeds paid amount (> 1 INR)
    gap_mask = (refund_done['Refund Amount (INR)'] - refund_done['Amount Paid (INR)']) > 1.0
    completed_payouts_with_gap = int(gap_mask.sum())

    # 7. gap_explained_by_deduction: diff between requested and (paid + deduction) <= 1 INR
    diff = (refund_done['Refund Amount (INR)'] - (refund_done['Amount Paid (INR)'].fillna(0) + refund_done['Deduction (INR)'].fillna(0))).abs()
    gap_explained_by_deduction = int((diff <= 1.0).sum())
    completed_gaps_explained_by_deduction = int((gap_mask & (diff <= 1.0)).sum())

    # 8. unexplained_gaps: list the IDs where the gap is not explained by the deduction
    unexplained_gaps = sorted(refund_done[diff > 1.0]['Norm_ID'].dropna().tolist())

    # Compute row-level discrepancy flags
    def flag_discrepancy(row):
        merge_type = row['_merge']
        if merge_type == 'left_only':
            return 'DROPPED_HANDOFF' if row['Clean_Status'] == 'Closed' else 'SUPPORT_ONLY'
        elif merge_type == 'right_only':
            return 'SHADOW_INTAKE'
        else:
            payout_status = row['Clean_Payout_Status']
            if payout_status == 'Pending Payout':
                return 'APPROVAL_BOTTLENECK'
            elif payout_status == 'Declined':
                return 'DECLINED_WITHOUT_SYNC'

            req_amt = row['Refund Amount (INR)']
            paid_amt = row['Amount Paid (INR)'] if pd.notna(row['Amount Paid (INR)']) else 0
            ded_amt = row['Deduction (INR)'] if pd.notna(row['Deduction (INR)']) else 0

            if pd.notna(req_amt):
                row_diff = abs(req_amt - (paid_amt + ded_amt))
                if row_diff > 1.0:
                    return 'AMOUNT_MISMATCH'

            return 'RECONCILED_OK'

    merged['Discrepancy_Type'] = merged.apply(flag_discrepancy, axis=1)

    # Calculate Lags
    merged['Handoff_Lag_Days'] = (merged['Rec_Date'] - merged['Req_Date']).dt.days
    merged['Finance_Proc_Lag_Days'] = (merged['Proc_Date'] - merged['Rec_Date']).dt.days
    merged['Total_Turnaround_Days'] = (merged['Proc_Date'] - merged['Req_Date']).dt.days
    avg_total_lag_days = round(float(merged['Total_Turnaround_Days'].mean()), 2)

    # Link with Escalations
    esc_counts = esc.groupby('Norm_ID').size().to_dict()
    merged['Escalation_Count'] = merged['Norm_ID'].map(esc_counts).fillna(0).astype(int)

    # Summary Statistics
    summary = {
        "exact_duplicate_rows_support": exact_duplicate_rows_support,
        "exact_duplicate_rows_finance": exact_duplicate_rows_finance,
        "conflicting_id_rows_support": conflicting_id_rows_support,
        "dropped_handoffs": dropped_handoffs,
        "shadow_finance_intakes": shadow_finance_intakes,
        "june_pending_payouts": june_pending_payouts,
        "completed_payouts_with_gap": completed_payouts_with_gap,
        "gap_explained_by_deduction": gap_explained_by_deduction,
        "completed_gaps_explained_by_deduction": completed_gaps_explained_by_deduction,
        "unexplained_gaps": unexplained_gaps,
        "avg_total_lag_days": avg_total_lag_days,
        # Operational totals
        "total_support_logged": len(st),
        "unique_support_tickets": len(st_unique),
        "total_finance_records": len(ft),
        "unique_finance_tickets": len(ft_unique),
        "total_escalations": len(esc),
        "reconciled_both": int((merged['_merge'] == 'both').sum()),
        "pending_approval_bottlenecks": june_pending_payouts,
        "unexplained_amount_mismatches": len(unexplained_gaps),
        "avg_handoff_lag": float(merged['Handoff_Lag_Days'].mean()),
        "avg_finance_lag": float(merged['Finance_Proc_Lag_Days'].mean()),
        "avg_total_lag": avg_total_lag_days
    }

    return merged, summary, esc

if __name__ == "__main__":
    cli_path = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("-") else None
    try:
        merged, summary, esc = run_reconciliation(cli_path)
    except FileNotFoundError as err:
        print(f"Error: {err}", file=sys.stderr)
        sys.exit(1)

    print("=" * 65)
    print("BHARATTRIP REFUND OPERATIONS: RECONCILIATION SUMMARY")
    print("=" * 65)
    metrics_to_print = [
        "exact_duplicate_rows_support",
        "exact_duplicate_rows_finance",
        "conflicting_id_rows_support",
        "dropped_handoffs",
        "shadow_finance_intakes",
        "june_pending_payouts",
        "completed_payouts_with_gap",
        "gap_explained_by_deduction",
        "unexplained_gaps",
        "avg_total_lag_days"
    ]
    for k in metrics_to_print:
        v = summary[k]
        if isinstance(v, float):
            print(f"  {k:30s}: {v:.2f}")
        else:
            print(f"  {k:30s}: {v}")
    print("=" * 65)
