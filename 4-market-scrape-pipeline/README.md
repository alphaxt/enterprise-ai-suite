# 🛒 ScrapeFlow: Automated Competitor Intelligence & Web Scraping Pipeline

[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?style=flat&logo=fastapi)](https://fastapi.tiangolo.com/)
[![ETL](https://img.shields.io/badge/Pipeline-ETL%20%2B%20SQLite-blue)](https://sqlite.org/)
[![Status](https://img.shields.io/badge/Status-Production--Ready-brightgreen)](https://github.com/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

A robust, enterprise-grade **Automated Web Scraping, ETL & Market Intelligence Platform** built in Python. Features anti-blocking header rotation, structured schema normalization with Pydantic, automated delta tracking for price drops, and an interactive executive dashboard.

---

## 🚀 Key Features

- **Anti-Bot Resilience**: Rotates realistic browser User-Agents and employs polite random jitter to prevent rate limiting.
- **Pydantic Schema Validation**: Guarantees zero corrupt records using strict data models for prices, SKUs, stock levels, and ratings.
- **Automated Price Drop & Delta Tracking**: Identifies price drops, discounts, and inventory stockouts between successive crawl runs.
- **Live Terminal Execution Console**: Interactive browser console showing live scraping logs, HTTP responses, and SKU ingestion in real time.
- **Competitor Price Comparison**: Normalizes product catalogs across multi-vendor competitors (e.g. Amazon, BestBuy, Walmart) for direct SKU benchmarking.
- **Instant CSV Export**: Filter and export structured market datasets with one click.

---

## 🛠️ System Architecture

```
┌─────────────────────────────────┐
│ Target E-Commerce / Web Sources │
└────────────────┬────────────────┘
                 │ Anti-Bot Headers / Backoff
┌────────────────▼────────────────┐
│   Modular Scraper (Crawler.py)  │
└────────────────┬────────────────┘
                 │ Raw HTML / Payloads
┌────────────────▼────────────────┐
│    ETL Pipeline & Pydantic      │
│  (Clean, Deduplicate, Normalize)│
└────────────────┬────────────────┘
                 │ Clean Relational Records
┌────────────────▼────────────────┐
│   SQLite Database & Deltas      │
└────────────────┬────────────────┘
                 │
┌────────────────▼────────────────┐
│      FastAPI REST Endpoints     │
└────────────────┬────────────────┘
                 │
┌────────────────▼────────────────┐
│  Market Intelligence Dashboard  │
│  (Live Console, KPIs, Export)   │
└─────────────────────────────────┘
```

---

## 📦 Project Structure

```
4-market-scrape-pipeline/
├── backend/
│   └── main.py          # FastAPI server & crawler trigger endpoints
├── scraper/
│   └── crawler.py       # Resilient scraper with User-Agent rotation
├── pipeline/
│   └── etl.py           # Data normalization, SQLite database & CSV exporter
├── static/
│   └── index.html       # Market Intelligence Dashboard & Live Console UI
├── requirements.txt     # Python dependencies
└── README.md
```

---

## ⚡ Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Start the Server
```bash
python backend/main.py
```

### 3. Open in Browser
- Dashboard: **[http://127.0.0.1:8003](http://127.0.0.1:8003)**
- API Documentation: **[http://127.0.0.1:8003/docs](http://127.0.0.1:8003/docs)**

---

## 🔌 API Reference

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/api/scrape/trigger` | Triggers an automated multi-competitor extraction cycle |
| `GET` | `/api/products` | Returns filterable product records by category or stock status |
| `GET` | `/api/insights` | Market summary KPIs (average discount, tracked competitors, stockouts) |
| `GET` | `/api/export/csv` | Generates and downloads a clean CSV report of the database |

---

## 📄 License
This project is licensed under the MIT License.
