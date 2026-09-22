"""
FastAPI Server for PulsePredict BI Churn & Retention Analytics
"""

import os
import sys
import csv
from pathlib import Path
from typing import Optional, List, Dict, Any
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, Response
from pydantic import BaseModel

BASE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = BASE_DIR.parent
STATIC_DIR = PROJECT_DIR / "static"
DATA_FILE = PROJECT_DIR / "data" / "customers.csv"

sys.path.append(str(PROJECT_DIR))
from ml.predictor import ChurnPredictor

app = FastAPI(
    title="PulsePredict BI: Predictive Churn & Revenue Intelligence",
    description="Machine Learning Pipeline and Executive What-If Simulator",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

predictor = ChurnPredictor()


class CustomerInput(BaseModel):
    tenure_months: float = 12
    monthly_charges: float = 180.0
    support_tickets: float = 2
    login_freq_weekly: float = 14
    usage_drop_pct: float = 15
    nps_score: float = 8
    contract: str = "Month-to-Month"


@app.get("/api/metrics")
def get_metrics():
    artifacts = predictor.artifacts
    # Calculate ARR aggregate from customers.csv
    total_arr = 0.0
    at_risk_arr = 0.0
    if DATA_FILE.exists():
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                monthly = float(row.get("monthly_charges", 100))
                is_churn = int(row.get("churn", 0))
                total_arr += monthly * 12
                if is_churn == 1:
                    at_risk_arr += monthly * 12

    return {
        "model_type": artifacts.get("model_type", "Calibrated Ensemble"),
        "metrics": artifacts.get("metrics", {}),
        "feature_importances": artifacts.get("feature_importances", {}),
        "total_arr": round(total_arr, 2),
        "at_risk_arr": round(at_risk_arr, 2),
        "baseline_churn_rate": artifacts.get("baseline_churn_rate", 0.32),
        "status": "Production-Calibrated"
    }


@app.post("/api/predict")
def predict_churn(payload: CustomerInput):
    return predictor.predict(payload.dict())


@app.post("/api/simulate")
def simulate_scenario(payload: CustomerInput):
    return predictor.predict(payload.dict())


@app.get("/api/customers")
def get_customers(limit: int = 50, filter_risk: Optional[str] = None):
    results = []
    if not DATA_FILE.exists():
        return {"customers": []}

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            if i >= limit * 2:
                break
            pred = predictor.predict({
                "tenure_months": row["tenure_months"],
                "monthly_charges": row["monthly_charges"],
                "support_tickets": row["support_tickets"],
                "login_freq_weekly": row["login_freq_weekly"],
                "usage_drop_pct": row["usage_drop_pct"],
                "nps_score": row["nps_score"],
                "contract": row["contract"]
            })
            if filter_risk and pred["risk_level"] != filter_risk:
                continue

            results.append({
                "customer_id": row["customer_id"],
                "company_name": row["company_name"],
                "industry": row["industry"],
                "contract": row["contract"],
                "monthly_charges": float(row["monthly_charges"]),
                "tenure_months": int(row["tenure_months"]),
                "support_tickets": int(row["support_tickets"]),
                "risk_level": pred["risk_level"],
                "churn_percentage": pred["churn_risk_percentage"],
                "badge_color": pred["badge_color"]
            })
            if len(results) >= limit:
                break

    return {"customers": results}


# Static Mount
if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


@app.get("/")
def serve_dashboard():
    index_file = STATIC_DIR / "index.html"
    if index_file.exists():
        return FileResponse(str(index_file))
    return {"message": "PulsePredict BI API Running. Navigate to /docs for API spec."}


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8001))
    host = os.getenv("HOST", "127.0.0.1")
    print(f"[INFO] Starting PulsePredict BI Server at http://{host}:{port}")
    uvicorn.run("main:app", host=host, port=port, reload=True)
