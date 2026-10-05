"""
Automated Pytest Suite for Multimodal Medical Image Analysis Platform
Validates detection, scoring, and rule execution across X-Ray, MRI, and CT Scans.
"""
import os
import tempfile
import shutil
import pytest
from database.db_manager import MedicalDatabaseManager
from services.diagnostic_scorer import DiagnosticScorer
from models.study import Patient, ImagingStudy, DiagnosticFinding

@pytest.fixture
def setup_scorer():
    temp_dir = tempfile.mkdtemp()
    temp_db = os.path.join(temp_dir, "test_imaging.db")
    db = MedicalDatabaseManager(db_path=temp_db)
    db.create_patient("PAT_001", "Jane Doe", 45, "F", "MRN-12345")
    scorer = DiagnosticScorer(db_manager=db)
    yield scorer, db
    try:
        shutil.rmtree(temp_dir, ignore_errors=True)
    except Exception:
        pass

def test_normal_xray_approved(setup_scorer):
    scorer, _ = setup_scorer
    study = {
        "study_id": "STU_NORM_1",
        "patient_id": "PAT_001",
        "study_timestamp": "2026-09-30 08:00:00",
        "cardiothoracic_ratio": 0.42,
        "focal_opacity_index": 0.10,
        "nodule_size_mm": 0.0,
        "contrast_deviation": 50.0,
        "pathology_hint": "NORMAL"
    }
    result = scorer.evaluate_study(study)
    assert result["severity_tier"] == "NORMAL"
    assert result["confidence_score"] <= 20.0
    assert len(result["findings"]) == 0

def test_pneumonia_consolidation_detected(setup_scorer):
    scorer, _ = setup_scorer
    study = {
        "study_id": "STU_PNEU_1",
        "patient_id": "PAT_001",
        "study_timestamp": "2026-09-30 09:30:00",
        "cardiothoracic_ratio": 0.43,
        "focal_opacity_index": 0.85,
        "pathology_hint": "PNEUMONIA"
    }
    result = scorer.evaluate_study(study)
    assert result["severity_tier"] == "CRITICAL"
    assert "PNEUMONIA" in result["pathology_detected"]
    assert any("Consolidation opacity" in f for f in result["findings"])

def test_cardiomegaly_ratio_detected(setup_scorer):
    scorer, _ = setup_scorer
    study = {
        "study_id": "STU_CARD_1",
        "patient_id": "PAT_001",
        "study_timestamp": "2026-09-30 11:00:00",
        "cardiothoracic_ratio": 0.58,
        "pathology_hint": "CARDIOMEGALY"
    }
    result = scorer.evaluate_study(study)
    assert result["severity_tier"] == "CRITICAL"
    assert "CARDIOMEGALY" in result["pathology_detected"]
    assert any("Cardiomegaly detected" in f for f in result["findings"])

def test_pulmonary_nodule_detected(setup_scorer):
    scorer, _ = setup_scorer
    study = {
        "study_id": "STU_NOD_1",
        "patient_id": "PAT_001",
        "study_timestamp": "2026-09-30 14:15:00",
        "nodule_size_mm": 14.5,
        "pathology_hint": "NODULE"
    }
    result = scorer.evaluate_study(study)
    assert result["severity_tier"] == "CRITICAL"
    assert "NODULE" in result["pathology_detected"]
    assert any("pulmonary" in f.lower() or "nodule" in f.lower() for f in result["findings"])

def test_brain_mri_tumor_detected(setup_scorer):
    scorer, _ = setup_scorer
    study = {
        "study_id": "STU_MRI_1",
        "patient_id": "PAT_001",
        "study_timestamp": "2026-09-30 15:30:00",
        "nodule_size_mm": 28.4,
        "pathology_hint": "BRAIN_MRI_TUMOR"
    }
    result = scorer.evaluate_study(study)
    assert result["severity_tier"] == "CRITICAL"
    assert "TUMOR" in result["pathology_detected"]
    assert any("tumor" in f.lower() or "neoplasm" in f.lower() for f in result["findings"])

def test_ct_acute_stroke_detected(setup_scorer):
    scorer, _ = setup_scorer
    study = {
        "study_id": "STU_CT_STR_1",
        "patient_id": "PAT_001",
        "modality": "CT",
        "hu_disparity": 8.4,
        "pathology_hint": "CT_STROKE"
    }
    result = scorer.evaluate_study(study)
    assert result["severity_tier"] == "CRITICAL"
    assert "STROKE" in result["pathology_detected"]
    assert any("Stroke" in f for f in result["findings"])

def test_subtle_pneumothorax_detected(setup_scorer):
    scorer, _ = setup_scorer
    study = {
        "study_id": "STU_XRAY_PTX_1",
        "patient_id": "PAT_001",
        "modality": "X-RAY",
        "pleural_retraction_pct": 14.0,
        "pathology_hint": "XRAY_PNEUMOTHORAX"
    }
    result = scorer.evaluate_study(study)
    assert result["severity_tier"] == "CRITICAL"
    assert "PNEUMOTHORAX" in result["pathology_detected"]
    assert any("Pneumothorax" in f for f in result["findings"])

def test_mri_ms_micro_plaques_detected(setup_scorer):
    scorer, _ = setup_scorer
    study = {
        "study_id": "STU_MRI_MS_1",
        "patient_id": "PAT_001",
        "modality": "MRI",
        "plaque_count": 4,
        "pathology_hint": "MRI_MS_PLAQUES"
    }
    result = scorer.evaluate_study(study)
    assert result["severity_tier"] == "CRITICAL"
    assert "MS_MICRO_PLAQUES" in result["pathology_detected"]
    assert any("Multiple Sclerosis" in f for f in result["findings"])

def test_poor_image_quality_flagged(setup_scorer):
    scorer, _ = setup_scorer
    study = {
        "study_id": "STU_BLUR_1",
        "patient_id": "PAT_001",
        "study_timestamp": "2026-09-30 16:00:00",
        "contrast_deviation": 12.0,
        "is_poor_quality": True,
        "pathology_hint": "POOR_QUALITY"
    }
    result = scorer.evaluate_study(study)
    assert result["severity_tier"] == "MONITOR"
    assert any("quality" in f.lower() for f in result["findings"])

def test_bilateral_asymmetry_flagged(setup_scorer):
    scorer, _ = setup_scorer
    study = {
        "study_id": "STU_ASYM_1",
        "patient_id": "PAT_001",
        "study_timestamp": "2026-09-30 16:30:00",
        "hemithorax_asymmetry": 0.48,
        "pathology_hint": "ASYMMETRY"
    }
    result = scorer.evaluate_study(study)
    assert result["severity_tier"] == "MONITOR"
    assert any("asymmetry" in f.lower() for f in result["findings"])
