"""
Core Vision Tracker: Multi-Object Tracking & Motion Vector Engine
Tracks vehicles and pedestrians across sequential video frames.
Calculates motion trajectories, estimated vehicle speeds, and collision proximity warnings.
"""

from typing import Dict, List, Tuple, Any
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont
from core.detector import _get_pil_font

class RoadObjectTracker:
    def __init__(self, max_disappeared: int = 20, max_distance_px: float = 120.0):
        self.next_object_id = 1
        self.objects: Dict[int, Dict[str, Any]] = {} # id -> track state
        self.disappeared: Dict[int, int] = {}
        self.max_disappeared = max_disappeared
        self.max_distance_px = max_distance_px
        
        # Calibration factors for dashcam perspective
        # Approximate: pixel displacement to km/h assuming 30 FPS
        self.speed_calibration_factor = 2.4

    def update(self, detections: List[Dict[str, Any]], frame_shape: Tuple[int, int]) -> List[Dict[str, Any]]:
        """
        Updates tracking state with new detections from current frame.
        Returns active tracked objects with trajectories and velocity info.
        """
        h_frame, w_frame = frame_shape[:2]
        
        # Calculate centroids of incoming detections
        input_centroids = []
        for det in detections:
            x, y, w, h = det['box']
            cx = int(x + w / 2)
            cy = int(y + h / 2)
            input_centroids.append((cx, cy))

        # If no objects currently tracked, register all incoming detections
        if len(self.objects) == 0:
            for i, det in enumerate(detections):
                self._register(det, input_centroids[i])
            return self.get_tracked_objects()

        # If no incoming detections, increment disappeared count
        if len(detections) == 0:
            for obj_id in list(self.disappeared.keys()):
                self.disappeared[obj_id] += 1
                if self.disappeared[obj_id] > self.max_disappeared:
                    self._deregister(obj_id)
            return self.get_tracked_objects()

        # Match existing tracked objects with new centroids using Euclidean distance
        object_ids = list(self.objects.keys())
        object_centroids = [self.objects[obj_id]['centroid'] for obj_id in object_ids]

        # Distance matrix
        D = np.zeros((len(object_ids), len(input_centroids)), dtype=np.float32)
        for i, oc in enumerate(object_centroids):
            for j, ic in enumerate(input_centroids):
                dist = np.hypot(oc[0] - ic[0], oc[1] - ic[1])
                D[i, j] = dist

        # Find minimum distance pairings
        rows = D.min(axis=1).argsort()
        cols = D.argmin(axis=1)[rows]

        used_rows = set()
        used_cols = set()

        for row, col in zip(rows, cols):
            if row in used_rows or col in used_cols:
                continue

            # Check distance threshold
            if D[row, col] > self.max_distance_px:
                continue

            obj_id = object_ids[row]
            new_det = detections[col]
            new_centroid = input_centroids[col]

            # Update tracked object
            old_centroid = self.objects[obj_id]['centroid']
            displacement = np.hypot(new_centroid[0] - old_centroid[0], new_centroid[1] - old_centroid[1])
            
            # Estimate speed (smoothed)
            instant_speed = displacement * self.speed_calibration_factor
            prev_speed = self.objects[obj_id].get('speed_kmh', 45.0)
            smoothed_speed = round(0.7 * prev_speed + 0.3 * instant_speed, 1)

            # Check collision hazard (if vehicle is in center lane and expanding downwards)
            in_center_lane = 0.3 * w_frame < new_centroid[0] < 0.7 * w_frame
            moving_closer = new_centroid[1] > old_centroid[1]
            is_close = new_det['box'][3] > 0.25 * h_frame # large bounding box height
            collision_warning = bool(in_center_lane and (moving_closer and is_close))

            self.objects[obj_id]['centroid'] = new_centroid
            self.objects[obj_id]['box'] = new_det['box']
            self.objects[obj_id]['confidence'] = new_det['confidence']
            self.objects[obj_id]['class'] = new_det['class']
            self.objects[obj_id]['color'] = new_det['color']
            self.objects[obj_id]['speed_kmh'] = max(15.0, min(smoothed_speed, 140.0))
            self.objects[obj_id]['collision_warning'] = collision_warning
            
            # Append trajectory (keep last 30 points)
            self.objects[obj_id]['trajectory'].append(new_centroid)
            if len(self.objects[obj_id]['trajectory']) > 30:
                self.objects[obj_id]['trajectory'].pop(0)

            self.disappeared[obj_id] = 0

            used_rows.add(row)
            used_cols.add(col)

        # Handle unmatched existing objects
        unused_rows = set(range(len(object_ids))) - used_rows
        for row in unused_rows:
            obj_id = object_ids[row]
            self.disappeared[obj_id] += 1
            if self.disappeared[obj_id] > self.max_disappeared:
                self._deregister(obj_id)

        # Handle new incoming detections
        unused_cols = set(range(len(input_centroids))) - used_cols
        for col in unused_cols:
            self._register(detections[col], input_centroids[col])

        return self.get_tracked_objects()

    def _register(self, detection: Dict[str, Any], centroid: Tuple[int, int]):
        obj_id = self.next_object_id
        self.next_object_id += 1
        
        self.objects[obj_id] = {
            'id': obj_id,
            'class': detection['class'],
            'confidence': detection['confidence'],
            'box': detection['box'],
            'centroid': centroid,
            'color': detection['color'],
            'speed_kmh': 50.0,
            'collision_warning': False,
            'trajectory': [centroid]
        }
        self.disappeared[obj_id] = 0

    def _deregister(self, obj_id: int):
        if obj_id in self.objects:
            del self.objects[obj_id]
        if obj_id in self.disappeared:
            del self.disappeared[obj_id]

    def get_tracked_objects(self) -> List[Dict[str, Any]]:
        return list(self.objects.values())

    def draw_tracking(self, image: np.ndarray, tracked_objects: List[Dict[str, Any]], 
                      draw_trails: bool = True, show_speed: bool = True,
                      box_thickness: int = 1, font_size: int = 8,
                      badge_style: str = "no_badge", box_style: str = "rectangle",
                      font_scale: float = None) -> np.ndarray:
        """
        Renders persistent track badges, velocity tags, and motion vector trails with sleek styling.
        """
        annotated = image.copy()
        
        # 1. Motion trails drawn in OpenCV for speed (only for genuinely moving objects)
        if draw_trails:
            for obj in tracked_objects:
                color = (0, 0, 255) if obj['collision_warning'] else obj['color']
                trajectory = obj['trajectory']
                if len(trajectory) >= 4:
                    total_disp = np.hypot(trajectory[-1][0] - trajectory[0][0], trajectory[-1][1] - trajectory[0][1])
                    # Only draw trail if object has moved at least 20 pixels (prevents scribbles on stationary cars)
                    if total_disp > 20:
                        recent_pts = trajectory[-10:] # Keep only recent 10 points
                        for k in range(1, len(recent_pts)):
                            pt1 = recent_pts[k - 1]
                            pt2 = recent_pts[k]
                            cv2.line(annotated, pt1, pt2, color, 2, cv2.LINE_AA)

        # 2. Convert to PIL for crisp TrueType rendering of boxes and badges
        img_rgb = cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(img_rgb).convert("RGBA")
        draw = ImageDraw.Draw(pil_img, "RGBA")
        img_w, img_h = pil_img.size

        # Dynamic Resolution Scaling Factor
        res_scale = max(1.0, min(img_w, img_h) / 540.0)

        # Proportional line thickness and font size
        base_thick = box_thickness if box_thickness is not None else 1
        actual_thickness = max(1, int(round(base_thick * res_scale)))

        base_font_size = font_size if font_size is not None else 9
        if font_scale is not None:
            base_font_size = max(7, min(16, int(font_scale * 22)))
        actual_font_size = max(8, int(round(base_font_size * res_scale)))
        font = _get_pil_font(actual_font_size)

        pad_x = max(3, int(round(4 * res_scale)))
        pad_y = max(2, int(round(2 * res_scale)))
        shadow_dist = max(1, int(round(res_scale)))

        for obj in tracked_objects:
            x, y, w, h = obj['box']
            bgr = (0, 0, 255) if obj['collision_warning'] else obj['color']
            rgb = (bgr[2], bgr[1], bgr[0])
            obj_id = obj['id']
            cname = obj['class'].lower()
            speed = obj['speed_kmh']

            # Current box line thickness
            cur_thick = max(actual_thickness + 1, 2) if obj['collision_warning'] else actual_thickness

            # Draw box or corner brackets
            if box_style == "corners":
                c_len = max(4, min(int(w // 4), int(h // 4), int(round(12 * res_scale))))
                draw.line([(x, y), (x + c_len, y)], fill=(*rgb, 255), width=cur_thick)
                draw.line([(x, y), (x, y + c_len)], fill=(*rgb, 255), width=cur_thick)
                draw.line([(x + w, y), (x + w - c_len, y)], fill=(*rgb, 255), width=cur_thick)
                draw.line([(x + w, y), (x + w, y + c_len)], fill=(*rgb, 255), width=cur_thick)
                draw.line([(x, y + h), (x + c_len, y + h)], fill=(*rgb, 255), width=cur_thick)
                draw.line([(x, y + h), (x, y + h - c_len)], fill=(*rgb, 255), width=cur_thick)
                draw.line([(x + w, y + h), (x + w - c_len, y + h)], fill=(*rgb, 255), width=cur_thick)
                draw.line([(x + w, y + h), (x + w, y + h - c_len)], fill=(*rgb, 255), width=cur_thick)
            elif box_style == "rectangle":
                draw.rectangle([x, y, x + w, y + h], outline=(*rgb, 255), width=cur_thick)

            # Skip text if none
            if badge_style == "none":
                continue

            # Format label badge
            if obj['collision_warning']:
                label = f"BRAKE! #{obj_id} {cname} {int(speed)}km/h"
            elif show_speed and cname in {'car', 'truck', 'bus', 'motorcycle'}:
                label = f"#{obj_id} {cname} {int(speed)}km/h"
            else:
                label = f"#{obj_id} {cname}"

            bbox = draw.textbbox((0, 0), label, font=font)
            tw = bbox[2] - bbox[0]
            th = bbox[3] - bbox[1]

            if badge_style in {"no_badge", "minimal"}:
                tx = x + int(round(2 * res_scale))
                ty = max(0, y - th - int(round(3 * res_scale)))
                for dx in range(-shadow_dist, shadow_dist + 1):
                    for dy in range(-shadow_dist, shadow_dist + 1):
                        if dx != 0 or dy != 0:
                            draw.text((tx + dx, ty + dy), label, fill=(0, 0, 0, 230), font=font)
                draw.text((tx, ty), label, fill=(*rgb, 255), font=font)

            elif badge_style in {"micro_tag", "tag", "solid"}:
                bx1 = x
                by1 = max(0, y - th - 2 * pad_y)
                bx2 = x + tw + 2 * pad_x
                by2 = by1 + th + 2 * pad_y
                draw.rectangle([bx1, by1, bx2, by2], fill=(*rgb, 255))
                draw.text((bx1 + pad_x, by1 + pad_y - 1), label, fill=(15, 15, 15, 255), font=font)

            elif badge_style in {"obsidian_hud", "micro_pill", "sleek", "glass_pill"}:
                bx1 = x
                by1 = max(0, y - th - 2 * pad_y)
                bx2 = x + tw + 2 * pad_x
                by2 = by1 + th + 2 * pad_y
                bg_col = (15, 23, 42, 230) if not obj['collision_warning'] else (180, 20, 30, 235)
                pill_radius = max(2, int(round(3 * res_scale)))
                draw.rounded_rectangle([bx1, by1, bx2, by2], radius=pill_radius,
                                       fill=bg_col, outline=(*rgb, 220), width=1)
                draw.text((bx1 + pad_x, by1 + pad_y - 1), label, fill=(255, 255, 255, 255), font=font)

        res_rgb = np.array(pil_img.convert("RGB"))
        return cv2.cvtColor(res_rgb, cv2.COLOR_RGB2BGR)
