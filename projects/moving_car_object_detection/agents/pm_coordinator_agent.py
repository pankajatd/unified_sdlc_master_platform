"""
Agent 1: Road Stream Coordinator (PM Agent)
Manages incoming video streams, user upload sessions, incident tickets, and traffic analytics logs.
"""

from datetime import datetime
from typing import Dict, List, Any
import uuid

class PMCoordinatorAgent:
    def __init__(self):
        self.agent_name = "Road Stream Coordinator"
        self.role_title = "PM / Stream Coordinator Agent"
        self.active_sessions: Dict[str, Dict[str, Any]] = {}
        self.incident_log: List[Dict[str, Any]] = []

    def start_session(self, source_name: str, media_type: str = "image") -> str:
        session_id = f"SESSION_{uuid.uuid4().hex[:8].upper()}"
        self.active_sessions[session_id] = {
            'session_id': session_id,
            'source_name': source_name,
            'media_type': media_type,
            'start_time': datetime.now().isoformat(),
            'total_detections': 0,
            'cars_detected': 0,
            'pedestrians_detected': 0,
            'incidents_flagged': 0
        }
        return session_id

    def log_incident(self, session_id: str, incident_type: str, details: str, severity: str = "WARNING"):
        ticket = {
            'ticket_id': f"INC_{uuid.uuid4().hex[:6].upper()}",
            'session_id': session_id,
            'timestamp': datetime.now().isoformat(),
            'incident_type': incident_type,
            'details': details,
            'severity': severity
        }
        self.incident_log.append(ticket)
        if session_id in self.active_sessions:
            self.active_sessions[session_id]['incidents_flagged'] += 1
        return ticket

    def update_metrics(self, session_id: str, metrics: Dict[str, Any]):
        if session_id in self.active_sessions:
            sess = self.active_sessions[session_id]
            sess['cars_detected'] += metrics.get('active_cars', 0)
            sess['pedestrians_detected'] += metrics.get('active_pedestrians', 0)
            sess['total_detections'] += metrics.get('raw_detections_count', 0)

    def get_summary(self, session_id: str) -> Dict[str, Any]:
        return self.active_sessions.get(session_id, {
            'status': 'Not found'
        })
