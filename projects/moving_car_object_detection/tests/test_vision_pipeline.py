"""
Unit and Integration Test Suite for Moving Car and Road Object Detection
Executes the 10 automated safety test suites via pytest.
"""

import os
from pathlib import Path
import pytest
from core.detector import RoadObjectDetector
from core.tracker import RoadObjectTracker
from agents.qa_testing_agent import QATestingAgent

BASE_DIR = Path(__file__).resolve().parent.parent
SAMPLE_IMAGE = str(BASE_DIR / "data" / "sample_images" / "urban_street_dashcam.jpg")

@pytest.fixture(scope="module")
def detector():
    return RoadObjectDetector()

@pytest.fixture(scope="module")
def tracker():
    return RoadObjectTracker()

@pytest.fixture(scope="module")
def qa_agent(detector):
    return QATestingAgent(detector=detector)

def test_onnx_model_loading(detector):
    assert detector.session is not None
    assert detector.input_size == 640

def test_letterbox_preprocessing(detector):
    import numpy as np
    canvas = np.zeros((480, 854, 3), dtype=np.uint8)
    lb, r, (dw, dh) = detector.letterbox(canvas, (640, 640))
    assert lb.shape == (640, 640, 3)
    assert r > 0

def test_blank_canvas_zero_false_alarms(detector):
    import numpy as np
    blank = np.ones((640, 640, 3), dtype=np.uint8) * 128
    dets = detector.detect(blank, conf_threshold=0.3)
    assert len(dets) == 0

def test_urban_road_car_detection(detector):
    import cv2
    img = cv2.imread(SAMPLE_IMAGE)
    assert img is not None
    dets = detector.detect(img, conf_threshold=0.15)
    cars = [d for d in dets if d['class'] in {'car', 'truck', 'bus'}]
    assert len(cars) > 0, "Should detect at least 1 car/vehicle in urban street scene"

def test_urban_road_pedestrian_detection(detector):
    import cv2
    img = cv2.imread(SAMPLE_IMAGE)
    dets = detector.detect(img, conf_threshold=0.15)
    pedestrians = [d for d in dets if d['class'] == 'person']
    assert len(pedestrians) > 0, "Should detect pedestrians on sidewalk"

def test_multi_object_tracking_continuity(tracker):
    sim_d1 = [{'class': 'car', 'confidence': 0.85, 'box': [100, 200, 80, 80], 'color': (21, 220, 250)}]
    sim_d2 = [{'class': 'car', 'confidence': 0.88, 'box': [104, 204, 80, 80], 'color': (21, 220, 250)}]
    tr1 = tracker.update(sim_d1, (480, 640))
    tr2 = tracker.update(sim_d2, (480, 640))
    assert len(tr1) == 1
    assert len(tr2) == 1
    assert tr1[0]['id'] == tr2[0]['id'], "Track ID should remain persistent across consecutive frames"

def test_forward_collision_warning_trigger():
    tr = RoadObjectTracker()
    sim_car_far = [{'class': 'car', 'confidence': 0.9, 'box': [250, 260, 160, 120], 'color': (21, 220, 250)}]
    sim_car_close = [{'class': 'car', 'confidence': 0.9, 'box': [250, 320, 190, 160], 'color': (21, 220, 250)}]
    tr.update(sim_car_far, (480, 640))
    res = tr.update(sim_car_close, (480, 640))
    assert res[0]['collision_warning'] is True, "Rapid approach in center lane should trigger collision warning"

def test_all_10_safety_tests_via_agent(qa_agent):
    report = qa_agent.run_all_safety_tests(sample_image_path=SAMPLE_IMAGE)
    assert report['all_passed'] is True, f"All 10 tests must pass, but got: {report}"
    assert report['passed'] == 10
