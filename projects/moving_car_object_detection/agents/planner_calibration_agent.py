"""
Agent 3: Frame Calibration Agent (Planner Agent)
Plans image and video preprocessing: letterboxing, aspect ratio preservation, and dynamic contrast calibration.
"""

from typing import Tuple, Dict, Any
import numpy as np
import cv2

class PlannerCalibrationAgent:
    def __init__(self, target_size: int = 640):
        self.agent_name = "Frame Calibration Agent"
        self.role_title = "Planner / Calibration Agent"
        self.target_size = target_size

    def calibrate_frame(self, frame: np.ndarray, enhance_lighting: bool = False) -> Tuple[np.ndarray, Dict[str, Any]]:
        """
        Calibrates input frame:
        1. Checks frame resolution and aspect ratio.
        2. Applies CLAHE (Contrast Limited Adaptive Histogram Equalization) if dark/shadowed.
        3. Returns calibrated frame with metadata.
        """
        h, w = frame.shape[:2]
        is_night = float(np.mean(frame)) < 60.0
        
        calibrated = frame.copy()
        applied_filters = []

        if enhance_lighting or is_night:
            # Enhance low-light road images using CLAHE on L-channel
            lab = cv2.cvtColor(calibrated, cv2.COLOR_BGR2LAB)
            l, a, b = cv2.split(lab)
            clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8, 8))
            cl = clahe.apply(l)
            limg = cv2.merge((cl, a, b))
            calibrated = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)
            applied_filters.append("CLAHE Night Contrast Equalization")

        metadata = {
            'original_resolution': (w, h),
            'aspect_ratio': round(w / max(1, h), 2),
            'mean_brightness': round(float(np.mean(frame)), 1),
            'is_low_light': is_night,
            'applied_filters': applied_filters,
            'target_dimensions': (self.target_size, self.target_size)
        }

        return calibrated, metadata
