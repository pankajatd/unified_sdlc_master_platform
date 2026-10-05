"""
Configuration settings for Medical Image Analysis Platform
"""
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
SAMPLE_SCANS_DIR = DATA_DIR / "sample_scans"
DB_PATH = BASE_DIR / "imaging.db"

PYTHON_EXE = r"C:\Users\panka\.gemini\antigravity\scratch\ocr_multiagent_system\venv_ocr\Scripts\python.exe"
MAX_HEALING_ITERATIONS = 3
DEFAULT_PORT = 8506
