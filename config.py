"""
Unified Autonomous SDLC Multi-Agent Platform - Configuration
Houses all 3 projects created with the 7 SDLC Agents:
1. Moving Car & Road Object Detection Platform (AutoVision AI)
2. Medical Image Analysis Platform (MedVision AI)
3. Banking Fraud Detection System (FraudGuard AI)
"""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

# Projects Directory references - Supports both self-contained repo & local dev
if (BASE_DIR / "projects" / "moving_car_object_detection").exists():
    MOVING_CAR_DIR = BASE_DIR / "projects" / "moving_car_object_detection"
    MEDICAL_DIR = BASE_DIR / "projects" / "medical_image_analysis"
    BANKING_DIR = BASE_DIR / "projects" / "banking_fraud_system"
else:
    SCRATCH_DIR = BASE_DIR.parent
    MOVING_CAR_DIR = SCRATCH_DIR / "moving_car_object_detection"
    MEDICAL_DIR = SCRATCH_DIR / "medical_image_analysis"
    BANKING_DIR = SCRATCH_DIR / "sdlc_multiagent_system" / "generated_projects" / "banking_fraud_system"

# Assets references
MOVING_CAR_MODELS = MOVING_CAR_DIR / "models"
MOVING_CAR_DATA = MOVING_CAR_DIR / "data"
MOVING_CAR_SAMPLE_IMAGES = MOVING_CAR_DATA / "sample_images"
MOVING_CAR_SAMPLE_VIDEOS = MOVING_CAR_DATA / "sample_videos"

MEDICAL_DATA = MEDICAL_DIR / "data"
MEDICAL_SCANS = MEDICAL_DATA / "matched_scans"
MEDICAL_DB = MEDICAL_DIR / "imaging.db"

BANKING_DB = BANKING_DIR / "banking_system.db"

# Python Executable for subtasks & pytest
PYTHON_EXE = os.environ.get(
    "SDLC_PYTHON_EXE",
    r"C:\Users\panka\.gemini\antigravity\scratch\ocr_multiagent_system\venv_ocr\Scripts\python.exe"
)
if not os.path.exists(PYTHON_EXE):
    import sys
    PYTHON_EXE = sys.executable

# SDLC Limits
MAX_HEALING_ITERATIONS = 3
COMMAND_TIMEOUT_SECONDS = 45
TEST_TIMEOUT_SECONDS = 60

# Prompts Map for the 3 Projects
PROJECT_PROMPTS = {
    "car": (
        "Build an autonomous real-time Moving Car & Road Object Detection Platform "
        "with YOLOv8 ONNX 640x640, centroid motion vector tracking, collision proximity warning, "
        "10 automated road safety test suites, and permanent side-by-side video command center."
    ),
    "medical": (
        "Build an automated Medical Image Analysis and Clinical Decision Support System "
        "with SQLite database, digital image processing for Chest X-Ray findings "
        "(Pneumonia, Cardiomegaly CTR, Pulmonary Nodule, Brain MRI, Head CT), "
        "composite diagnostic scoring, and 10 clinical safety unit tests."
    ),
    "banking": (
        "Build an advanced Banking Fraud Detection System with SQLite database tables, "
        "real-time transaction scoring algorithms, rapid velocity rules, "
        "high-risk merchant category code (MCC) detection, and automated unit tests."
    )
}
