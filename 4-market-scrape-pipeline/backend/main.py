"""
FastAPI Server for ScrapeFlow Market Intelligence & Crawler Pipeline
"""

import os
import sys
from pathlib import Path
from typing import Optional
from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

BASE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = BASE_DIR.parent
STATIC_DIR = PROJECT_DIR / "static"

sys.path.append(str(PROJECT_DIR))
from scraper.crawler import MarketCrawler
from pipeline.etl import ETLPipeline

app = FastAPI(
    title="ScrapeFlow: Automated Scraping & ETL Market Intelligence",
    description="Anti-Bot Web Crawler, Structured ETL Pipeline, and Price Tracker",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

crawler = MarketCrawler()
pipeline = ETLPipeline()

# Initial seed crawl on startup
try:
    initial_records = crawler.crawl_competitors()
    pipeline.process_and_save(initial_records)
    print(f"[OK] Seeded database with {len(initial_records)} competitor records.")
except Exception as e:
    print(f"[WARN] Startup crawl warning: {e}")


@app.post("/api/scrape/trigger")
def trigger_scrape():
    """Triggers an automated crawler pass across all targets."""
    raw_data = crawler.crawl_competitors()
    res = pipeline.process_and_save(raw_data)
    return {
        "status": "success",
        "records_ingested": res["records_processed"],
        "price_drops_detected": res["price_drops_detected"],
        "price_drops": res["price_drops"],
        "logs": crawler.logs
    }


@app.get("/api/logs")
def get_logs():
    return {"logs": crawler.logs}


@app.get("/api/products")
def get_products(category: Optional[str] = None, in_stock: Optional[bool] = None):
    return {"products": pipeline.fetch_all(category=category, in_stock_only=bool(in_stock))}


@app.get("/api/insights")
def get_insights():
    return pipeline.get_market_summary()


@app.get("/api/export/csv")
def export_csv():
    csv_data = pipeline.export_csv_string()
    return Response(
        content=csv_data,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=market_intelligence_report.csv"}
    )


# Static Mount
if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


@app.get("/")
def serve_dashboard():
    index_file = STATIC_DIR / "index.html"
    if index_file.exists():
        return FileResponse(str(index_file))
    return {"message": "ScrapeFlow API Running. Visit /docs for OpenAPI specs."}


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8003))
    host = os.getenv("HOST", "127.0.0.1")
    print(f"[INFO] Starting ScrapeFlow Server at http://{host}:{port}")
    uvicorn.run("main:app", host=host, port=port, reload=True)
