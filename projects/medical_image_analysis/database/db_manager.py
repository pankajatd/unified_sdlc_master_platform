"""
Database manager for Medical Image Analysis operations (SQLite)
"""
import sqlite3
import os
from pathlib import Path
from typing import List, Dict, Any, Optional

class MedicalDatabaseManager:
    def __init__(self, db_path: str = "imaging.db"):
        self.db_path = db_path
        self._init_db()

    def get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        schema_path = Path(__file__).resolve().parent / "schema.sql"
        if schema_path.exists():
            with open(schema_path, "r", encoding="utf-8") as f:
                schema_sql = f.read()
            with self.get_connection() as conn:
                conn.executescript(schema_sql)

    def create_patient(self, patient_id: str, full_name: str, age: int, gender: str, mrn: str):
        with self.get_connection() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO patients (patient_id, full_name, age, gender, medical_record_number) VALUES (?, ?, ?, ?, ?)",
                (patient_id, full_name, age, gender, mrn)
            )

    def insert_study(self, study_dict: Dict[str, Any]):
        with self.get_connection() as conn:
            conn.execute(
                """INSERT INTO imaging_studies 
                   (study_id, patient_id, modality, body_part, study_timestamp, image_filename, image_width, image_height, mean_intensity, contrast_ratio, status)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    study_dict["study_id"],
                    study_dict["patient_id"],
                    study_dict.get("modality", "CHEST_XRAY"),
                    study_dict.get("body_part", "CHEST"),
                    study_dict["study_timestamp"],
                    study_dict.get("image_filename", "scan.png"),
                    study_dict.get("image_width", 512),
                    study_dict.get("image_height", 512),
                    study_dict.get("mean_intensity", 128.0),
                    study_dict.get("contrast_ratio", 1.0),
                    study_dict.get("status", "COMPLETED")
                )
            )

    def record_finding(self, finding_dict: Dict[str, Any]):
        with self.get_connection() as conn:
            conn.execute(
                """INSERT INTO diagnostic_findings 
                   (finding_id, study_id, patient_id, pathology_detected, confidence_score, severity_tier, affected_zone, radiologist_verified)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    finding_dict["finding_id"],
                    finding_dict["study_id"],
                    finding_dict["patient_id"],
                    finding_dict["pathology_detected"],
                    finding_dict["confidence_score"],
                    finding_dict["severity_tier"],
                    finding_dict.get("affected_zone", "BILATERAL"),
                    1 if finding_dict.get("radiologist_verified", False) else 0
                )
            )

    def record_doctor_review(self, review_dict: Dict[str, Any]):
        with self.get_connection() as conn:
            conn.execute(
                """INSERT INTO doctor_reviews 
                   (review_id, finding_id, doctor_id, doctor_name, diagnosis_confirmed, clinical_notes)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (
                    review_dict["review_id"],
                    review_dict["finding_id"],
                    review_dict["doctor_id"],
                    review_dict["doctor_name"],
                    1 if review_dict.get("diagnosis_confirmed", True) else 0,
                    review_dict.get("clinical_notes", "")
                )
            )

    def get_findings_for_study(self, study_id: str) -> List[Dict[str, Any]]:
        with self.get_connection() as conn:
            cur = conn.execute("SELECT * FROM diagnostic_findings WHERE study_id = ? ORDER BY created_at DESC", (study_id,))
            return [dict(row) for row in cur.fetchall()]

    def get_all_studies(self, limit: int = 20) -> List[Dict[str, Any]]:
        with self.get_connection() as conn:
            cur = conn.execute("SELECT * FROM imaging_studies ORDER BY study_timestamp DESC LIMIT ?", (limit,))
            return [dict(row) for row in cur.fetchall()]

    def get_all_patients(self) -> List[Dict[str, Any]]:
        with self.get_connection() as conn:
            cur = conn.execute("SELECT * FROM patients ORDER BY full_name ASC")
            return [dict(row) for row in cur.fetchall()]

    def get_all_reviews(self, limit: int = 20) -> List[Dict[str, Any]]:
        with self.get_connection() as conn:
            cur = conn.execute("SELECT * FROM doctor_reviews ORDER BY review_timestamp DESC LIMIT ?", (limit,))
            return [dict(row) for row in cur.fetchall()]

    def clear_history(self):
        with self.get_connection() as conn:
            conn.execute("DELETE FROM doctor_reviews;")
            conn.execute("DELETE FROM diagnostic_findings;")
            conn.execute("DELETE FROM imaging_studies;")
            conn.commit()

    def get_system_stats(self) -> Dict[str, int]:
        with self.get_connection() as conn:
            p = conn.execute("SELECT COUNT(*) FROM patients").fetchone()[0]
            s = conn.execute("SELECT COUNT(*) FROM imaging_studies").fetchone()[0]
            f = conn.execute("SELECT COUNT(*) FROM diagnostic_findings").fetchone()[0]
            r = conn.execute("SELECT COUNT(*) FROM doctor_reviews").fetchone()[0]
            return {
                "patients_count": p,
                "studies_count": s,
                "findings_count": f,
                "reviews_count": r
            }
