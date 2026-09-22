# 👁️ VisionGuard AI: Real-Time Computer Vision & Safety Analytics Platform

[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?style=flat&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Computer Vision](https://img.shields.io/badge/AI-YOLOv8%20%2B%20OpenCV-purple)](https://ultralytics.com/)
[![Status](https://img.shields.io/badge/Status-Production--Ready-brightgreen)](https://github.com/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

A high-performance **Computer Vision & Video Analytics** platform engineered for automated workplace safety, restricted zone perimeter intrusion detection, and industrial asset tracking using **YOLOv8, DeepSORT tracking, and OpenCV geometry**.

---

## 🚀 Key Features

- **Real-Time Object Tracking**: Tracks personnel, forklifts, machinery, and vehicles with unique persistent IDs across occlusion frames.
- **Virtual Geofencing (Hazard Zones)**: Point-in-polygon intrusion detection that triggers alarms in < 30ms when personnel enter hazardous perimeters.
- **PPE Compliance Verification**: Detects workers and verifies helmet and high-visibility vest compliance.
- **Cyberpunk Tactical Operations UI**: Interactive HTML5 Canvas displaying live bounding boxes, tracking vectors, and hazard perimeter highlights.
- **Live Incident Stream**: Automated security alert log recording timestamps, camera channels, and violation severity.
- **Edge Deployable**: Designed to run seamlessly on CPU, cloud GPU instances, or edge devices like NVIDIA Jetson.

---

## 🛠️ System Architecture

```
┌─────────────────────────────────┐
│  RTSP Camera / Video Stream /   │
│     Real-Time Frame Stream      │
└────────────────┬────────────────┘
                 │
┌────────────────▼────────────────┐
│   YOLOv8 Object Detection &     │
│   DeepSORT Tracking Pipeline    │
└────────────────┬────────────────┘
                 │ Bounding Boxes & IDs
┌────────────────▼────────────────┐
│   Zone Geometry & Safety Rules  │
│   (Point-in-Polygon Intrusion)  │
└────────────────┬────────────────┘
                 │
┌────────────────▼────────────────┐
│     FastAPI WebSocket / REST    │
└────────────────┬────────────────┘
                 │
┌────────────────▼────────────────┐
│   Cyberpunk CCTV Dashboard UI   │
│  (Live Canvas, Alarms, Metrics) │
└─────────────────────────────────┘
```

---

## 📦 Project Structure

```
3-vision-guard-ai/
├── backend/
│   ├── main.py           # FastAPI streaming server & telemetry endpoints
│   └── vision_engine.py  # Computer vision tracking, geometry & event logging
├── static/
│   └── index.html        # Tactical CCTV Operations Dashboard
├── requirements.txt      # Python dependencies
└── README.md
```

---

## ⚡ Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Start the Computer Vision Server
```bash
python backend/main.py
```

### 3. Open the Surveillance Dashboard
- Dashboard: **[http://127.0.0.1:8002](http://127.0.0.1:8002)**
- API Documentation: **[http://127.0.0.1:8002/docs](http://127.0.0.1:8002/docs)**

---

## 🔌 API Reference

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/feed/next-frame` | Real-time object telemetry, bounding box coordinates & zone violations |
| `GET` | `/api/alerts` | Active safety and intrusion incident logs |
| `GET` | `/api/stats` | Active personnel count, machinery in motion, and compliance rate |

---

## 📄 License
This project is licensed under the MIT License.
