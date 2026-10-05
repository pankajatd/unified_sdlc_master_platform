"""
Composite Diagnostic Scoring & Clinical Severity Engine
Supports X-Rays, MRIs, and CT Scans with Subtle Anomaly Triage.
"""
import time
import uuid
from typing import Dict, Any, List
from rules.clinical_rules import (
    AcuteIschemicStrokeRule,
    SubtlePneumothoraxRule,
    MultipleSclerosisPlaqueRule,
    PneumoniaConsolidationRule,
    CardiothoracicRatioRule,
    PulmonaryNoduleRule,
    ImageQualityRule,
    BilateralAsymmetryRule
)

class DiagnosticScorer:
    def __init__(self, db_manager=None):
        self.db_manager = db_manager
        self.rules = [
            AcuteIschemicStrokeRule(),
            SubtlePneumothoraxRule(),
            MultipleSclerosisPlaqueRule(),
            PneumoniaConsolidationRule(),
            CardiothoracicRatioRule(),
            PulmonaryNoduleRule(),
            ImageQualityRule(),
            BilateralAsymmetryRule()
        ]

    def evaluate_study(self, study_payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluates a medical imaging study against clinical rules across X-Rays, MRIs, and CT Scans.
        Returns composite severity verdict, confidence score, and triggered findings.
        """
        triggered_findings: List[str] = []
        rule_scores: List[float] = []

        for rule in self.rules:
            triggered, score, desc = rule.evaluate(study_payload)
            if triggered:
                triggered_findings.append(desc)
                rule_scores.append(score)

        if not rule_scores:
            composite_score = 5.0
            primary_pathology = "NORMAL_STUDY"
            severity_tier = "NORMAL"
        else:
            composite_score = round(max(rule_scores), 1)
            
            # Determine primary pathology
            first_finding = triggered_findings[0]
            if "Stroke" in first_finding or "Ischemic" in first_finding:
                primary_pathology = "CT_ACUTE_STROKE"
            elif "Pneumothorax" in first_finding:
                primary_pathology = "XRAY_PNEUMOTHORAX"
            elif "Multiple Sclerosis" in first_finding:
                primary_pathology = "MRI_MS_MICRO_PLAQUES"
            elif "Pneumonia" in first_finding:
                primary_pathology = "PNEUMONIA_CONSOLIDATION"
            elif "Cardiomegaly" in first_finding:
                primary_pathology = "CARDIOMEGALY"
            elif "Glioblastoma" in first_finding or "Neoplasm" in first_finding:
                primary_pathology = "BRAIN_MRI_TUMOR"
            elif "Ground-Glass" in first_finding:
                primary_pathology = "CT_GROUND_GLASS_NODULE"
            elif "nodule" in first_finding.lower():
                primary_pathology = "PULMONARY_NODULE"
            elif "quality" in first_finding:
                primary_pathology = "ARTIFACT_UNREADABLE"
            else:
                primary_pathology = "ASYMMETRY_SUSPICIOUS"

            if composite_score >= 80.0:
                severity_tier = "CRITICAL"
            elif composite_score >= 40.0:
                severity_tier = "MONITOR"
            else:
                severity_tier = "NORMAL"

        result = {
            "study_id": study_payload.get("study_id", f"STU_{int(time.time())}"),
            "patient_id": study_payload.get("patient_id", "PAT_UNKNOWN"),
            "pathology_detected": primary_pathology,
            "confidence_score": composite_score,
            "severity_tier": severity_tier,
            "findings": triggered_findings,
            "timestamp": study_payload.get("study_timestamp", time.strftime("%Y-%m-%d %H:%M:%S"))
        }

        # Persist to database if db_manager is active
        if self.db_manager:
            try:
                self.db_manager.insert_study(study_payload)
            except Exception:
                pass
            try:
                finding_record = {
                    "finding_id": f"FIND_{uuid.uuid4().hex[:8].upper()}",
                    "study_id": result["study_id"],
                    "patient_id": result["patient_id"],
                    "pathology_detected": result["pathology_detected"],
                    "confidence_score": result["confidence_score"],
                    "severity_tier": result["severity_tier"],
                    "affected_zone": study_payload.get("body_part", "BRAIN/CHEST"),
                    "radiologist_verified": False
                }
                self.db_manager.record_finding(finding_record)
            except Exception:
                pass

        return result
