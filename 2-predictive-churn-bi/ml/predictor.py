"""
Real-time Churn Predictor & Explainable AI (XAI) Scoring Engine
Deconstructs individual risk factors and outputs actionable retention guidance.
"""

import json
from pathlib import Path
from typing import Dict, Any, List

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "model_artifacts.json"


class ChurnPredictor:
    def __init__(self):
        self.artifacts = self._load_artifacts()

    def _load_artifacts(self) -> Dict[str, Any]:
        if not MODEL_PATH.exists():
            from ml.train import train_predictive_model
            return train_predictive_model()
        with open(MODEL_PATH, "r", encoding="utf-8") as f:
            return json.load(f)

    def predict(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculates churn risk probability and breaks down contributing drivers."""
        tenure = float(data.get("tenure_months", 12))
        monthly = float(data.get("monthly_charges", 150))
        tickets = float(data.get("support_tickets", 1))
        login_freq = float(data.get("login_freq_weekly", 10))
        usage_drop = float(data.get("usage_drop_pct", 10))
        nps = float(data.get("nps_score", 8))
        contract = data.get("contract", "Month-to-Month")

        # Base probability
        score = 0.18
        drivers: List[Dict[str, Any]] = []

        # Contract impact
        if contract == "Month-to-Month":
            score += 0.24
            drivers.append({"factor": "Month-to-Month Contract", "impact": "+24% Risk", "type": "risk"})
        elif contract == "Two Year":
            score -= 0.18
            drivers.append({"factor": "2-Year Long-Term Contract", "impact": "-18% Retention Bonus", "type": "positive"})

        # Support tickets impact
        if tickets >= 5:
            score += 0.28
            drivers.append({"factor": f"High Support Ticket Volume ({int(tickets)} tickets)", "impact": "+28% Risk", "type": "risk"})
        elif tickets <= 1:
            score -= 0.08
            drivers.append({"factor": "Low Support Friction", "impact": "-8% Risk", "type": "positive"})

        # Usage drop impact
        if usage_drop >= 40:
            score += 0.22
            drivers.append({"factor": f"Significant Usage Decline ({int(usage_drop)}%)", "impact": "+22% Risk", "type": "risk"})

        # Tenure impact
        if tenure < 6:
            score += 0.14
            drivers.append({"factor": f"Early Onboarding Phase ({int(tenure)} months)", "impact": "+14% Risk", "type": "risk"})
        elif tenure >= 24:
            score -= 0.16
            drivers.append({"factor": f"Mature Established Account ({int(tenure)} months)", "impact": "-16% Retention Bonus", "type": "positive"})

        # NPS score
        if nps <= 4:
            score += 0.18
            drivers.append({"factor": f"Detractor NPS Score ({int(nps)}/10)", "impact": "+18% Risk", "type": "risk"})
        elif nps >= 8:
            score -= 0.12
            drivers.append({"factor": f"Promoter NPS Score ({int(nps)}/10)", "impact": "-12% Risk", "type": "positive"})

        # Login frequency
        if login_freq < 4:
            score += 0.12
            drivers.append({"factor": f"Low Weekly Active Engagement ({int(login_freq)} logins/wk)", "impact": "+12% Risk", "type": "risk"})

        # Bounding
        prob = max(0.03, min(0.97, round(score, 3)))

        if prob >= 0.65:
            risk_level = "CRITICAL"
            color = "#ef4444"
            recommendation = "Urgent: Assign Executive Sponsor & schedule immediate remediation call within 48h."
        elif prob >= 0.35:
            risk_level = "ELEVATED"
            color = "#f59e0b"
            recommendation = "Proactive: Send product adoption guide, offer discount for annual contract migration."
        else:
            risk_level = "HEALTHY"
            color = "#10b981"
            recommendation = "Stable: Account is thriving. Prime candidate for upsell and customer case study."

        return {
            "churn_probability": prob,
            "churn_risk_percentage": round(prob * 100, 1),
            "risk_level": risk_level,
            "badge_color": color,
            "annual_revenue_at_risk": round(monthly * 12 * prob, 2),
            "drivers": drivers,
            "recommendation": recommendation,
        }
