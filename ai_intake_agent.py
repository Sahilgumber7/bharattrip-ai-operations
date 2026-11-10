"""
BharatTrip AI Omnichannel Intake & Triage Agent
Author: AI Operations Associate Candidate
Purpose: Ingest messy unstructured messages (Email, WhatsApp, Chat),
         extract structured entities, assign canonical RF-IDs, calculate policy deductions,
         and generate instant proactive responses to prevent escalations.
"""

import re
import json
import hashlib
from datetime import datetime

class RefundIntakeAgent:
    def __init__(self):
        # Known travel agents from historical database
        self.known_agents = [
            "Peak Journeys", "Nomad Travel", "TripHub", "BlueJet Tours",
            "Metro Yatra", "GoFly Holidays", "Wander Agency", "Sunrise Trips",
            "Skyline Travels", "Orbit Travels", "Coral Voyages", "Voyage Desk",
            "Global Wings", "Himalaya Holidays", "Kaveri Tours", "SafarNama Travel",
            "Yatri Junction", "DeccanFly", "Lotus Travel Co", "Anand Travels", "Pinnacle Getaways"
        ]

    def parse_message(self, text, channel="WhatsApp", sender=""):
        """
        Parses unstructured incoming message text into structured ticket entities.
        Works across English and Hinglish / colloquial travel agent vernacular.
        """
        text_lower = text.lower()

        # 1. Detect Agent Name
        detected_agent = "Unknown Agent"
        if sender and sender != "Unknown":
            detected_agent = sender
        else:
            for ag in self.known_agents:
                if ag.lower() in text_lower:
                    detected_agent = ag
                    break

        # 2. Detect Route / Sector (e.g. DEL-DXB, BLR-MAA, BOM-GOI, etc.)
        sector_match = re.search(r'([A-Z]{3}\s*[-/]\s*[A-Z]{3})', text.upper())
        detected_sector = sector_match.group(1).replace(" ", "") if sector_match else "Unspecified"

        # 3. Detect Reference Number if mentioned
        ref_match = re.search(r'RF\s*[-]?\s*(\d+)', text.upper())
        detected_ref = f"RF-{ref_match.group(1)}" if ref_match else None

        # 4. Intent Classification
        is_status_followup = any(w in text_lower for w in [
            "kya hua", "status", "update", "chasing", "follow up", "follow-up",
            "koi jawab nahi", "haven't received", "havent received", "not received",
            "still waiting", "2 hafte", "two weeks", "where is", "kab aayega"
        ])

        is_dispute = any(w in text_lower for w in [
            "less than", "short payment", "wrong amount", "deduction", "diff",
            "mismatch", "promised", "quoted", "two different figures"
        ])

        if is_dispute:
            intent = "AMOUNT_DISPUTE"
        elif is_status_followup:
            intent = "STATUS_FOLLOWUP"
        else:
            intent = "NEW_REFUND_REQUEST"

        # 5. Urgency & Escalation Risk Scoring (0 - 100)
        risk_score = 20
        risk_factors = []

        if any(w in text_lower for w in ["2 hafte", "two weeks", "weeks ago", "month ago", "last month"]):
            risk_score += 40
            risk_factors.append("Extended wait time (>2 weeks)")
        
        if any(w in text_lower for w in ["client asking", "customer angry", "urgent", "loss", "bhai", "please help"]):
            risk_score += 25
            risk_factors.append("Client pressure / relationship distress")

        if not detected_ref and is_status_followup:
            risk_score += 20
            risk_factors.append("Unlogged shadow request (Missing RF ID)")

        urgency_level = "CRITICAL" if risk_score >= 70 else "HIGH" if risk_score >= 50 else "MEDIUM" if risk_score >= 30 else "LOW"

        # 6. Extract Amount if mentioned
        amt_match = re.search(r'(?:rs\.?|inr|₹)?\s*(\d{3,6})', text_lower)
        estimated_amount = float(amt_match.group(1)) if amt_match else None

        # Standard Policy Deduction heuristic (e.g. airline cancellation ₹3000 + agency processing fee ₹500)
        standard_deduction = 3500.0 if (estimated_amount and estimated_amount > 5000) else 0.0
        net_payable = (estimated_amount - standard_deduction) if estimated_amount else None

        # Assign canonical unique ID if unlogged (deterministic 6 uppercase hex chars based on text)
        if detected_ref:
            assigned_id = detected_ref
        else:
            suffix = hashlib.sha256(text.strip().encode("utf-8")).hexdigest()[:6].upper()
            assigned_id = f"RF-NEW-{suffix}"

        # 7. Generate Proactive Response
        response_draft = self._generate_response(
            agent=detected_agent,
            ref_id=assigned_id,
            sector=detected_sector,
            intent=intent,
            urgency=urgency_level,
            channel=channel
        )

        return {
            "ticket_id": assigned_id,
            "agent": detected_agent,
            "sector": detected_sector,
            "intent": intent,
            "urgency": urgency_level,
            "risk_score": min(risk_score, 100),
            "risk_factors": risk_factors,
            "channel": channel,
            "raw_text": text,
            "estimated_gross_inr": estimated_amount,
            "estimated_deduction_inr": standard_deduction,
            "estimated_net_payable_inr": net_payable,
            "recommended_action": self._recommended_action(intent, urgency_level, detected_ref),
            "proactive_response_draft": response_draft
        }

    def _recommended_action(self, intent, urgency, has_ref):
        if not has_ref:
            return "INSTANT_LOG_AND_CONFIRM: Log canonical RF-ID into SSOT, notify agent immediately with tracking reference."
        if intent == "STATUS_FOLLOWUP" and urgency == "CRITICAL":
            return "PRIORITY_FINANCE_PING: Flag to Finance lead on Slack/Queue for immediate payout batch execution."
        if intent == "AMOUNT_DISPUTE":
            return "POLICY_BREAKDOWN_SEND: Send automated itemized tax & airline cancellation fee calculation."
        return "STANDARD_PIPELINE: Ingest into Finance processing queue."

    def _generate_response(self, agent, ref_id, sector, intent, urgency, channel):
        greeting = f"Hi {agent}," if agent != "Unknown Agent" else "Hello,"
        sector_str = f" for route {sector}" if sector != "Unspecified" else ""

        return (
            f"{greeting}\n\n"
            f"We have logged your request{sector_str} under reference {ref_id} and are checking its status. "
            f"We will update you once we have confirmed the position.\n\n"
            f"Warm regards,\nBharatTrip Operations Team"
        )

if __name__ == "__main__":
    agent = RefundIntakeAgent()

    # Test sample from task brief (WhatsApp from Nomad Travel)
    sample_1 = "Bhai refund ka kya hua? BLR-MAA wala. 2 hafte ho gaye, koi jawab nahi."
    parsed_1 = agent.parse_message(sample_1, channel="WhatsApp", sender="Nomad Travel")
    print("\n--- SAMPLE 1: Nomad Travel WhatsApp (RF-1098 case) ---")
    print(json.dumps(parsed_1, indent=2))

    # Test sample from task brief (Email from Peak Journeys)
    sample_2 = "Hi, I cancelled booking for DEL-DXB last week and was told I'd get a refund. I haven't received anything and I don't have any reference number. Please help, my client is asking."
    parsed_2 = agent.parse_message(sample_2, channel="Email", sender="Peak Journeys")
    print("\n--- SAMPLE 2: Peak Journeys Email (RF-1099 case) ---")
    print(json.dumps(parsed_2, indent=2))

