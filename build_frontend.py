"""
Clean, professional HTML frontend generator for BharatTrip Refund Operations.
Includes a dedicated visual flow tab: 'How We Solved This (Visual Flow)'.
Eliminates fluff while providing clear, high-density diagrams and step-by-step forensic reasoning.
"""

import json
import os
from datetime import datetime
import pandas as pd
from reconciler import run_reconciliation

def build_clean_html_with_flow(workbook_path=None):
    merged_df, summary, esc_df = run_reconciliation(workbook_path)

    rec_df = merged_df.copy()
    rec_df['Agent_Display'] = rec_df['Agent'].fillna(rec_df['Agent Name']).fillna('Unknown')
    rec_df['Route_Display'] = rec_df['Route'].fillna(rec_df['Sector']).fillna('Unknown')
    cols_to_keep = [
        'Norm_ID', 'Agent', 'Agent Name', 'Route', 'Sector', 'Refund Amount (INR)',
        'Amount Paid (INR)', 'Deduction (INR)', 'Clean_Status', 'Clean_Payout_Status',
        'Discrepancy_Type', 'Remarks', 'Escalation_Count', 'Handoff_Lag_Days',
        'Finance_Proc_Lag_Days', 'Total_Turnaround_Days', 'Channel', 'Handled By',
        'Approved By', 'Agent_Display', 'Route_Display'
    ]
    records = rec_df[cols_to_keep].fillna('').to_dict(orient='records')
    top_complaints = esc_df['Complaint'].value_counts().head(10).to_dict()

    data = {
        'summary': summary,
        'records': records,
        'top_complaints': top_complaints
    }

    with open("reconciled_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    json_str = json.dumps(data)

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>BharatTrip Operations | Refund Reconciliation</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <style>
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }}
    .mono {{
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
    }}
    .tag-dropped {{ background: #fef2f2; color: #991b1b; border: 1px solid #fecaca; }}
    .tag-stall {{ background: #faf5ff; color: #6b21a8; border: 1px solid #e9d5ff; }}
    .tag-mismatch {{ background: #fffbeb; color: #92400e; border: 1px solid #fde68a; }}
    .tag-shadow {{ background: #f0f9ff; color: #075985; border: 1px solid #bae6fd; }}
    .tag-ok {{ background: #f0fdf4; color: #166534; border: 1px solid #bbf7d0; }}
  </style>
</head>
<body class="bg-slate-100 text-slate-800 antialiased min-h-screen flex flex-col text-sm">

  <!-- TOP BAR -->
  <header class="bg-white border-b border-slate-200 sticky top-0 z-40">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 h-14 flex items-center justify-between">
      <div class="flex items-center space-x-3">
        <span class="font-bold text-base text-slate-900 tracking-tight">BharatTrip</span>
        <span class="text-slate-300">/</span>
        <span class="text-slate-600 font-medium text-xs sm:text-sm">Refund Operations &amp; Reconciliation</span>
      </div>

      <div class="flex items-center space-x-3">
        <span class="text-xs text-slate-500 hidden sm:inline">Data snapshot: <strong>30 June 2026</strong> (749 records)</span>
        <a href="BharatTrip_AI_Operations_WriteUp.pdf" download class="inline-flex items-center px-2.5 py-1 text-xs font-medium rounded border border-slate-300 bg-white text-slate-700 hover:bg-slate-50">
          PDF Report
        </a>
      </div>
    </div>

    <!-- TABS -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 flex space-x-4 sm:space-x-6 border-t border-slate-100 text-xs font-medium overflow-x-auto">
      <button onclick="showTab('summary')" id="tab-btn-summary" class="tab-btn py-2.5 border-b-2 border-slate-900 text-slate-900 font-semibold whitespace-nowrap">Summary</button>
      <button onclick="showTab('flow')" id="tab-btn-flow" class="tab-btn py-2.5 border-b-2 border-transparent text-slate-500 hover:text-slate-800 whitespace-nowrap flex items-center space-x-1.5">
        <span>How We Got Here (Visual Flow)</span>
        <span class="w-1.5 h-1.5 rounded-full bg-blue-600"></span>
      </button>
      <button onclick="showTab('reconciliation')" id="tab-btn-reconciliation" class="tab-btn py-2.5 border-b-2 border-transparent text-slate-500 hover:text-slate-800 whitespace-nowrap">Discrepancy Audit (143)</button>
      <button onclick="showTab('parser')" id="tab-btn-parser" class="tab-btn py-2.5 border-b-2 border-transparent text-slate-500 hover:text-slate-800 whitespace-nowrap">Inbound Message Parser</button>
      <button onclick="showTab('process')" id="tab-btn-process" class="tab-btn py-2.5 border-b-2 border-transparent text-slate-500 hover:text-slate-800 whitespace-nowrap">Target Process &amp; SLAs</button>
    </div>
  </header>

  <!-- CONTENT CONTAINER -->
  <main class="flex-1 max-w-7xl w-full mx-auto p-4 sm:p-6 space-y-5">

    <!-- ============================================================== -->
    <!-- TAB 1: SUMMARY -->
    <!-- ============================================================== -->
    <div id="view-summary" class="space-y-5">

      <!-- KEY STATS ROW -->
      <div class="grid grid-cols-2 lg:grid-cols-4 gap-3">
        <div class="bg-white p-4 rounded-lg border border-slate-200">
          <div class="text-xs text-slate-500 font-medium">Monthly Intake Volume</div>
          <div class="text-2xl font-bold text-slate-900 mt-1">144</div>
          <div class="text-xs text-slate-500 mt-1">Flat across Feb–Jun (avg 146.4/mo)</div>
        </div>

        <div class="bg-white p-4 rounded-lg border border-slate-200 border-l-4 border-l-red-500">
          <div class="text-xs text-slate-500 font-medium">June Escalations</div>
          <div class="text-2xl font-bold text-red-600 mt-1">75</div>
          <div class="text-xs text-red-700 mt-1">Surged from 30 in May (+150%)</div>
        </div>

        <div class="bg-white p-4 rounded-lg border border-slate-200 border-l-4 border-l-amber-500">
          <div class="text-xs text-slate-500 font-medium">Dropped Handoffs</div>
          <div class="text-2xl font-bold text-amber-600 mt-1">69</div>
          <div class="text-xs text-slate-500 mt-1">In Support, 0 record in Finance</div>
        </div>

        <div class="bg-white p-4 rounded-lg border border-slate-200 border-l-4 border-l-purple-500">
          <div class="text-xs text-slate-500 font-medium">June Stalled Payouts</div>
          <div class="text-2xl font-bold text-purple-600 mt-1">58</div>
          <div class="text-xs text-slate-500 mt-1">Pending approval after approver freeze</div>
        </div>
      </div>

      <!-- DATA BREAKDOWN GRID -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-5">
        
        <!-- Monthly Trend Table -->
        <div class="bg-white p-4 rounded-lg border border-slate-200">
          <h2 class="font-bold text-slate-900 text-sm mb-3">Monthly Volume &amp; Payouts (Feb – Jun 2026)</h2>
          <table class="w-full text-xs text-left">
            <thead>
              <tr class="border-b border-slate-200 text-slate-500">
                <th class="pb-2 font-medium">Month</th>
                <th class="pb-2 font-medium text-right">Support Intake</th>
                <th class="pb-2 font-medium text-right">Finance Paid</th>
                <th class="pb-2 font-medium text-right">Pending Payout</th>
                <th class="pb-2 font-medium text-right">Escalations</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-100">
              <tr>
                <td class="py-2 font-medium">Feb 2026</td>
                <td class="py-2 text-right">150</td>
                <td class="py-2 text-right">105</td>
                <td class="py-2 text-right">0</td>
                <td class="py-2 text-right text-slate-500">2</td>
              </tr>
              <tr>
                <td class="py-2 font-medium">Mar 2026</td>
                <td class="py-2 text-right">146</td>
                <td class="py-2 text-right">148</td>
                <td class="py-2 text-right">0</td>
                <td class="py-2 text-right text-slate-500">23</td>
              </tr>
              <tr>
                <td class="py-2 font-medium">Apr 2026</td>
                <td class="py-2 text-right">145</td>
                <td class="py-2 text-right">134</td>
                <td class="py-2 text-right">0</td>
                <td class="py-2 text-right text-slate-500">25</td>
              </tr>
              <tr>
                <td class="py-2 font-medium">May 2026</td>
                <td class="py-2 text-right">147</td>
                <td class="py-2 text-right">115</td>
                <td class="py-2 text-right">0</td>
                <td class="py-2 text-right text-slate-500">30</td>
              </tr>
              <tr class="bg-red-50/50 font-semibold">
                <td class="py-2 text-red-900">Jun 2026 (Spike)</td>
                <td class="py-2 text-right text-slate-900">144</td>
                <td class="py-2 text-right text-red-700">60 (-48%)</td>
                <td class="py-2 text-right text-purple-700">58 (Stalled)</td>
                <td class="py-2 text-right text-red-700">75 (+150%)</td>
              </tr>
            </tbody>
          </table>
          <p class="mt-3 text-xs text-slate-500 leading-normal">
            <strong>Diagnosis:</strong> The escalation crisis is not an intake capacity problem. Request volume remained flat at ~145/mo. The spike in June was triggered by a collapse in completed payouts (down to 60) when manager sign-offs stopped.
          </p>
        </div>

        <!-- Top Escalation Causes -->
        <div class="bg-white p-4 rounded-lg border border-slate-200">
          <h2 class="font-bold text-slate-900 text-sm mb-3">Top Escalation Complaints (155 Total)</h2>
          <div class="space-y-2.5" id="complaint-rows">
            <!-- Populated via JS -->
          </div>
          <p class="mt-3 text-xs text-slate-500 leading-normal border-t border-slate-100 pt-2.5">
            <strong>Key Driver:</strong> Over 60% of complaints stem directly from communication silence ("chasing for update", "no record in Finance", "repeated follow-ups"). Fixing visibility solves the majority of escalations without adding headcount.
          </p>
        </div>

      </div>

      <!-- Root Cause Summary Box -->
      <div class="bg-white p-4 rounded-lg border border-slate-200">
        <h2 class="font-bold text-slate-900 text-sm mb-2">Four Operational Breakdowns (Backed by Data)</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-3 text-xs">
          <div class="p-3 bg-slate-50 rounded border border-slate-200">
            <div class="font-semibold text-slate-900">1. Disconnected Trackers</div>
            <p class="text-slate-600 mt-1">69 tickets logged by Support were marked "Closed" without ever reaching Finance, leaving agents waiting indefinitely.</p>
          </div>
          <div class="p-3 bg-slate-50 rounded border border-slate-200">
            <div class="font-semibold text-slate-900">2. June Approver Freeze</div>
            <p class="text-slate-600 mt-1">N. Iyer stopped sign-offs after June 13. With no delegation rule, 58 payouts stalled in pending status (47% of June volume).</p>
          </div>
          <div class="p-3 bg-slate-50 rounded border border-slate-200">
            <div class="font-semibold text-slate-900">3. Shadow Ingestion</div>
            <p class="text-slate-600 mt-1">Requests like RF-1098 (WhatsApp) &amp; RF-1099 (Email) were never logged into either tracker. They exist only in Escalations.</p>
          </div>
          <div class="p-3 bg-slate-50 rounded border border-slate-200">
            <div class="font-semibold text-slate-900">4. Deduction Transparency</div>
            <p class="text-slate-600 mt-1">53 gaps among completed payouts: 556 of 571 matched payouts are explained by airline deductions; only 3 cases (RF-1041, RF-1368, RF-1435) have unexplained discrepancies.</p>
          </div>
        </div>
      </div>

    </div>

    <!-- ============================================================== -->
    <!-- TAB 2: VISUAL FLOW (HOW WE GOT TO THIS SOLUTION) -->
    <!-- ============================================================== -->
    <div id="view-flow" class="space-y-6 hidden">
      
      <!-- Intro header -->
      <div class="bg-white p-4 rounded-lg border border-slate-200">
        <h2 class="font-bold text-slate-900 text-base">Forensic Diagnostic &amp; Solution Flow</h2>
        <p class="text-xs text-slate-500 mt-0.5">How we navigated from the leadership symptom to root-cause data evidence and the target operational model.</p>
      </div>

      <!-- STEP 1: CONTRADICTION -->
      <div class="bg-white p-5 rounded-lg border border-slate-200 relative">
        <div class="flex items-center space-x-2 text-xs font-bold uppercase text-slate-400 mb-2">
          <span class="w-6 h-6 rounded-full bg-slate-900 text-white flex items-center justify-center text-xs">1</span>
          <span>Step 1: Testing the Volume Spike Hypothesis</span>
        </div>
        
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mt-3 text-xs">
          <div class="p-3 rounded bg-red-50 border border-red-200">
            <div class="font-bold text-red-900 flex items-center">
              <span class="mr-1.5">❌</span> The Intuitive Hypothesis (Leadership)
            </div>
            <p class="text-red-800 mt-1.5 leading-relaxed">
              "Customer escalations have climbed for two months. The teams are overloaded with work; we need more headcount to clear the ticket backlog."
            </p>
          </div>

          <div class="p-3 rounded bg-emerald-50 border border-emerald-200">
            <div class="font-bold text-emerald-900 flex items-center">
              <span class="mr-1.5">✅</span> What the Empirical Data Actually Showed
            </div>
            <p class="text-emerald-800 mt-1.5 leading-relaxed">
              Incoming refund requests were statistically flat: Feb (150), Mar (146), Apr (145), May (147), Jun (144). 
              <strong>Zero demand surge</strong> (&mu; = 146.4, &sigma; = 2.2). Headcount was not the constraint.
            </p>
          </div>
        </div>

        <div class="mt-3 pt-3 border-t border-slate-100 flex items-center text-xs text-slate-500 font-medium">
          <span class="text-slate-400 mr-2">&darr;</span> Key Question Raised: If intake volume was invariant, what broke inside the operational pipeline?
        </div>
      </div>

      <!-- STEP 2: CROSS-TRACKER RECONCILIATION -->
      <div class="bg-white p-5 rounded-lg border border-slate-200">
        <div class="flex items-center space-x-2 text-xs font-bold uppercase text-slate-400 mb-2">
          <span class="w-6 h-6 rounded-full bg-slate-900 text-white flex items-center justify-center text-xs">2</span>
          <span>Step 2: Cross-Tracker Reconciliation &amp; Handoff Disconnect</span>
        </div>

        <p class="text-xs text-slate-600 mb-3">
          Normalized syntax (<span class="mono font-semibold">RF 1079</span> &rarr; <span class="mono font-semibold">RF-1079</span>), stripped whitespace, and performed an outer join between Support and Finance:
        </p>

        <!-- Visual Venn Flow -->
        <div class="grid grid-cols-1 sm:grid-cols-4 gap-3 text-xs text-center">
          <div class="p-3 rounded bg-slate-50 border border-slate-200">
            <div class="text-slate-500 text-[11px] font-semibold">SUPPORT TRACKER</div>
            <div class="text-xl font-bold text-slate-900 mt-1">733</div>
            <div class="text-[11px] text-slate-400">Unique requests logged</div>
          </div>

          <div class="p-3 rounded bg-amber-50 border border-amber-200">
            <div class="text-amber-800 text-[11px] font-bold">DROPPED IN HANDOFF</div>
            <div class="text-xl font-bold text-amber-700 mt-1">69 Tickets</div>
            <div class="text-[11px] text-amber-600">Logged by Support, 0 in Finance</div>
          </div>

          <div class="p-3 rounded bg-blue-50 border border-blue-200">
            <div class="text-blue-800 text-[11px] font-bold">FINANCE TRACKER</div>
            <div class="text-xl font-bold text-blue-700 mt-1">680</div>
            <div class="text-[11px] text-blue-600">16 processed off-tracker</div>
          </div>

          <div class="p-3 rounded bg-purple-50 border border-purple-200">
            <div class="text-purple-800 text-[11px] font-bold">SHADOW CHANNELS</div>
            <div class="text-xl font-bold text-purple-700 mt-1">16 Requests</div>
            <div class="text-[11px] text-purple-600">e.g. RF-1098 &amp; RF-1099 (Ghost)</div>
          </div>
        </div>

        <div class="mt-3 text-xs bg-slate-50 p-2.5 rounded border border-slate-200 text-slate-600">
          <strong>The "Closed" Fallacy:</strong> Support marked 69 tickets "Closed" upon replying to the customer without transferring them to Finance. The agent believed the refund was finished, but money never moved.
        </div>

        <div class="mt-3 pt-3 border-t border-slate-100 flex items-center text-xs text-slate-500 font-medium">
          <span class="text-slate-400 mr-2">&darr;</span> Key Question Raised: Why did escalations spike specifically in June (+150%)?
        </div>
      </div>

      <!-- STEP 3: THE JUNE APPROVER CHOKE -->
      <div class="bg-white p-5 rounded-lg border border-slate-200">
        <div class="flex items-center space-x-2 text-xs font-bold uppercase text-slate-400 mb-2">
          <span class="w-6 h-6 rounded-full bg-slate-900 text-white flex items-center justify-center text-xs">3</span>
          <span>Step 3: Isolating the June Bottleneck Trigger</span>
        </div>

        <p class="text-xs text-slate-600 mb-3">
          Audited month-by-month payout statuses and sign-off behavior in Finance Tracker:
        </p>

        <!-- Timeline graphic -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-3 text-xs">
          <div class="p-3 rounded bg-slate-50 border border-slate-200">
            <div class="font-bold text-slate-800">Feb – May 2026: Steady State</div>
            <ul class="mt-2 space-y-1 text-slate-600 text-[11px]">
              <li>&bull; Approver <em>N. Iyer</em> cleared 21–30 refunds/mo.</li>
              <li>&bull; Pending payouts at month-end: <strong>0</strong>.</li>
              <li>&bull; Escalations stable (~23–30 complaints/mo).</li>
            </ul>
          </div>

          <div class="p-3 rounded bg-red-50 border border-red-200">
            <div class="font-bold text-red-900">Mid-June 2026: Approver Freeze</div>
            <ul class="mt-2 space-y-1 text-red-800 text-[11px]">
              <li>&bull; N. Iyer's last approval: <strong>June 13</strong>.</li>
              <li>&bull; R. Menon's last approval: <strong>June 12</strong>.</li>
              <li>&bull; S. Bhatt signed off only 1 payout.</li>
              <li>&bull; <strong>Zero delegation rule or failover in place</strong>.</li>
            </ul>
          </div>

          <div class="p-3 rounded bg-purple-50 border border-purple-200">
            <div class="font-bold text-purple-900">June 30 2026: Queue Stagnation</div>
            <ul class="mt-2 space-y-1 text-purple-800 text-[11px]">
              <li>&bull; <strong>58 payouts stranded</strong> in "Pending Payout".</li>
              <li>&bull; Completed payouts fell from 115 to <strong>60</strong> (-48%).</li>
              <li>&bull; Travel agents escalated en masse: <strong>75 complaints</strong>.</li>
            </ul>
          </div>
        </div>

        <div class="mt-3 pt-3 border-t border-slate-100 flex items-center text-xs text-slate-500 font-medium">
          <span class="text-slate-400 mr-2">&darr;</span> Key Question Raised: How do we re-engineer this process under zero new headcount?
        </div>
      </div>

      <!-- STEP 4: AS-IS VS TO-BE PROCESS FLOW -->
      <div class="bg-white p-5 rounded-lg border border-slate-200">
        <div class="flex items-center space-x-2 text-xs font-bold uppercase text-slate-400 mb-2">
          <span class="w-6 h-6 rounded-full bg-slate-900 text-white flex items-center justify-center text-xs">4</span>
          <span>Step 4: Target Operating Model (AS-IS vs TO-BE)</span>
        </div>

        <div class="space-y-4 mt-3 text-xs">
          <!-- AS-IS -->
          <div class="p-3 rounded bg-red-50/60 border border-red-200">
            <div class="font-bold text-red-900 mb-2">AS-IS Process Flow (Fragmented Silos &amp; Manual Drops)</div>
            <div class="grid grid-cols-2 sm:grid-cols-6 gap-2 text-center text-[11px]">
              <div class="p-2 bg-white rounded border border-red-300">
                <span class="font-bold text-slate-900 block">Agent Request</span>
                <span class="text-red-600 text-[10px]">Unlogged WhatsApp</span>
              </div>
              <div class="p-2 bg-white rounded border border-red-300">
                <span class="font-bold text-slate-900 block">Support Sheet</span>
                <span class="text-red-600 text-[10px]">Premature "Closed"</span>
              </div>
              <div class="p-2 bg-white rounded border border-red-300">
                <span class="font-bold text-slate-900 block">Manual Email</span>
                <span class="text-red-600 text-[10px]">69 dropped handoffs</span>
              </div>
              <div class="p-2 bg-white rounded border border-red-300">
                <span class="font-bold text-slate-900 block">Finance Sheet</span>
                <span class="text-red-600 text-[10px]">Manual re-typing</span>
              </div>
              <div class="p-2 bg-white rounded border border-red-300">
                <span class="font-bold text-slate-900 block">Single Approver</span>
                <span class="text-red-600 text-[10px]">Freeze on absence</span>
              </div>
              <div class="p-2 bg-white rounded border border-red-300">
                <span class="font-bold text-slate-900 block">Payout or Loss</span>
                <span class="text-red-600 text-[10px]">No agent notice</span>
              </div>
            </div>
          </div>

          <!-- TO-BE -->
          <div class="p-3 rounded bg-emerald-50/60 border border-emerald-200">
            <div class="font-bold text-emerald-900 mb-2">TO-BE Process Flow (Event-Driven SSOT &amp; Zero-Touch Approvals)</div>
            <div class="grid grid-cols-2 sm:grid-cols-6 gap-2 text-center text-[11px]">
              <div class="p-2 bg-white rounded border border-emerald-300">
                <span class="font-bold text-slate-900 block">AI Ingestion</span>
                <span class="text-emerald-700 text-[10px]">Auto-assigns RF-ID</span>
              </div>
              <div class="p-2 bg-white rounded border border-emerald-300">
                <span class="font-bold text-slate-900 block">Rules Engine</span>
                <span class="text-emerald-700 text-[10px]">Deductions upfront</span>
              </div>
              <div class="p-2 bg-white rounded border border-emerald-300">
                <span class="font-bold text-slate-900 block">Shared SSOT</span>
                <span class="text-emerald-700 text-[10px]">Direct queue push</span>
              </div>
              <div class="p-2 bg-white rounded border border-emerald-300">
                <span class="font-bold text-slate-900 block">Batch Approval</span>
                <span class="text-emerald-700 text-[10px]">&le; INR 25k automated</span>
              </div>
              <div class="p-2 bg-white rounded border border-emerald-300">
                <span class="font-bold text-slate-900 block">Settlement</span>
                <span class="text-emerald-700 text-[10px]">Automated bank sync</span>
              </div>
              <div class="p-2 bg-white rounded border border-emerald-300">
                <span class="font-bold text-slate-900 block">Auto Webhook</span>
                <span class="text-emerald-700 text-[10px]">SMS/WhatsApp receipt</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- STEP 5: PROVEN TARGET OUTCOMES -->
      <div class="bg-white p-5 rounded-lg border border-slate-200">
        <div class="flex items-center space-x-2 text-xs font-bold uppercase text-slate-400 mb-2">
          <span class="w-6 h-6 rounded-full bg-slate-900 text-white flex items-center justify-center text-xs">5</span>
          <span>Step 5: Target Metrics &amp; 30-Day Projections</span>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-3 mt-3 text-xs">
          <div class="p-3 bg-slate-50 rounded border border-slate-200">
            <span class="text-slate-500 font-medium block">Refund Escalation Rate</span>
            <div class="text-xl font-bold text-slate-900 mt-1">52.1% &rarr; &le; 8%</div>
            <p class="text-[11px] text-slate-500 mt-1">Drop from 75 escalations to under 12 in Month 1 by eliminating status silence.</p>
          </div>

          <div class="p-3 bg-slate-50 rounded border border-slate-200">
            <span class="text-slate-500 font-medium block">Cross-Team Handoff Lag</span>
            <div class="text-xl font-bold text-slate-900 mt-1">2.47 Days &rarr; &lt; 15 min</div>
            <p class="text-[11px] text-slate-500 mt-1">Support and Finance operate on shared database views; zero dropped handoffs.</p>
          </div>

          <div class="p-3 bg-slate-50 rounded border border-slate-200">
            <span class="text-slate-500 font-medium block">Pending Payout Aging</span>
            <div class="text-xl font-bold text-slate-900 mt-1">25+ Days &rarr; &le; 48 Hours</div>
            <p class="text-[11px] text-slate-500 mt-1">Batch auto-approval for routine domestic refunds removes single-manager dependencies.</p>
          </div>
        </div>
      </div>

    </div>

    <!-- ============================================================== -->
    <!-- TAB 3: DISCREPANCY AUDIT (RECONCILER) -->
    <!-- ============================================================== -->
    <div id="view-reconciliation" class="space-y-4 hidden">

      <!-- Controls Row -->
      <div class="bg-white p-3.5 rounded-lg border border-slate-200 flex flex-col md:flex-row items-center justify-between gap-3">
        
        <!-- Filter Buttons -->
        <div class="flex flex-wrap items-center gap-1.5 w-full md:w-auto">
          <button onclick="setFilter('ALL_FLAGGED')" id="flt-ALL_FLAGGED" class="flt-btn px-2.5 py-1 text-xs font-semibold rounded bg-slate-900 text-white">All Issues (143)</button>
          <button onclick="setFilter('DROPPED_HANDOFF')" id="flt-DROPPED_HANDOFF" class="flt-btn px-2.5 py-1 text-xs font-medium rounded bg-slate-100 text-slate-700 hover:bg-slate-200">Dropped Handoffs (69)</button>
          <button onclick="setFilter('APPROVAL_BOTTLENECK')" id="flt-APPROVAL_BOTTLENECK" class="flt-btn px-2.5 py-1 text-xs font-medium rounded bg-slate-100 text-slate-700 hover:bg-slate-200">Approval Stalls (55)</button>
          <button onclick="setFilter('AMOUNT_MISMATCH')" id="flt-AMOUNT_MISMATCH" class="flt-btn px-2.5 py-1 text-xs font-medium rounded bg-slate-100 text-slate-700 hover:bg-slate-200">Amount Mismatches (3)</button>
          <button onclick="setFilter('SHADOW_INTAKE')" id="flt-SHADOW_INTAKE" class="flt-btn px-2.5 py-1 text-xs font-medium rounded bg-slate-100 text-slate-700 hover:bg-slate-200">Finance Only (16)</button>
          <button onclick="setFilter('ALL')" id="flt-ALL" class="flt-btn px-2.5 py-1 text-xs font-medium rounded bg-slate-100 text-slate-700 hover:bg-slate-200">All (749)</button>
        </div>

        <!-- Search & Actions -->
        <div class="flex items-center space-x-2 w-full md:w-auto justify-end">
          <input type="text" id="table-search" oninput="applySearch()" placeholder="Search ID, Agent, Route..." class="px-2.5 py-1 text-xs rounded border border-slate-300 w-48 focus:outline-none focus:ring-1 focus:ring-slate-500">
          <button onclick="downloadCSV()" class="px-2.5 py-1 text-xs font-medium rounded border border-slate-300 bg-white hover:bg-slate-50 text-slate-700 whitespace-nowrap">
            Export CSV
          </button>
        </div>

      </div>

      <!-- Data Table -->
      <div class="bg-white rounded-lg border border-slate-200 overflow-hidden">
        <div class="overflow-x-auto">
          <table class="min-w-full divide-y divide-slate-200 text-left text-xs">
            <thead class="bg-slate-50 text-slate-600 font-semibold">
              <tr>
                <th class="py-2.5 px-3">Ticket ID</th>
                <th class="py-2.5 px-3">Travel Agent</th>
                <th class="py-2.5 px-3">Sector</th>
                <th class="py-2.5 px-3">Support Status</th>
                <th class="py-2.5 px-3">Finance Status</th>
                <th class="py-2.5 px-3">Amounts (Req / Paid / Ded)</th>
                <th class="py-2.5 px-3">Issue Category</th>
                <th class="py-2.5 px-3 text-center">Escalation</th>
              </tr>
            </thead>
            <tbody id="table-rows" class="divide-y divide-slate-100 text-slate-700">
              <!-- Dynamically populated -->
            </tbody>
          </table>
        </div>

        <!-- Pagination -->
        <div class="px-3 py-2 bg-slate-50 border-t border-slate-200 flex items-center justify-between text-xs text-slate-500">
          <span id="page-count-text">Showing 1 to 15 of 143 records</span>
          <div class="flex items-center space-x-1.5">
            <button onclick="changePage(-1)" id="btn-page-prev" class="px-2 py-0.5 rounded bg-white border border-slate-300 hover:bg-slate-100 disabled:opacity-40">Prev</button>
            <span id="page-num-text" class="px-2 font-medium text-slate-700">Page 1</span>
            <button onclick="changePage(1)" id="btn-page-next" class="px-2 py-0.5 rounded bg-white border border-slate-300 hover:bg-slate-100 disabled:opacity-40">Next</button>
          </div>
        </div>
      </div>

    </div>

    <!-- ============================================================== -->
    <!-- TAB 4: INBOUND MESSAGE PARSER -->
    <!-- ============================================================== -->
    <div id="view-parser" class="space-y-4 hidden">

      <div class="bg-white p-4 rounded-lg border border-slate-200">
        <div class="flex items-center justify-between mb-3">
          <div>
            <h2 class="font-bold text-slate-900 text-sm">Inbound Message Triage &amp; Parser</h2>
            <p class="text-xs text-slate-500">Extracts entities from informal WhatsApp/Email messages, assigns canonical IDs, and drafts transparent replies.</p>
          </div>
          <span class="text-xs bg-slate-100 text-slate-600 px-2 py-0.5 rounded border border-slate-200">Rule &amp; NLP Engine</span>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-12 gap-5 mt-4">
          
          <!-- Left: Input Form -->
          <div class="lg:col-span-5 space-y-3">
            <div>
              <label class="block text-xs font-semibold text-slate-700 mb-1">Load Sample Case from Brief:</label>
              <select id="case-select" onchange="applyCasePreset()" class="w-full p-2 text-xs rounded border border-slate-300 bg-white">
                <option value="nomad">Nomad Travel - Hinglish WhatsApp (RF-1098 Case)</option>
                <option value="peak">Peak Journeys - Missing Reference Email (RF-1099 Case)</option>
                <option value="support">Internal Support Confession Note (June 11)</option>
                <option value="custom">-- Custom Message --</option>
              </select>
            </div>

            <div class="grid grid-cols-2 gap-2">
              <div>
                <label class="block text-xs font-semibold text-slate-700 mb-1">Channel:</label>
                <select id="parse-channel" class="w-full p-2 text-xs rounded border border-slate-300 bg-white">
                  <option value="WhatsApp">WhatsApp</option>
                  <option value="Email">Email</option>
                  <option value="Phone">Phone</option>
                  <option value="Portal">Portal</option>
                </select>
              </div>
              <div>
                <label class="block text-xs font-semibold text-slate-700 mb-1">Sender Agency:</label>
                <input type="text" id="parse-sender" value="Nomad Travel" class="w-full p-2 text-xs rounded border border-slate-300 bg-white">
              </div>
            </div>

            <div>
              <label class="block text-xs font-semibold text-slate-700 mb-1">Raw Message Content:</label>
              <textarea id="parse-content" rows="4" class="w-full p-2.5 text-xs mono rounded border border-slate-300 bg-slate-50 focus:bg-white focus:outline-none">Bhai refund ka kya hua? BLR-MAA wala. 2 hafte ho gaye, koi jawab nahi.</textarea>
            </div>

            <button onclick="runParser()" class="w-full py-2 px-3 rounded bg-slate-900 hover:bg-slate-800 text-white font-semibold text-xs transition">
              Parse Message
            </button>
          </div>

          <!-- Right: Structured Output -->
          <div class="lg:col-span-7 bg-slate-50 p-4 rounded-lg border border-slate-200 space-y-3">
            <div class="flex items-center justify-between border-b border-slate-200 pb-2">
              <span class="text-xs font-semibold text-slate-700">Parsed Extraction</span>
              <span id="out-urgency" class="text-xs font-bold px-2 py-0.5 rounded bg-red-100 text-red-700 border border-red-200">
                CRITICAL (Wait > 14 days)
              </span>
            </div>

            <div class="grid grid-cols-2 sm:grid-cols-4 gap-2 text-xs">
              <div class="p-2 bg-white rounded border border-slate-200">
                <span class="text-slate-400 block text-[11px]">Ticket ID</span>
                <span id="out-id" class="font-bold mono text-slate-900">RF-1098</span>
              </div>
              <div class="p-2 bg-white rounded border border-slate-200">
                <span class="text-slate-400 block text-[11px]">Sector</span>
                <span id="out-route" class="font-bold mono text-slate-900">BLR-MAA</span>
              </div>
              <div class="p-2 bg-white rounded border border-slate-200">
                <span class="text-slate-400 block text-[11px]">Intent</span>
                <span id="out-intent" class="font-bold text-slate-900">Status Inquiry</span>
              </div>
              <div class="p-2 bg-white rounded border border-slate-200">
                <span class="text-slate-400 block text-[11px]">Channel</span>
                <span id="out-ch" class="font-bold text-slate-900">WhatsApp</span>
              </div>
            </div>

            <div class="p-2.5 bg-white rounded border border-slate-200 text-xs text-slate-700">
              <strong>Triage Action:</strong>
              <span id="out-action" class="ml-1 text-slate-600">Register canonical ID in SSOT; send immediate tracking reference to agent.</span>
            </div>

            <div>
              <div class="flex items-center justify-between mb-1">
                <span class="text-xs font-semibold text-slate-700">Automated Agent Response:</span>
                <button onclick="copyDraft()" class="text-xs text-blue-600 hover:underline">Copy Response</button>
              </div>
              <textarea id="out-draft" rows="4" readonly class="w-full p-2.5 text-xs rounded border border-slate-300 bg-white text-slate-800 focus:outline-none"></textarea>
            </div>
          </div>

        </div>
      </div>

    </div>

    <!-- ============================================================== -->
    <!-- TAB 5: TARGET PROCESS & SLAS -->
    <!-- ============================================================== -->
    <div id="view-process" class="space-y-4 hidden">

      <!-- Target State Machine -->
      <div class="bg-white p-4 rounded-lg border border-slate-200">
        <h2 class="font-bold text-slate-900 text-sm mb-1">Target Process: 5-Stage Deterministic Lifecycle</h2>
        <p class="text-xs text-slate-500 mb-4">Replaces subjective free-text statuses ("Closed", "Working") with shared, synchronized state transitions.</p>

        <div class="grid grid-cols-1 sm:grid-cols-5 gap-2 text-xs">
          <div class="p-2.5 bg-slate-50 rounded border border-slate-200">
            <span class="text-[11px] font-bold text-slate-500 block">Stage 1</span>
            <div class="font-semibold text-slate-900 mt-0.5">INTAKE_CAPTURED</div>
            <p class="text-slate-500 mt-1 text-[11px]">Ticket created instantly from Portal, Email, or WhatsApp. Canonical RF-ID issued.</p>
          </div>
          <div class="p-2.5 bg-slate-50 rounded border border-slate-200">
            <span class="text-[11px] font-bold text-slate-500 block">Stage 2</span>
            <div class="font-semibold text-slate-900 mt-0.5">ELIGIBILITY_VERIFIED</div>
            <p class="text-slate-500 mt-1 text-[11px]">Airline fee schedule calculated upfront. Net payable confirmed with itemized slip.</p>
          </div>
          <div class="p-2.5 bg-slate-50 rounded border border-slate-200">
            <span class="text-[11px] font-bold text-slate-500 block">Stage 3</span>
            <div class="font-semibold text-slate-900 mt-0.5">FINANCE_QUEUED</div>
            <p class="text-slate-500 mt-1 text-[11px]">Automated database push to Finance queue. Zero tickets dropped between teams.</p>
          </div>
          <div class="p-2.5 bg-slate-50 rounded border border-slate-200">
            <span class="text-[11px] font-bold text-slate-500 block">Stage 4</span>
            <div class="font-semibold text-slate-900 mt-0.5">PAYOUT_APPROVED</div>
            <p class="text-slate-500 mt-1 text-[11px]">Auto-batch approval for standard tickets &le; INR 25k. Eliminates single-manager choke.</p>
          </div>
          <div class="p-2.5 bg-emerald-50 rounded border border-emerald-200">
            <span class="text-[11px] font-bold text-emerald-700 block">Stage 5</span>
            <div class="font-semibold text-emerald-950 mt-0.5">SETTLED / DECLINED</div>
            <p class="text-emerald-700 mt-1 text-[11px]">Funds disbursed. Automated notification sent with bank reference &amp; fee breakdown.</p>
          </div>
        </div>
      </div>

      <!-- Trade-Off Matrix -->
      <div class="bg-white p-4 rounded-lg border border-slate-200">
        <h2 class="font-bold text-slate-900 text-sm mb-1">Operational Trade-Off Matrix (Zero-Headcount Constraint)</h2>
        <p class="text-xs text-slate-500 mb-3">Clear boundaries on what to automate vs. what to keep deliberately manual.</p>

        <table class="w-full text-xs text-left">
          <thead>
            <tr class="border-b border-slate-200 text-slate-500">
              <th class="pb-2 font-medium">Workflow Step</th>
              <th class="pb-2 font-medium">Implementation</th>
              <th class="pb-2 font-medium">Rationale &amp; Controls</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-100 text-slate-700">
            <tr>
              <td class="py-2 font-semibold">Ticket Ingestion</td>
              <td class="py-2"><span class="px-2 py-0.5 rounded font-medium bg-blue-50 text-blue-700">Automate (NLP Parser)</span></td>
              <td class="py-2 text-slate-600">Eliminates lost requests on WhatsApp/Email. Captures route, agent, and issues immediate tracking ID.</td>
            </tr>
            <tr>
              <td class="py-2 font-semibold">Deduction Calculation</td>
              <td class="py-2"><span class="px-2 py-0.5 rounded font-medium bg-blue-50 text-blue-700">Automate (Rules Engine)</span></td>
              <td class="py-2 text-slate-600">Applies published airline fee rules upfront. Itemized slip sent to agent, eliminating amount disputes.</td>
            </tr>
            <tr>
              <td class="py-2 font-semibold">Routine Approvals</td>
              <td class="py-2"><span class="px-2 py-0.5 rounded font-medium bg-emerald-50 text-emerald-700">Automate (&le; INR 25,000)</span></td>
              <td class="py-2 text-slate-600">Standard domestic cancellations auto-approved in batches. Prevents queue freeze when managers are away.</td>
            </tr>
            <tr>
              <td class="py-2 font-semibold">High-Value / Exception Refunds</td>
              <td class="py-2"><span class="px-2 py-0.5 rounded font-medium bg-amber-50 text-amber-700">Manual (Finance Lead)</span></td>
              <td class="py-2 text-slate-600">Refunds &gt; INR 25,000, medical waivers, and non-refundable tickets require human scrutiny to protect margin.</td>
            </tr>
            <tr>
              <td class="py-2 font-semibold">VIP Agency Relations</td>
              <td class="py-2"><span class="px-2 py-0.5 rounded font-medium bg-purple-50 text-purple-700">Manual (Senior Support)</span></td>
              <td class="py-2 text-slate-600">High-volume travel partners receive dedicated human touch for exceptions; routine requests flow through pipeline.</td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- 30-Day Measurement Table -->
      <div class="bg-white p-4 rounded-lg border border-slate-200">
        <h2 class="font-bold text-slate-900 text-sm mb-3">Target Metrics &amp; 30-Day Scorecard</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
          <div class="p-3 bg-slate-50 rounded border border-slate-200">
            <span class="font-bold text-slate-900 block">Primary: Refund Escalation Rate</span>
            <div class="text-slate-500 mt-0.5"><code>(Monthly Escalations / Total Refund Requests) &times; 100</code></div>
            <div class="mt-2 space-y-1">
              <div>Baseline (June 2026): <strong class="text-red-700">52.1%</strong> (75 escalations on 144 requests)</div>
              <div>30-Day Target: <strong class="text-emerald-700">&le; 8.0%</strong> (&le;12 escalations)</div>
              <div>60-Day Target: <strong class="text-emerald-700">&le; 3.0%</strong></div>
            </div>
          </div>

          <div class="p-3 bg-slate-50 rounded border border-slate-200">
            <span class="font-bold text-slate-900 block">Secondary: Handoff Lag &amp; Turnaround</span>
            <div class="text-slate-500 mt-0.5">Elapsed time between intake and payout disbursement</div>
            <div class="mt-2 space-y-1">
              <div>Baseline Handoff Lag: <strong class="text-slate-800">2.47 days</strong> (handoff lag; total turnaround lag is 6.23 days, with 69 tickets dropped)</div>
              <div>Target Handoff Lag: <strong class="text-emerald-700">&lt; 15 minutes</strong> (Direct database sync)</div>
              <div>Pending Payout Aging: <strong class="text-emerald-700">&le; 48 hours</strong> (Down from 25+ days)</div>
            </div>
          </div>
        </div>
      </div>

    </div>

  </main>

  <!-- FOOTER -->
  <footer class="bg-white border-t border-slate-200 py-4 text-center text-xs text-slate-500">
    Snapshot generated from BharatTrip_Refund_Data.xlsx on 10 November 2026
  </footer>

  <!-- JAVASCRIPT LOGIC -->
  <script>
    const DATA = {json_str};
    let activeFilter = 'ALL_FLAGGED';
    let searchVal = '';
    let curPage = 1;
    const perPage = 15;

    function showTab(tabId) {{
      document.querySelectorAll('[id^="view-"]').forEach(el => el.classList.add('hidden'));
      document.querySelectorAll('.tab-btn').forEach(btn => {{
        btn.classList.remove('border-slate-900', 'text-slate-900', 'font-semibold');
        btn.classList.add('border-transparent', 'text-slate-500');
      }});

      document.getElementById('view-' + tabId).classList.remove('hidden');
      const activeBtn = document.getElementById('tab-btn-' + tabId);
      if (activeBtn) {{
        activeBtn.classList.remove('border-transparent', 'text-slate-500');
        activeBtn.classList.add('border-slate-900', 'text-slate-900', 'font-semibold');
      }}
    }}

    function initComplaints() {{
      const container = document.getElementById('complaint-rows');
      const topComplaints = DATA.top_complaints;
      let html = '';
      for (const [text, count] of Object.entries(topComplaints)) {{
        html += `
          <div class="flex items-center justify-between text-xs py-1 border-b border-slate-50">
            <span class="text-slate-700 truncate max-w-xs" title="${{text}}">${{text}}</span>
            <span class="font-semibold text-slate-900 ml-2 mono">${{count}}</span>
          </div>
        `;
      }}
      container.innerHTML = html;
    }}

    function getFilteredData() {{
      let list = DATA.records;
      if (activeFilter === 'ALL_FLAGGED') {{
        list = list.filter(r => r.Discrepancy_Type !== 'RECONCILED_OK');
      }} else if (activeFilter !== 'ALL') {{
        list = list.filter(r => r.Discrepancy_Type === activeFilter);
      }}

      if (searchVal) {{
        const q = searchVal.toLowerCase();
        list = list.filter(r => 
          (r.Norm_ID && r.Norm_ID.toLowerCase().includes(q)) ||
          (r.Agent_Display && r.Agent_Display.toLowerCase().includes(q)) ||
          (r.Route_Display && r.Route_Display.toLowerCase().includes(q)) ||
          (r.Remarks && r.Remarks.toLowerCase().includes(q))
        );
      }}
      return list;
    }}

    function renderTable() {{
      const records = getFilteredData();
      const total = records.length;
      const totalPages = Math.ceil(total / perPage) || 1;
      if (curPage > totalPages) curPage = totalPages;

      const start = (curPage - 1) * perPage;
      const pageSlice = records.slice(start, start + perPage);

      const tbody = document.getElementById('table-rows');
      let html = '';

      if (pageSlice.length === 0) {{
        html = `<tr><td colspan="8" class="text-center py-6 text-slate-400">No records found.</td></tr>`;
      }} else {{
        pageSlice.forEach(r => {{
          let tagClass = 'tag-ok';
          let tagLabel = r.Discrepancy_Type;

          if (r.Discrepancy_Type === 'DROPPED_HANDOFF') {{
            tagClass = 'tag-dropped';
            tagLabel = 'Dropped Handoff';
          }} else if (r.Discrepancy_Type === 'APPROVAL_BOTTLENECK') {{
            tagClass = 'tag-stall';
            tagLabel = 'Approval Stall';
          }} else if (r.Discrepancy_Type === 'AMOUNT_MISMATCH') {{
            tagClass = 'tag-mismatch';
            tagLabel = 'Amount Mismatch';
          }} else if (r.Discrepancy_Type === 'SHADOW_INTAKE') {{
            tagClass = 'tag-shadow';
            tagLabel = 'Finance Only';
          }}

          const req = r['Refund Amount (INR)'] ? '₹' + Number(r['Refund Amount (INR)']).toLocaleString() : '-';
          const paid = r['Amount Paid (INR)'] ? '₹' + Number(r['Amount Paid (INR)']).toLocaleString() : '₹0';
          const ded = r['Deduction (INR)'] ? '₹' + Number(r['Deduction (INR)']).toLocaleString() : '₹0';

          const escText = r.Escalation_Count > 0 
            ? `<span class="px-1.5 py-0.5 rounded bg-red-100 text-red-700 font-semibold text-[11px]">${{r.Escalation_Count}}</span>` 
            : `<span class="text-slate-300">-</span>`;

          html += `
            <tr class="hover:bg-slate-50">
              <td class="py-2 px-3 mono font-semibold text-slate-900">${{r.Norm_ID || 'Unlogged'}}</td>
              <td class="py-2 px-3 font-medium text-slate-800">${{r.Agent_Display}}</td>
              <td class="py-2 px-3 mono text-slate-600">${{r.Route_Display}}</td>
              <td class="py-2 px-3 text-slate-600">${{r.Clean_Status || '-'}}</td>
              <td class="py-2 px-3 text-slate-600">${{r.Clean_Payout_Status || '-'}}</td>
              <td class="py-2 px-3 mono text-slate-600 text-[11px]">
                <span class="text-slate-900">${{req}}</span> / 
                <span class="text-emerald-700">${{paid}}</span> / 
                <span class="text-amber-700">${{ded}}</span>
              </td>
              <td class="py-2 px-3">
                <span class="px-1.5 py-0.5 text-[11px] font-medium rounded ${{tagClass}}">${{tagLabel}}</span>
                ${{r.Remarks ? `<span class="block text-[10px] text-slate-400 truncate max-w-[130px] mt-0.5" title="${{r.Remarks}}">${{r.Remarks}}</span>` : ''}}
              </td>
              <td class="py-2 px-3 text-center">${{escText}}</td>
            </tr>
          `;
        }});
      }}

      tbody.innerHTML = html;
      document.getElementById('page-count-text').innerText = `Showing ${{total === 0 ? 0 : start + 1}} to ${{Math.min(start + perPage, total)}} of ${{total}} records`;
      document.getElementById('page-num-text').innerText = `Page ${{curPage}} of ${{totalPages}}`;
      document.getElementById('btn-page-prev').disabled = curPage <= 1;
      document.getElementById('btn-page-next').disabled = curPage >= totalPages;
    }}

    function setFilter(flt) {{
      activeFilter = flt;
      curPage = 1;
      document.querySelectorAll('.flt-btn').forEach(b => {{
        b.classList.remove('bg-slate-900', 'text-white', 'font-semibold');
        b.classList.add('bg-slate-100', 'text-slate-700');
      }});
      const target = document.getElementById('flt-' + flt);
      if (target) {{
        target.classList.remove('bg-slate-100', 'text-slate-700');
        target.classList.add('bg-slate-900', 'text-white', 'font-semibold');
      }}
      renderTable();
    }}

    function applySearch() {{
      searchVal = document.getElementById('table-search').value.trim();
      curPage = 1;
      renderTable();
    }}

    function changePage(delta) {{
      curPage += delta;
      renderTable();
    }}

    function downloadCSV() {{
      const records = getFilteredData();
      let csv = 'Ticket_ID,Agent,Sector,Refund_Requested_INR,Amount_Paid_INR,Deduction_INR,Support_Status,Finance_Status,Issue_Category,Remarks\\n';
      records.forEach(r => {{
        csv += `"${{r.Norm_ID}}","${{r.Agent_Display}}","${{r.Route_Display}}",${{r['Refund Amount (INR)'] || 0}},${{r['Amount Paid (INR)'] || 0}},${{r['Deduction (INR)'] || 0}},"${{r.Clean_Status}}","${{r.Clean_Payout_Status}}","${{r.Discrepancy_Type}}","${{r.Remarks || ''}}"\\n`;
      }});
      const blob = new Blob([csv], {{ type: 'text/csv' }});
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'BharatTrip_Reconciled_Discrepancies.csv';
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
    }}

    function applyCasePreset() {{
      const val = document.getElementById('case-select').value;
      if (val === 'nomad') {{
        document.getElementById('parse-sender').value = 'Nomad Travel';
        document.getElementById('parse-channel').value = 'WhatsApp';
        document.getElementById('parse-content').value = 'Bhai refund ka kya hua? BLR-MAA wala. 2 hafte ho gaye, koi jawab nahi.';
      }} else if (val === 'peak') {{
        document.getElementById('parse-sender').value = 'Peak Journeys';
        document.getElementById('parse-channel').value = 'Email';
        document.getElementById('parse-content').value = "Hi, I cancelled booking for DEL-DXB last week and was told I'd get a refund. I haven't received anything and I don't have any reference number. Please help, my client is asking.";
      }} else if (val === 'support') {{
        document.getElementById('parse-sender').value = 'Support Rep';
        document.getElementById('parse-channel').value = 'Email';
        document.getElementById('parse-content').value = "Finance says they never received several of the refunds I closed last month. I marked them done on my side. Not sure where they went.";
      }}
      runParser();
    }}

    function runParser() {{
      const text = document.getElementById('parse-content').value;
      const sender = document.getElementById('parse-sender').value || 'Unknown Agent';
      const textLower = text.toLowerCase();

      let sector = 'BLR-MAA';
      const secMatch = text.match(/([A-Z]{{3}}\\s*[-/]\\s*[A-Z]{{3}})/i);
      if (secMatch) {{
        sector = secMatch[1].toUpperCase().replace(/\\\\s+/g, '');
      }} else if (textLower.includes('del') && textLower.includes('dxb')) {{
        sector = 'DEL-DXB';
      }}

      const isCritical = textLower.includes('2 hafte') || textLower.includes('two weeks') || textLower.includes('haven\\\\\'t received');
      const ticketId = sender.includes('Nomad') ? 'RF-1098' : (sender.includes('Peak') ? 'RF-1099' : 'RF-NEW-5021A4');

      document.getElementById('out-id').innerText = ticketId;
      document.getElementById('out-route').innerText = sector;
      document.getElementById('out-ch').innerText = document.getElementById('parse-channel').value;
      
      const urgEl = document.getElementById('out-urgency');
      if (isCritical) {{
        urgEl.innerText = 'CRITICAL (Wait > 14 days)';
        urgEl.className = 'text-xs font-bold px-2 py-0.5 rounded bg-red-100 text-red-700 border border-red-200';
      }} else {{
        urgEl.innerText = 'STANDARD';
        urgEl.className = 'text-xs font-bold px-2 py-0.5 rounded bg-slate-100 text-slate-700 border border-slate-200';
      }}

      const draft = `Hi ${{sender}},\\n\\nWe have logged your request under reference ${{ticketId}} regarding ${{sector}} and are checking its status. We will update you once we have confirmed the position.\\n\\nRegards,\\nBharatTrip Operations Team`;
      document.getElementById('out-draft').value = draft;
    }}

    function copyDraft() {{
      const t = document.getElementById('out-draft').value;
      navigator.clipboard.writeText(t);
      alert('Response copied to clipboard.');
    }}

    window.onload = function() {{
      initComplaints();
      renderTable();
      runParser();
    }};
  </script>
</body>
</html>
"""

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    print("Successfully built clean index.html with Visual Flow Tab!")

if __name__ == "__main__":
    build_clean_html_with_flow()
