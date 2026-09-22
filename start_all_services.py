"""
Enterprise AI Suite - Unified Services Orchestrator
Launches all 4 microservices concurrently across dedicated ports:
- Port 8000: DocuMind AI (Enterprise RAG Agent)
- Port 8001: PulsePredict BI (Customer Churn & Retention ML)
- Port 8002: VisionGuard AI (Computer Vision & Safety Geofencing)
- Port 8003: ScrapeFlow (Anti-Bot ETL & Competitor Scraper)
"""

import subprocess
import sys
import time
import os

SERVICES = [
    {
        "name": "DocuMind AI (Enterprise RAG)",
        "dir": "1-enterprise-rag-agent",
        "cmd": [sys.executable, "backend/main.py"],
        "port": 8000,
        "url": "http://127.0.0.1:8000"
    },
    {
        "name": "PulsePredict BI (Customer Churn ML)",
        "dir": "2-predictive-churn-bi",
        "cmd": [sys.executable, "backend/main.py"],
        "port": 8001,
        "url": "http://127.0.0.1:8001"
    },
    {
        "name": "VisionGuard AI (Computer Vision HUD)",
        "dir": "3-vision-guard-ai",
        "cmd": [sys.executable, "backend/main.py"],
        "port": 8002,
        "url": "http://127.0.0.1:8002"
    },
    {
        "name": "ScrapeFlow (E-Commerce Scraping & ETL)",
        "dir": "4-market-scrape-pipeline",
        "cmd": [sys.executable, "backend/main.py"],
        "port": 8003,
        "url": "http://127.0.0.1:8003"
    }
]

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    processes = []

    print("=" * 65)
    print("🚀 Launching Enterprise AI & Full-Stack Platform Suite")
    print("=" * 65)

    for svc in SERVICES:
        svc_dir = os.path.join(base_dir, svc["dir"])
        if os.path.exists(svc_dir):
            print(f"[*] Starting {svc['name']} on {svc['url']} ...")
            proc = subprocess.Popen(svc["cmd"], cwd=svc_dir)
            processes.append((svc["name"], proc, svc["url"]))
            time.sleep(0.5)
        else:
            print(f"[!] Directory not found: {svc_dir}")

    print("\n✅ All 4 Enterprise Platforms are live:")
    for name, _, url in processes:
        print(f"  • {name.ljust(40)} -> {url}")

    print("\nPress Ctrl+C to terminate all services.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping all services...")
        for _, proc, _ in processes:
            proc.terminate()
        print("Shutdown complete.")

if __name__ == "__main__":
    main()
