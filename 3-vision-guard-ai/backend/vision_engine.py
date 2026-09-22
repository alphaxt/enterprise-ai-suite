"""
VisionGuard Computer Vision Analytics Engine
Implements Object Tracking, Virtual Geofencing (Point-in-Polygon),
Safety Rule Enforcement, and Frame Simulation.
"""

import time
import math
import random
from typing import List, Dict, Any, Tuple


def point_in_polygon(x: float, y: float, polygon: List[Tuple[float, float]]) -> bool:
    """Standard ray-casting algorithm to detect if coordinates lie within a polygon zone."""
    n = len(polygon)
    inside = False
    p1x, p1y = polygon[0]
    for i in range(n + 1):
        p2x, p2y = polygon[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y
    return inside


class TrackedEntity:
    def __init__(self, track_id: int, label: str, x: float, y: float, w: float, h: float, vx: float, vy: float, ppe_compliant: bool = True):
        self.track_id = track_id
        self.label = label
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.vx = vx
        self.vy = vy
        self.confidence = round(random.uniform(0.88, 0.98), 2)
        self.ppe_compliant = ppe_compliant
        self.in_zone = False

    def update(self, bounds_w: float = 800, bounds_h: float = 500):
        self.x += self.vx
        self.y += self.vy

        # Bounce off canvas walls
        if self.x < 30 or self.x + self.w > bounds_w - 30:
            self.vx *= -1
        if self.y < 30 or self.y + self.h > bounds_h - 30:
            self.vy *= -1

    def to_dict(self) -> Dict[str, Any]:
        return {
            "track_id": self.track_id,
            "label": self.label,
            "bbox": [round(self.x, 1), round(self.y, 1), round(self.w, 1), round(self.h, 1)],
            "confidence": self.confidence,
            "ppe_compliant": self.ppe_compliant,
            "in_zone": self.in_zone
        }


class VisionAnalyticsPipeline:
    def __init__(self):
        # Default Restricted Hazard Zone (e.g. Heavy Automated Machinery area)
        self.hazard_zone = [
            (420, 100),
            (740, 100),
            (740, 420),
            (420, 420)
        ]
        self.entities: List[TrackedEntity] = self._seed_entities()
        self.events_log: List[Dict[str, Any]] = []
        self.total_violations_counter = 0

    def _seed_entities(self) -> List[TrackedEntity]:
        return [
            TrackedEntity(101, "Worker (PPE)", 120, 150, 45, 90, 1.8, 0.9, ppe_compliant=True),
            TrackedEntity(102, "Forklift", 220, 320, 90, 70, -1.2, 1.1, ppe_compliant=True),
            TrackedEntity(103, "Technician", 460, 240, 45, 90, 1.1, -1.4, ppe_compliant=False),
            TrackedEntity(104, "Inspector", 320, 80, 45, 90, -1.5, 0.7, ppe_compliant=True),
            TrackedEntity(105, "Pallet Jack", 580, 340, 75, 55, 0.8, 1.3, ppe_compliant=True),
        ]

    def process_frame(self) -> Dict[str, Any]:
        """Calculates updated entity positions, checks polygon zones, and returns live frame telemetry."""
        active_detections = []
        violations = []

        for entity in self.entities:
            entity.update(bounds_w=800, bounds_h=500)
            
            # Bottom-center coordinate represents foot location
            foot_x = entity.x + (entity.w / 2)
            foot_y = entity.y + entity.h

            is_inside = point_in_polygon(foot_x, foot_y, self.hazard_zone)
            entity.in_zone = is_inside

            if is_inside:
                violations.append({
                    "track_id": entity.track_id,
                    "label": entity.label,
                    "type": "ZONE_INTRUSION",
                    "severity": "CRITICAL",
                    "timestamp": time.strftime("%H:%M:%S")
                })
                # Add to persistent event log if new
                if random.random() < 0.15:
                    self._record_event(
                        severity="CRITICAL",
                        title=f"Restricted Zone Intrusion: {entity.label} #{entity.track_id}",
                        location="Hazard Zone A (Heavy Machinery)"
                    )

            if not entity.ppe_compliant:
                if random.random() < 0.08:
                    self._record_event(
                        severity="WARNING",
                        title=f"PPE Non-Compliance: Missing Hardhat on #{entity.track_id}",
                        location="Main Floor Sector 3"
                    )

            active_detections.append(entity.to_dict())

        # Overall compliance rate
        compliant_count = sum(1 for e in self.entities if e.ppe_compliant and not e.in_zone)
        compliance_pct = round((compliant_count / len(self.entities)) * 100, 1)

        return {
            "timestamp": time.time(),
            "frame_width": 800,
            "frame_height": 500,
            "hazard_zone": self.hazard_zone,
            "detections": active_detections,
            "active_violations": violations,
            "metrics": {
                "active_personnel": sum(1 for e in self.entities if "Worker" in e.label or "Technician" in e.label or "Inspector" in e.label),
                "active_machinery": sum(1 for e in self.entities if "Forklift" in e.label or "Pallet" in e.label),
                "compliance_percentage": compliance_pct,
                "total_events_logged": len(self.events_log)
            }
        }

    def _record_event(self, severity: str, title: str, location: str):
        event = {
            "id": f"EVT-{1000 + len(self.events_log)}",
            "time": time.strftime("%H:%M:%S"),
            "severity": severity,
            "title": title,
            "location": location
        }
        self.events_log.insert(0, event)
        if len(self.events_log) > 25:
            self.events_log.pop()

    def get_recent_events(self) -> List[Dict[str, Any]]:
        if not self.events_log:
            # Seed initial sample events
            self._record_event("INFO", "Surveillance Feed Channel 01 Initialized", "Sector A")
            self._record_event("CRITICAL", "Zone Intrusion Detected: Track #103", "Hazard Zone A")
            self._record_event("WARNING", "PPE Alert: Missing Helmet #103", "Loading Bay")
        return self.events_log
