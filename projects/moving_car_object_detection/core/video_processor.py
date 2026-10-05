"""
Core Video Processor: Frame-by-Frame Road Vision Pipeline
Processes video feeds (dashcam MP4, CCTV clips) with real-time detection, tracking, and telemetry.
"""

import time
from typing import Dict, List, Any, Generator, Tuple
import cv2
import numpy as np
from core.detector import RoadObjectDetector
from core.tracker import RoadObjectTracker

class VideoStreamProcessor:
    def __init__(self, detector: RoadObjectDetector = None, tracker: RoadObjectTracker = None):
        self.detector = detector or RoadObjectDetector()
        self.tracker = tracker or RoadObjectTracker()

    def process_frame(self, frame: np.ndarray, conf_threshold: float = 0.20,
                      draw_trails: bool = True, show_speed: bool = True,
                      box_thickness: int = 1, font_size: int = 8,
                      badge_style: str = "no_badge", box_style: str = "rectangle",
                      font_scale: float = None) -> Tuple[np.ndarray, Dict[str, Any]]:
        """
        Processes a single frame: detection + tracking + HUD overlay.
        Returns (annotated_frame, frame_metrics).
        """
        start_time = time.perf_counter()
        
        # 1. Detection
        detections = self.detector.detect(frame, conf_threshold=conf_threshold)
        
        # 2. Tracking
        tracked_objects = self.tracker.update(detections, frame.shape)
        
        # 3. Render
        annotated = self.tracker.draw_tracking(
            frame, tracked_objects, draw_trails=draw_trails, show_speed=show_speed,
            box_thickness=box_thickness, font_size=font_size, badge_style=badge_style,
            box_style=box_style, font_scale=font_scale
        )
        
        elapsed_ms = (time.perf_counter() - start_time) * 1000.0
        fps = round(1000.0 / max(1.0, elapsed_ms), 1)

        # Count active entities
        cars_count = sum(1 for o in tracked_objects if o['class'] in {'car', 'truck', 'bus'})
        pedestrians_count = sum(1 for o in tracked_objects if o['class'] == 'person')
        lights_count = sum(1 for o in tracked_objects if o['class'] in {'traffic light', 'stop sign'})
        collision_alerts = sum(1 for o in tracked_objects if o['collision_warning'])

        # Draw Executive Telemetry HUD on top left
        hud_h, hud_w = 40, min(annotated.shape[1] - 20, 520)
        overlay = annotated.copy()
        cv2.rectangle(overlay, (10, 10), (10 + hud_w, 10 + hud_h), (15, 23, 42), -1)
        cv2.addWeighted(overlay, 0.75, annotated, 0.25, 0, annotated)
        cv2.rectangle(annotated, (10, 10), (10 + hud_w, 10 + hud_h), (2, 132, 199), 1)

        hud_text = f"FPS: {fps} | Latency: {elapsed_ms:.1f}ms | Cars: {cars_count} | Pedestrians: {pedestrians_count}"
        if collision_alerts > 0:
            hud_text += f" | ALERT: {collision_alerts}"
        cv2.putText(annotated, hud_text, (20, 36), cv2.FONT_HERSHEY_SIMPLEX, 0.52, (255, 255, 255), 1, cv2.LINE_AA)

        metrics = {
            'fps': fps,
            'latency_ms': round(elapsed_ms, 2),
            'active_cars': cars_count,
            'active_pedestrians': pedestrians_count,
            'traffic_lights': lights_count,
            'collision_alerts': collision_alerts,
            'tracked_objects': tracked_objects,
            'raw_detections_count': len(detections)
        }

        return annotated, metrics

    def process_video_generator(self, video_path: str, conf_threshold: float = 0.20,
                                max_frames: int = None, skip_frames: int = 1,
                                draw_trails: bool = True, show_speed: bool = True,
                                box_thickness: int = 1, font_size: int = 8,
                                badge_style: str = "no_badge", box_style: str = "rectangle",
                                font_scale: float = None) -> Generator[Tuple[int, np.ndarray, Dict[str, Any]], None, None]:
        """
        Yields (frame_idx, annotated_frame, metrics) for video streaming in Streamlit.
        """
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise ValueError(f"Could not open video file: {video_path}")

        frame_idx = 0
        try:
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break

                if frame_idx % skip_frames == 0:
                    annotated, metrics = self.process_frame(
                        frame, conf_threshold=conf_threshold, draw_trails=draw_trails,
                        show_speed=show_speed, box_thickness=box_thickness,
                        font_size=font_size, badge_style=badge_style,
                        box_style=box_style, font_scale=font_scale
                    )
                    yield frame_idx, annotated, metrics

                frame_idx += 1
                if max_frames and frame_idx >= max_frames:
                    break
        finally:
            cap.release()
