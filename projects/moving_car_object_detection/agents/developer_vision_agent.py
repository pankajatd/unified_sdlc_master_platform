"""
Agent 4: Computer Vision Specialist (Developer Agent)
Executes neural inference, draws high-contrast executive bounding boxes, and tracks vehicle trajectories.
"""

from typing import List, Dict, Any, Tuple
import numpy as np
from core.detector import RoadObjectDetector
from core.tracker import RoadObjectTracker

class DeveloperVisionAgent:
    def __init__(self, detector: RoadObjectDetector = None, tracker: RoadObjectTracker = None):
        self.agent_name = "Computer Vision Specialist"
        self.role_title = "Developer Agent"
        self.detector = detector or RoadObjectDetector()
        self.tracker = tracker or RoadObjectTracker()

    def process_image(self, image: np.ndarray, conf_threshold: float = 0.20) -> Tuple[np.ndarray, List[Dict[str, Any]], Dict[str, int]]:
        """
        Runs object detection on static street image.
        Returns (annotated_image, detections_list, class_counts_dict).
        """
        detections = self.detector.detect(image, conf_threshold=conf_threshold)
        annotated = self.detector.draw_detections(image, detections)

        counts = {}
        for det in detections:
            c = det['class']
            counts[c] = counts.get(c, 0) + 1

        return annotated, detections, counts

    def process_video_frame(self, frame: np.ndarray, conf_threshold: float = 0.20,
                            draw_trails: bool = True, show_speed: bool = True) -> Tuple[np.ndarray, List[Dict[str, Any]]]:
        """
        Runs detection and multi-object tracking with velocity and trajectory trails.
        """
        detections = self.detector.detect(frame, conf_threshold=conf_threshold)
        tracked = self.tracker.update(detections, frame.shape)
        annotated = self.tracker.draw_tracking(frame, tracked, draw_trails=draw_trails, show_speed=show_speed)

        return annotated, tracked
