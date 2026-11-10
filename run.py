"""
BharatTrip AI Operations Prototype: Quick-Start Runner
Run with: python run.py
Or Web UI: python run.py --web
Or Streamlit: python run.py --streamlit
"""

import sys
import os
import webbrowser
import http.server
import socketserver
import subprocess
from reconciler import run_reconciliation, DEFAULT_WORKBOOK
from ai_intake_agent import RefundIntakeAgent

def start_web_server(port=8080):
    print("=" * 70)
    print(f"Launching BharatTrip HTML Web Frontend at http://localhost:{port}...")
    print("=" * 70)

    webbrowser.open(f"http://localhost:{port}/index.html")

    class QuietHandler(http.server.SimpleHTTPRequestHandler):
        def log_message(self, format, *args):
            pass

    with socketserver.TCPServer(("", port), QuietHandler) as httpd:
        print(f"Serving at http://localhost:{port}/index.html (Press Ctrl+C to stop)")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server.")

def main():
    if len(sys.argv) > 1:
        flag = sys.argv[1].lower()
        if flag in ["--web", "--html", "-w"]:
            start_web_server()
            return
        elif flag in ["--streamlit", "--ui"]:
            print("Starting Streamlit Web Dashboard...")
            subprocess.run(["streamlit", "run", "app.py"])
            return

    # Check for custom workbook path or default
    workbook_path = None
    if len(sys.argv) > 1 and not sys.argv[1].startswith("-"):
        workbook_path = sys.argv[1]

    print("=" * 70)
    print("BHARATTRIP REFUND OPERATIONS COPILOT & RECONCILIATION ENGINE")
    print("AI Operations Associate Take-Home Task Prototype")
    print("=" * 70)

    # 1. Run Core Reconciler
    print("\n[STEP 1] Running Automated Cross-Tracker Reconciliation on Excel Extract...")
    try:
        merged_df, summary, esc_df = run_reconciliation(workbook_path)
    except FileNotFoundError as err:
        print(f"Error: {err}", file=sys.stderr)
        sys.exit(1)

    print("\n--- RECONCILIATION SUMMARY METRICS ---")
    metrics_to_show = [
        ("exact_duplicate_rows_support", summary["exact_duplicate_rows_support"]),
        ("exact_duplicate_rows_finance", summary["exact_duplicate_rows_finance"]),
        ("conflicting_id_rows_support", summary["conflicting_id_rows_support"]),
        ("dropped_handoffs", summary["dropped_handoffs"]),
        ("shadow_finance_intakes", summary["shadow_finance_intakes"]),
        ("june_pending_payouts", summary["june_pending_payouts"]),
        ("completed_payouts_with_gap", summary["completed_payouts_with_gap"]),
        ("gap_explained_by_deduction", summary["gap_explained_by_deduction"]),
        ("unexplained_gaps", summary["unexplained_gaps"]),
        ("avg_total_lag_days", summary["avg_total_lag_days"]),
    ]

    for name, val in metrics_to_show:
        if isinstance(val, float):
            print(f"  {name:30s}: {val:.2f}")
        else:
            print(f"  {name:30s}: {val}")

    # 2. Test Intake Agent on sample cases
    print("\n" + "=" * 70)
    print("[STEP 2] Testing AI Omnichannel Intake Agent on Brief Samples...")
    agent = RefundIntakeAgent()

    test_cases = [
        ("Nomad Travel", "WhatsApp", "Bhai refund ka kya hua? BLR-MAA wala. 2 hafte ho gaye, koi jawab nahi."),
        ("Peak Journeys", "Email", "Hi, I cancelled booking for DEL-DXB last week and was told I'd get a refund. I haven't received anything and I don't have any reference number. Please help, my client is asking.")
    ]

    for sender, ch, msg in test_cases:
        print(f"\nIncoming from: {sender} ({ch})")
        print(f"Raw Text     : \"{msg}\"")
        res = agent.parse_message(msg, channel=ch, sender=sender)
        print(f" -> Assigned Ref ID  : {res['ticket_id']}")
        print(f" -> Detected Route   : {res['sector']}")
        print(f" -> Intent / Urgency : {res['intent']} | Urgency: {res['urgency']} (Risk Score: {res['risk_score']}/100)")
        print(f" -> Action           : {res['recommended_action']}")
        print(f" -> Drafted Reply    :\n    {res['proactive_response_draft'].replace('\n', '\n    ')}")

    print("\n" + "=" * 70)
    print("PROTOTYPE READY & OPERATIONAL!")
    print("To view the HTML frontend, run:")
    print("   python run.py --web")
    print("   or double-click 'index.html'")
    print("=" * 70)

if __name__ == "__main__":
    main()
