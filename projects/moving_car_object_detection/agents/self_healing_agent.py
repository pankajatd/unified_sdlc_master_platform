"""
Agent 7: Self-Healing System Maintainer (Self-Healing DevOps Agent)
Monitors execution health, manages frame drops, auto-recovers from corrupted video streams, and prevents crashes.
"""

from typing import Dict, Any, List
import numpy as np

class SelfHealingAgent:
    def __init__(self, target_latency_ms: float = 50.0):
        self.agent_name = "Self-Healing System Maintainer"
        self.role_title = "Self-Healing DevOps Agent"
        self.target_latency_ms = target_latency_ms
        self.recovery_events: List[Dict[str, Any]] = []
        self.healthy = True

    def audit_frame_health(self, frame: Any) -> np.ndarray:
        """
        Audits raw frame data before passing to neural model.
        If frame is None or corrupted, auto-heals by generating a neutral blank fallback frame.
        """
        if frame is None or not isinstance(frame, np.ndarray) or frame.size == 0:
            self.recovery_events.append({
                'type': 'CORRUPTED_FRAME_RECOVERED',
                'action': 'Substituted blank frame buffer to avoid pipeline crash'
            })
            # Generate fallback frame
            return np.zeros((480, 640, 3), dtype=np.uint8)
        
        # Ensure 3-channel BGR
        if len(frame.shape) == 2:
            import cv2
            return cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)

        return frame

    def monitor_latency(self, latency_ms: float) -> Dict[str, Any]:
        """
        Checks processing latency against real-time 30-60 FPS budget.
        Recommends dynamic frame skipping if latency spikes.
        """
        if latency_ms > self.target_latency_ms * 1.5:
            action = "Recommend setting skip_frames=2 to preserve real-time playback"
            status = "THROTTLED"
        else:
            action = "Nominal real-time performance maintained"
            status = "HEALTHY"

        return {
            'agent': self.agent_name,
            'status': status,
            'current_latency_ms': latency_ms,
            'budget_target_ms': self.target_latency_ms,
            'recommended_action': action,
            'total_self_healing_events': len(self.recovery_events)
        }
