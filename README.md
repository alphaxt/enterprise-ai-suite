# 🚀 Enterprise AI & Full-Stack Platform Suite

[![Python](https://img.shields.io/badge/Language-Python%203.10%2B-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?style=flat&logo=fastapi)](https://fastapi.tiangolo.com)
[![Machine Learning](https://img.shields.io/badge/AI-Scikit--Learn%20%7C%20YOLOv8-F7931E?style=flat)](https://scikit-learn.org)
[![Architecture](https://img.shields.io/badge/Architecture-Enterprise%20Microservices-purple?style=flat)](https://github.com/alphaxt)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat)](LICENSE)

A unified **Enterprise AI, Computer Vision, Predictive BI & Data Engineering Suite** engineered as production-grade solutions for corporate workflow automation, document intelligence, workplace safety analytics, and automated market intelligence.

---

## 🧭 Systems Overview & Port Allocation

Each platform runs as an independent microservice with its own dedicated port, allowing concurrent execution without port conflicts:

| Directory | Platform | Core Domain | Tech Stack | Port | Core Capabilities |
| :--- | :--- | :--- | :--- | :---: | :--- |
| **`1-enterprise-rag-agent`** | **🧠 DocuMind AI** | Enterprise RAG & Autonomous GenAI | FastAPI, Hybrid BM25/Vector RAG, Pydantic, Citation Guardrails | `8000` | • Dense + sparse hybrid retrieval<br>• 100% verifiable source citations<br>• Out-of-scope domain guardrails<br>• Embedded LLMOps telemetry |
| **`2-predictive-churn-bi`** | **📊 PulsePredict BI** | Predictive Machine Learning & XAI | Scikit-Learn, FastAPI, Explainable AI, Simulation Engine | `8001` | • 0.89+ ROC-AUC ensemble classification<br>• Localized XAI risk factor drivers<br>• Interactive what-if retention simulator<br>• Executive ARR risk dashboards |
| **`3-vision-guard-ai`** | **👁️ VisionGuard AI** | Computer Vision & Safety Analytics | YOLOv8, DeepSORT, OpenCV, HTML5 Canvas HUD | `8002` | • Real-time persistent ID tracking<br>• Point-in-polygon virtual geofencing (<30ms)<br>• Automated PPE compliance verification<br>• Tactical surveillance operator HUD |
| **`4-market-scrape-pipeline`** | **🛒 ScrapeFlow** | Anti-Bot Scraping & ETL Pipeline | Python, Anti-Bot Rotation, Pydantic, SQLite | `8003` | • User-Agent rotation & exponential backoff<br>• Strict Pydantic schema validation<br>• Price-drop delta tracking between crawls<br>• Live streaming terminal execution console |

---

## 📂 Suite Directory Structure

```text
enterprise-ai-suite/
├── .gitignore
├── .gitattributes                           # Linguist 100% Python enforcement
├── LICENSE
├── README.md                                # Master suite architecture documentation
├── FREELANCING_PLAYBOOK.md                  # High-ticket proposal templates & Upwork roadmap
├── start_all_services.py                    # Multi-process orchestrator for all 4 platforms
│
├── 1-enterprise-rag-agent/                  # Platform 1: DocuMind AI (Port 8000)
│   ├── backend/                             # FastAPI REST & citation generation logic
│   ├── data/                                # Document corpora (.pdf, .txt, .md) & vector indices
│   ├── static/                              # Glassmorphic tactical chat UI & citation drawer
│   └── requirements.txt
│
├── 2-predictive-churn-bi/                   # Platform 2: PulsePredict BI (Port 8001)
│   ├── backend/                             # FastAPI inference & scenario simulation API
│   ├── ml/                                  # Scikit-learn pipelines, XAI weights & training scripts
│   ├── data/                                # Customer telemetry & cohort datasets
│   ├── static/                              # Executive BI dashboard & dynamic parameter sliders
│   └── requirements.txt
│
├── 3-vision-guard-ai/                       # Platform 3: VisionGuard AI (Port 8002)
│   ├── backend/                             # YOLOv8 inference, DeepSORT tracking & geofencing
│   ├── static/                              # Real-time HTML5 Canvas HUD & intrusion alert logs
│   └── requirements.txt
│
└── 4-market-scrape-pipeline/                # Platform 4: ScrapeFlow (Port 8003)
    ├── scraper/                             # Resilient crawler with header rotation
    ├── pipeline/                            # Pydantic validation, normalization & delta engine
    ├── backend/                             # FastAPI endpoints for real-time streaming
    ├── static/                              # Live terminal console & market intelligence table
    └── requirements.txt
```

---

## 🏗️ End-to-End System Architecture

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                       ENTERPRISE AI PLATFORM SUITE                          │
└─────────────────────────────────────────────────────────────────────────────┘
          │                                 │
┌─────────▼──────────────┐        ┌─────────▼──────────────┐
│     DocuMind AI        │        │    PulsePredict BI     │
│   (Enterprise RAG)     │        │  (Predictive Churn ML) │
│ • Hybrid Semantic/BM25 │        │ • 0.89+ ROC-AUC        │
│ • Zero Hallucinations  │        │ • Explainable AI (XAI) │
│ • Embedded Telemetry   │        │ • What-If Simulator    │
│   Port: 8000           │        │   Port: 8001           │
└────────────────────────┘        └────────────────────────┘
          │                                 │
┌─────────▼──────────────┐        ┌─────────▼──────────────┐
│    VisionGuard AI      │        │       ScrapeFlow       │
│  (Computer Vision HUD) │        │ (Data Scraping & ETL)  │
│ • YOLOv8 + DeepSORT    │        │ • Anti-Bot Rotation    │
│ • Virtual Geofencing   │        │ • Pydantic Validation  │
│ • <30ms Alarm Latency  │        │ • Price Delta Engine   │
│   Port: 8002           │        │   Port: 8003           │
└────────────────────────┘        └────────────────────────┘
```

---

## ⚡ Quick Start: Running the Platforms

### Option A: Launch All 4 Services Concurrently
Use the included multi-process orchestrator:

```bash
python start_all_services.py
```

This launches all 4 servers simultaneously in background processes and displays their URLs:
- **DocuMind AI:** `http://127.0.0.1:8000`
- **PulsePredict BI:** `http://127.0.0.1:8001`
- **VisionGuard AI:** `http://127.0.0.1:8002`
- **ScrapeFlow:** `http://127.0.0.1:8003`

---

### Option B: Run Any Platform Individually

```bash
# 1. DocuMind AI (Port 8000)
cd 1-enterprise-rag-agent
pip install -r requirements.txt
python backend/main.py

# 2. PulsePredict BI (Port 8001)
cd 2-predictive-churn-bi
pip install -r requirements.txt
python backend/main.py

# 3. VisionGuard AI (Port 8002)
cd 3-vision-guard-ai
pip install -r requirements.txt
python backend/main.py

# 4. ScrapeFlow (Port 8003)
cd 4-market-scrape-pipeline
pip install -r requirements.txt
python backend/main.py
```

---

## 👤 Author

**Muhammad Danish**
- **GitHub:** [@alphaxt](https://github.com/alphaxt)
- **LinkedIn:** [Muhammad Danish](https://www.linkedin.com/in/muhammad-danish1/)
- **Degree:** B.S. Data Science @ University of Central Punjab (UCP)

---

## 📄 License
This project is open-source under the [MIT License](LICENSE).
