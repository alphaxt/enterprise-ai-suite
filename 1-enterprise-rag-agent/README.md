# 🧠 DocuMind AI: Enterprise RAG & Autonomous Document Intelligence Hub

[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?style=flat&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.11%2B-blue?style=flat&logo=python)](https://www.python.org/)
[![Architecture](https://img.shields.io/badge/Architecture-Hybrid%20RAG%20%2B%20Guardrails-purple)](https://github.com/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

An enterprise-ready **Retrieval-Augmented Generation (RAG)** platform and autonomous document intelligence system. Designed for legal, compliance, and product operations teams to query complex enterprise contracts, technical specifications, and internal knowledge bases with **100% verifiable source citations, sub-second latency, and zero-hallucination guardrails**.

---

## 🚀 Key Features

- **Hybrid Semantic Retrieval**: Combines BM25 sparse keyword search with dense semantic scoring for high-precision retrieval across domain-specific jargon.
- **Verifiable Source Citations**: Every claim quotes the exact document title, section, page number, and source snippet.
- **Out-of-Scope Domain Guardrails**: Rejects off-topic or unverified queries (`OUT_OF_SCOPE_REJECTED`) to eliminate AI hallucinations.
- **Dynamic Multi-Format Ingestion**: Supports drag-and-drop ingestion of `.txt`, `.md`, and `.pdf` files with automated chunking and section extraction.
- **Real-Time LLMOps Analytics**: Embedded telemetry tracking end-to-end query latency, token usage, retrieval confidence, and vector index statistics.
- **Dual Inference Mode**: Works out of the box with an intelligent local heuristic extractor, or seamlessly connects to cloud LLM providers (Groq Llama 3, OpenAI, Anthropic).
- **Modern Glassmorphic Web Dashboard**: Dark-mode tactical UI with interactive citation drawers, quick prompt chips, and instant document management.

---

## 🛠️ System Architecture

```
                               ┌────────────────────────┐
                               │   Modern Web Dashboard │
                               │  (Chat, Citations, UI) │
                               └───────────┬────────────┘
                                           │ HTTP / JSON
                               ┌───────────▼────────────┐
                               │   FastAPI REST Server  │
                               └───────────┬────────────┘
                                           │
                    ┌──────────────────────┴──────────────────────┐
                    ▼                                             ▼
       ┌─────────────────────────┐                   ┌────────────────────────┐
       │  Agent Query Router     │                   │  Hybrid RAG Engine     │
       │  - Intent Classifier    │◄──────────────────┤  - Stopword Filter     │
       │  - Out-of-Scope Guard   │   Hybrid Search   │  - BM25 Sparse Index   │
       │  - Clause Synthesizer   │                   │  - Semantic Projections│
       └────────────┬────────────┘                   └────────────────────────┘
                    │ Verified Context & Citations
       ┌────────────▼────────────┐
       │ Extractive / LLM Engine │ (Groq Llama-3 /
       │ Citation Attribution    │  OpenAI / Local)
       └─────────────────────────┘
```

---

## 📦 Project Structure

```
1-enterprise-rag-agent/
├── backend/
│   ├── main.py            # FastAPI REST server & endpoint routing
│   ├── rag_engine.py      # Hybrid BM25 & semantic vector retrieval engine
│   └── agent.py           # Intent routing, citation extraction & guardrails
├── data/
│   └── samples/
│       ├── enterprise_sla.txt    # Sample SaaS Master Services Agreement & SLA
│       └── ai_product_specs.txt  # Sample Platform Architecture Specifications
├── static/
│   └── index.html         # Responsive dark-mode web application & dashboard
├── .env.example           # Configuration template
├── requirements.txt       # Python dependencies
└── README.md
```

---

## ⚡ Quick Start

### 1. Clone & Navigate
```bash
git clone https://github.com/alphaxt/enterprise-rag-agent.git
cd enterprise-rag-agent
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Environment Setup (Optional)
```bash
cp .env.example .env
```
*(Optional: Add your `GROQ_API_KEY` or `OPENAI_API_KEY`. If left blank, the system automatically uses the high-precision local semantic extraction engine)*

### 4. Run the Platform
```bash
python backend/main.py
```

### 5. Access the Web Dashboard
- Web UI: **[http://127.0.0.1:8000](http://127.0.0.1:8000)**
- Interactive OpenAPI / Swagger Docs: **[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)**

---

## 🔌 API Reference

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/health` | Service health status check |
| `GET` | `/api/stats` | Returns total indexed docs, chunks, and retrieval engine status |
| `GET` | `/api/documents` | Lists all active document filenames in the knowledge base |
| `POST` | `/api/query` | Submits a query, returns answer, exact citations, and latency telemetry |
| `POST` | `/api/upload` | Ingests a new file or raw text dynamically into the vector index |

### Example Query Request (`POST /api/query`)
```json
{
  "query": "What is the service availability guarantee and penalties for downtime?",
  "top_k": 3
}
```

### Example Response
```json
{
  "answer": "Based on enterprise documentation, here are the exact provisions governing uptime...",
  "citations": [
    {
      "citation_id": "[1]",
      "doc_name": "enterprise_sla.txt",
      "section": "SECTION 1: SERVICE AVAILABILITY & UPTIME COMMITMENT",
      "page": 1,
      "relevance_score": 0.884,
      "exact_quote": "1.1 Service Level Guarantee: Provider warrants that the Enterprise AI Cloud Platform shall maintain an aggregate Monthly Uptime Percentage of not less than 99.95%..."
    }
  ],
  "intent": "FACTUAL_EXTRACTION",
  "latency_ms": 14.2,
  "guardrail_status": "VERIFIED_HIGH_CONFIDENCE"
}
```

---

## 🔒 Enterprise Guardrails & Compliance

1. **Zero Hallucination Policy**: Queries lacking genuine content keyword representation in the ingested documentation trigger an automatic `OUT_OF_SCOPE_REJECTED` status rather than fabricating assumptions.
2. **Data Isolation**: Document chunks are partitioned by document identifier, with page-level provenance tracking.
3. **No External Leakage**: In local mode, zero telemetry or customer text is transmitted over external networks.

---

## 📄 License
This project is licensed under the MIT License.
