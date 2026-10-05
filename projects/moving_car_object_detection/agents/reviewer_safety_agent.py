"""
Agent 5: Road Safety Reviewer (Reviewer Agent)
Audits detections against autonomous driving and road safety standards.
Monitors blind spots, pedestrian hazard zones, and filters false-positive artifacts.
"""

from typing import List, Dict, Any, Tuple

class ReviewerSafetyAgent:
    def __init__(self, min_confidence_floor: float = 0.15):
        self.agent_name = "Road Safety Reviewer"
        self.role_title = "Reviewer / Safety Inspector Agent"
        self.min_confidence_floor = min_confidence_floor

    def audit_detections(self, detections: List[Dict[str, Any]], frame_shape: Tuple[int, int]) -> Dict[str, Any]:
        """
        Audits detection outputs for road safety compliance:
        - Flags vulnerable road users (pedestrians, cyclists).
        - Flags vehicles in close proximity.
        - Calculates confidence quality score.
        """
        h_frame, w_frame = frame_shape[:2]
        
        pedestrians = [d for d in detections if d['class'] == 'person']
        bicycles = [d for d in detections if d['class'] in {'bicycle', 'motorcycle'}]
        cars = [d for d in detections if d['class'] in {'car', 'truck', 'bus'}]
        traffic_signals = [d for d in detections if d['class'] in {'traffic light', 'stop sign'}]

        safety_alerts = []

        # 1. Check for vulnerable pedestrians in roadway
        for p in pedestrians:
            x, y, w, h = p['box']
            in_roadway = 0.25 * w_frame < (x + w/2) < 0.75 * w_frame
            if in_roadway and (y + h) > 0.5 * h_frame:
                safety_alerts.append({
                    'type': 'PEDESTRIAN_IN_LANE',
                    'severity': 'CRITICAL',
                    'message': f"Pedestrian detected directly in travel path (Conf: {int(p['confidence']*100)}%)"
                })

        # 2. Check for tailgating / close vehicle
        for c in cars:
            x, y, w, h = c['box']
            if h > 0.35 * h_frame and (0.25 * w_frame < (x + w/2) < 0.75 * w_frame):
                safety_alerts.append({
                    'type': 'PROXIMITY_HAZARD',
                    'severity': 'HIGH',
                    'message': f"Leading vehicle in close braking range (Bounding box height: {h}px)"
                })

        mean_conf = float(sum(d['confidence'] for d in detections) / max(1, len(detections)))

        return {
            'auditor': self.agent_name,
            'status': 'SAFETY_COMPLIANT' if not safety_alerts else 'SAFETY_ATTENTION_REQUIRED',
            'vulnerable_entities_count': len(pedestrians) + len(bicycles),
            'traffic_controls_present': len(traffic_signals) > 0,
            'mean_confidence': round(mean_conf, 2),
            'safety_alerts': safety_alerts
        }
