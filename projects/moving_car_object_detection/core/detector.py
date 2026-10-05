"""
Core Vision Detector: YOLOv8 ONNX Road Object Detection Engine
Performs real-time multi-class object detection across vehicles, pedestrians, and road assets.
Uses onnxruntime for ultra-fast, zero-overhead CPU/GPU inference.
"""

import os
from pathlib import Path
from typing import Dict, List, Tuple, Any
import numpy as np
import cv2
import onnxruntime as ort
from PIL import Image, ImageDraw, ImageFont

_FONT_CACHE: Dict[int, Any] = {}

def _get_pil_font(size: int):
    """Loads and caches crisp anti-aliased TrueType fonts for high-definition rendering."""
    if size not in _FONT_CACHE:
        font_candidates = [
            "C:/Windows/Fonts/segoeui.ttf",
            "C:/Windows/Fonts/arial.ttf",
            "C:/Windows/Fonts/calibri.ttf"
        ]
        chosen = None
        for fc in font_candidates:
            if os.path.exists(fc):
                try:
                    chosen = ImageFont.truetype(fc, size)
                    break
                except Exception:
                    pass
        if chosen is None:
            chosen = ImageFont.load_default()
        _FONT_CACHE[size] = chosen
    return _FONT_CACHE[size]

COCO_CLASSES = [
    'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat',
    'traffic light', 'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird', 'cat',
    'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear', 'zebra', 'giraffe', 'backpack',
    'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball',
    'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard', 'tennis racket',
    'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple',
    'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair',
    'couch', 'potted plant', 'bed', 'dining table', 'toilet', 'tv', 'laptop', 'mouse',
    'remote', 'keyboard', 'cell phone', 'microwave', 'oven', 'toaster', 'sink', 'refrigerator',
    'book', 'clock', 'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush'
]

# High-contrast color palette matching executive urban dashcam visuals
# BGR format for OpenCV
CLASS_COLORS = {
    'car': (21, 220, 250),           # Bright Yellow
    'bus': (180, 50, 230),          # Bright Magenta / Fuchsia
    'truck': (22, 130, 255),         # Vivid Orange
    'person': (235, 60, 180),        # Hot Pink / Magenta
    'motorcycle': (230, 100, 130),   # Purple / Lavender
    'bicycle': (180, 200, 20),       # Cyan / Teal
    'traffic light': (240, 140, 40), # Electric Sky Blue
    'stop sign': (50, 50, 240),      # Crimson Red
    'handbag': (40, 220, 60),        # Lime Green
    'backpack': (40, 220, 60),       # Lime Green
    'suitcase': (40, 220, 60),       # Lime Green
}
DEFAULT_COLOR = (200, 200, 200)

ROAD_TARGET_CLASSES = {'car', 'person', 'bus', 'truck', 'motorcycle', 'bicycle', 'traffic light', 'stop sign', 'handbag', 'backpack'}

class RoadObjectDetector:
    def __init__(self, model_path: str = None, input_size: int = 640):
        if model_path is None:
            base_dir = Path(__file__).resolve().parent.parent
            model_path = str(base_dir / "models" / "yolov8n_640.onnx")
            
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"YOLOv8 ONNX model not found at: {model_path}")

        self.model_path = model_path
        self.input_size = input_size
        
        # Initialize ONNX Runtime session
        opts = ort.SessionOptions()
        opts.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL
        self.session = ort.InferenceSession(model_path, opts, providers=['CPUExecutionProvider'])
        
        self.input_name = self.session.get_inputs()[0].name
        self.output_name = self.session.get_outputs()[0].name
        
        # Auto-detect input dimension from ONNX model if specified
        try:
            model_dim = self.session.get_inputs()[0].shape[2]
            if isinstance(model_dim, int) and model_dim > 0:
                self.input_size = model_dim
        except Exception:
            pass

    @staticmethod
    def letterbox(im: np.ndarray, new_shape: Tuple[int, int] = (640, 640), color: Tuple[int, int, int] = (114, 114, 114)):
        """Aspect ratio preserving resize with letterbox padding."""
        shape = im.shape[:2] # [height, width]
        r = min(new_shape[0] / shape[0], new_shape[1] / shape[1])
        new_unpad = int(round(shape[1] * r)), int(round(shape[0] * r))
        dw, dh = new_shape[1] - new_unpad[0], new_shape[0] - new_unpad[1]
        dw /= 2
        dh /= 2
        im_resized = cv2.resize(im, new_unpad, interpolation=cv2.INTER_LINEAR)
        top, bottom = int(round(dh - 0.1)), int(round(dh + 0.1))
        left, right = int(round(dw - 0.1)), int(round(dw + 0.1))
        im_padded = cv2.copyMakeBorder(im_resized, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)
        return im_padded, r, (dw, dh)

    def detect(self, image: np.ndarray, conf_threshold: float = 0.20, iou_threshold: float = 0.45,
               filter_road_classes_only: bool = True) -> List[Dict[str, Any]]:
        """
        Runs object detection on a BGR image.
        Returns list of detections with bounding box, class, confidence, and color.
        """
        h_orig, w_orig = image.shape[:2]
        lb_img, ratio, (pad_w, pad_h) = self.letterbox(image, (self.input_size, self.input_size))
        
        # Convert BGR to RGB, normalize [0, 1], transpose to [1, 3, 640, 640]
        input_tensor = (cv2.cvtColor(lb_img, cv2.COLOR_BGR2RGB).astype(np.float32) / 255.0)
        input_tensor = input_tensor.transpose(2, 0, 1)[np.newaxis, :]

        # Run inference
        outputs = self.session.run(None, {self.input_name: input_tensor})
        predictions = np.squeeze(outputs[0]).T # shape [8400, 84]

        boxes = []
        confidences = []
        class_ids = []

        for row in predictions:
            classes_scores = row[4:]
            max_score = float(np.max(classes_scores))
            if max_score >= conf_threshold:
                class_id = int(np.argmax(classes_scores))
                cname = COCO_CLASSES[class_id]
                
                if filter_road_classes_only and cname not in ROAD_TARGET_CLASSES:
                    continue

                cx, cy, bw, bh = float(row[0]), float(row[1]), float(row[2]), float(row[3])
                # Unpad and scale back to original image coordinates
                x1 = int(round((cx - 0.5 * bw - pad_w) / ratio))
                y1 = int(round((cy - 0.5 * bh - pad_h) / ratio))
                w = int(round(bw / ratio))
                h = int(round(bh / ratio))

                # Clip to image bounds
                x1 = max(0, min(x1, w_orig - 1))
                y1 = max(0, min(y1, h_orig - 1))
                w = max(1, min(w, w_orig - x1))
                h = max(1, min(h, h_orig - y1))

                boxes.append([x1, y1, w, h])
                confidences.append(max_score)
                class_ids.append(class_id)

        if not boxes:
            return []

        indices = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, iou_threshold)
        
        detections = []
        for idx in indices:
            cid = class_ids[idx]
            cname = COCO_CLASSES[cid]
            conf = confidences[idx]
            box = boxes[idx]
            color = CLASS_COLORS.get(cname, DEFAULT_COLOR)
            
            detections.append({
                'class': cname,
                'class_id': cid,
                'confidence': conf,
                'box': box,  # [x, y, w, h]
                'color': color
            })

        # Sort by confidence descending
        detections.sort(key=lambda d: d['confidence'], reverse=True)
        return detections

    def draw_detections(self, image: np.ndarray, detections: List[Dict[str, Any]], 
                        show_conf: bool = False, box_thickness: int = 2,
                        font_size: int = None, badge_style: str = "default",
                        box_style: str = "rectangle", label_content: str = "name_only",
                        font_scale: float = None) -> np.ndarray:
        """
        Renders crisp green bounding boxes with solid green tags placed clearly ABOVE the boxes.
        Matches the exact Ultralytics/COCO reference standard with crisp white text.
        """
        img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(img_rgb).convert("RGBA")
        draw = ImageDraw.Draw(pil_img, "RGBA")
        img_w, img_h = pil_img.size

        # Fresh vibrant green matching user reference sample image
        green_col = (115, 205, 95)

        base_dim = min(img_w, img_h)
        calc_font_size = max(11, min(18, int(base_dim * 0.016))) if font_size is None else font_size
        try:
            font = _get_pil_font(calc_font_size)
        except Exception:
            font = ImageFont.load_default()

        pad_x = max(4, int(calc_font_size * 0.35))
        pad_y = max(2, int(calc_font_size * 0.2))

        for det in detections:
            x, y, w, h = det['box']
            cname = det['class'].lower()
            
            # Clean 2px green bounding box
            draw.rectangle([x, y, x + w, y + h], outline=(*green_col, 255), width=2)

            if label_content == "none":
                continue

            # Format label
            if show_conf or label_content == "name_conf":
                label = f"{cname} {int(det['confidence'] * 100)}%"
            else:
                label = f"{cname}"

            bbox = draw.textbbox((0, 0), label, font=font)
            tw = bbox[2] - bbox[0]
            th = bbox[3] - bbox[1]

            tag_w = tw + pad_x * 2
            tag_h = th + pad_y * 2

            # Position tag clearly ABOVE the bounding box with 1px margin
            if y >= tag_h + 2:
                by1 = y - tag_h - 1
                by2 = y - 1
            else:
                by1 = y + 1
                by2 = y + tag_h + 1
            bx1 = x
            bx2 = x + tag_w

            # Solid filled green tag
            draw.rectangle([bx1, by1, bx2, by2], fill=(*green_col, 255))
            # Crisp bold white text inside tag
            draw.text((bx1 + pad_x, by1 + pad_y - 1), label, fill=(255, 255, 255, 255), font=font)

        # Convert back to OpenCV BGR
        res_rgb = np.array(pil_img.convert("RGB"))
        return cv2.cvtColor(res_rgb, cv2.COLOR_RGB2BGR)

