"""
Agent 2: Vision Architect Agent (Architecture Agent)
Designs the neural vision pipeline, ONNX runtime execution provider, anchor dimensions, and COCO class mapping.
"""

from typing import Dict, Any, List

class VisionArchitectureAgent:
    def __init__(self):
        self.agent_name = "Vision Architect"
        self.role_title = "Architecture Agent"
        self.architecture_spec = {
            'backbone': 'CSPDarknet53 with PANet Feature Pyramid',
            'inference_engine': 'ONNX Runtime (CPU/GPU optimized)',
            'input_dimensions': (1, 3, 640, 640),
            'anchor_candidates': 8400,
            'prediction_channels': 84,  # [cx, cy, w, h] + 80 class logits
            'supported_modalities': ['Single Dashcam Image', 'Recorded Road Video (MP4)', 'Live RTSP Stream'],
            'target_road_taxonomy': {
                'vehicles': ['car', 'truck', 'bus', 'motorcycle', 'bicycle'],
                'pedestrians': ['person'],
                'road_infrastructure': ['traffic light', 'stop sign'],
                'accessories': ['handbag', 'backpack', 'suitcase']
            }
        }

    def get_pipeline_blueprint(self) -> Dict[str, Any]:
        return {
            'agent': self.agent_name,
            'role': self.role_title,
            'spec': self.architecture_spec,
            'execution_strategy': 'Zero-copy NumPy tensor streaming into ONNX Runtime Session'
        }

    def validate_model_compatibility(self, input_shape: tuple, output_shape: tuple) -> bool:
        """Verifies that loaded ONNX model conforms to 640x640 YOLOv8 output tensor schema."""
        valid_input = len(input_shape) == 4 and input_shape[2] == 640 and input_shape[3] == 640
        valid_output = len(output_shape) == 3 and output_shape[1] == 84 and output_shape[2] == 8400
        return valid_input and valid_output
