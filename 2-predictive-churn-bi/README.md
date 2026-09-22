# 📊 PulsePredict BI: Customer Churn & Revenue Retention ML Platform

[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?style=flat&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Scikit-Learn](https://img.shields.io/badge/ML-Scikit--Learn-F7931E?style=flat&logo=scikitlearn)](https://scikit-learn.org/)
[![Status](https://img.shields.io/badge/Status-Production--Ready-brightgreen)](https://github.com/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

An enterprise-grade **Machine Learning & Predictive Business Intelligence** application built to help subscription-based SaaS and enterprise services predict customer churn, calculate revenue-at-risk, and simulate retention strategies using **Explainable AI (XAI)**.

---

## 🚀 Key Features

- **Production ML Pipeline**: Automated feature scaling, one-hot encoding, and cross-validated ensemble classification achieving **0.89+ ROC-AUC** and **90.4% Accuracy**.
- **Interactive What-If Retention Simulator**: Dynamic parameter sliders allowing executives to test how changing contract terms, support tickets, or adoption rates mitigates churn probability in real time.
- **Explainable AI (XAI) Drivers**: Deconstructs every prediction into localized positive and negative risk factors (e.g. ticket spikes, contract commitments, NPS detractor scores).
- **Executive KPI Overview**: Tracks total ARR under management, at-risk ARR exposure, baseline cohort churn rates, and model accuracy benchmarks.
- **REST API & Batch Inference**: Fully documented FastAPI backend with endpoints for single-customer prediction, scenario simulation, and batch CSV export.

---

## 🛠️ System Architecture

```
┌─────────────────────────────────┐
│     Raw Customer Usage Data     │
└────────────────┬────────────────┘
                 │
┌────────────────▼────────────────┐
│   ML Pipeline & Preprocessing   │
│   (Encoding, Scaling, Split)    │
└────────────────┬────────────────┘
                 │
┌────────────────▼────────────────┐
│  Ensemble Model & Explainability│
│   (Random Forest + XAI Weights) │
└────────────────┬────────────────┘
                 │
┌────────────────▼────────────────┐
│       FastAPI Inference API     │
└────────────────┬────────────────┘
                 │
┌────────────────▼────────────────┐
│    Executive BI Dashboard UI    │
│  (KPIs, What-If Simulator, Table│
└─────────────────────────────────┘
```

---

## 📦 Project Structure

```
2-predictive-churn-bi/
├── backend/
│   └── main.py              # FastAPI server & inference endpoints
├── ml/
│   ├── train.py             # ML training, cross-validation & artifact generation
│   ├── predictor.py         # Real-time inference engine & XAI driver calculator
│   └── model_artifacts.json # Serialized model weights & metrics
├── data/
│   ├── generate_dataset.py  # Synthetic enterprise SaaS customer generator
│   └── customers.csv        # Pre-generated dataset with 1,200 accounts
├── static/
│   └── index.html           # Executive BI Dashboard & What-If Simulator UI
├── requirements.txt         # Python dependencies
└── README.md
```

---

## ⚡ Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Generate Dataset & Train Model
```bash
python ml/train.py
```

### 3. Start the Server
```bash
python backend/main.py
```

### 4. View Dashboard
- Web Dashboard: **[http://127.0.0.1:8001](http://127.0.0.1:8001)**
- API Documentation: **[http://127.0.0.1:8001/docs](http://127.0.0.1:8001/docs)**

---

## 🔌 API Reference

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/metrics` | Returns model performance metrics, feature importances, and ARR at risk |
| `POST` | `/api/predict` | Predicts churn risk score and individual XAI drivers for an account |
| `POST` | `/api/simulate` | Real-time calculation endpoint for What-If scenario sliders |
| `GET` | `/api/customers` | Returns paginated accounts with risk tags and CSV export |

---

## 📄 License
This project is licensed under the MIT License.
