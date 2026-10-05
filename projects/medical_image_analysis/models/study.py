"""
Data models and defensive dataclasses for Medical Image Analysis
"""
from dataclasses import dataclass
from typing import Optional

@dataclass
class Patient:
    patient_id: str
    full_name: str
    age: int
    gender: str
    medical_record_number: str

    def __post_init__(self):
        if self.age < 0 or self.age > 130:
            raise ValueError(f"Invalid patient age: {self.age}")
        if not self.medical_record_number:
            raise ValueError("MRN cannot be empty")

@dataclass
class ImagingStudy:
    study_id: str
    patient_id: str
    study_timestamp: str
    modality: str = "CHEST_XRAY"
    body_part: str = "CHEST"
    image_filename: str = "scan.png"
    image_width: int = 512
    image_height: int = 512
    mean_intensity: float = 128.0
    contrast_ratio: float = 1.0
    status: str = "COMPLETED"

    def __post_init__(self):
        if self.image_width <= 0 or self.image_height <= 0:
            raise ValueError("Image dimensions must be positive integers")

@dataclass
class DiagnosticFinding:
    finding_id: str
    study_id: str
    patient_id: str
    pathology_detected: str
    confidence_score: float
    severity_tier: str
    affected_zone: str = "BILATERAL"
    radiologist_verified: bool = False

    def __post_init__(self):
        if not (0.0 <= self.confidence_score <= 100.0):
            raise ValueError(f"Confidence score {self.confidence_score} must be between 0 and 100")
        if self.severity_tier not in ["NORMAL", "MONITOR", "CRITICAL"]:
            raise ValueError(f"Invalid severity tier: {self.severity_tier}")

@dataclass
class RadiologistReview:
    review_id: str
    finding_id: str
    doctor_id: str
    doctor_name: str
    diagnosis_confirmed: bool = True
    clinical_notes: str = ""
