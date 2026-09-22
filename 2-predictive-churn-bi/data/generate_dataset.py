"""
Dataset Generator for SaaS Customer Churn & Retention Analytics
Produces realistic enterprise dataset with correlated behavioral drivers.
"""

import os
import random
import csv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_FILE = BASE_DIR / "customers.csv"

INDUSTRIES = ["Fintech", "Healthcare", "E-Commerce", "EdTech", "Logistics", "Cybersecurity", "DevOps"]
CONTRACTS = ["Month-to-Month", "One Year", "Two Year"]
PAYMENT_METHODS = ["Credit Card", "Bank Transfer", "Electronic Check"]

def generate_saas_dataset(num_records: int = 1200):
    random.seed(42)
    records = []

    for i in range(1, num_records + 1):
        cust_id = f"CUST-{1000 + i}"
        company = f"Acme-{INDUSTRIES[i % len(INDUSTRIES)]}-{i}"
        industry = random.choice(INDUSTRIES)
        contract = random.choices(CONTRACTS, weights=[0.55, 0.30, 0.15])[0]
        payment = random.choice(PAYMENT_METHODS)
        
        tenure_months = random.randint(1, 48)
        monthly_charges = round(random.uniform(49.0, 999.0), 2)
        
        # Correlated drivers
        # Short tenure + month-to-month + high tickets = high churn probability
        support_tickets = random.randint(0, 10)
        login_freq_weekly = random.randint(1, 35)
        usage_drop_pct = random.randint(0, 85)
        nps_score = random.randint(1, 10)

        # Churn score calculation with realistic noise
        churn_risk_score = 0.15
        if contract == "Month-to-Month":
            churn_risk_score += 0.25
        elif contract == "Two Year":
            churn_risk_score -= 0.15

        if support_tickets >= 5:
            churn_risk_score += 0.28
        if usage_drop_pct >= 40:
            churn_risk_score += 0.22
        if tenure_months < 6:
            churn_risk_score += 0.18
        if nps_score <= 4:
            churn_risk_score += 0.20
        if login_freq_weekly < 4:
            churn_risk_score += 0.15

        # Add random noise
        churn_risk_score += random.uniform(-0.1, 0.1)
        churn_risk_score = max(0.02, min(0.98, churn_risk_score))
        
        churned = 1 if churn_risk_score > 0.52 else 0

        records.append({
            "customer_id": cust_id,
            "company_name": company,
            "industry": industry,
            "contract": contract,
            "tenure_months": tenure_months,
            "monthly_charges": monthly_charges,
            "support_tickets": support_tickets,
            "login_freq_weekly": login_freq_weekly,
            "usage_drop_pct": usage_drop_pct,
            "nps_score": nps_score,
            "payment_method": payment,
            "churn": churned
        })

    # Save to CSV
    os.makedirs(BASE_DIR, exist_ok=True)
    fieldnames = list(records[0].keys())
    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)

    print(f"[SUCCESS] Generated {len(records)} customer records at {OUTPUT_FILE}")
    return OUTPUT_FILE

if __name__ == "__main__":
    generate_saas_dataset()
