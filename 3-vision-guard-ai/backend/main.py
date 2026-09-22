"""
FastAPI Server for VisionGuard AI Computer Vision Surveillance
"""

import os
import sys
from pathlib import Path
from typing import List, Dict, Any, Tuple
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

BASE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = BASE_DIR.parent
STATIC_DIR = PROJECT_DIR / "static"

sys.path.append(str(PROJECT_DIR))
from backend.vision_engine import VisionAnalyticsPipeline

app = FastAPI(
    title="VisionGuard AI: Computer Vision Safety Platform",
    description="Real-Time Object Tracking, Geofencing, and Industrial Safety Monitoring",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

pipeline = VisionAnalyticsPipeline()


@app.get("/api/feed/next-frame")
def get_next_frame():
    """Returns telemetry of detected objects, bounding boxes, and active zone violations."""
    return pipeline.process_frame()


@app.get("/api/alerts")
def get_alerts():
    return {"alerts": pipeline.get_recent_events()}


@app.get("/api/stats")
def get_stats():
    frame = pipeline.process_frame()
    return frame["metrics"]


# Static UI Mount
if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


@app.get("/")
def serve_dashboard():
    index_file = STATIC_DIR / "index.html"
    if index_file.exists():
        return FileResponse(str(index_file))
    return {"message": "VisionGuard AI Server Running. Navigate to /docs for API specs."}


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8002))
    host = os.getenv("HOST", "127.0.0.1")
    print(f"[INFO] Starting VisionGuard AI Server at http://{host}:{port}")
    uvicorn.run("main:app", host=host, port=port, reload=True)
