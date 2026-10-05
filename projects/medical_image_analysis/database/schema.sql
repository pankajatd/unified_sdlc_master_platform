-- Medical Image Analysis & Clinical Decision Support Database Schema
CREATE TABLE IF NOT EXISTS patients (
    patient_id TEXT PRIMARY KEY,
    full_name TEXT NOT NULL,
    age INTEGER NOT NULL,
    gender TEXT NOT NULL,
    medical_record_number TEXT UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS imaging_studies (
    study_id TEXT PRIMARY KEY,
    patient_id TEXT NOT NULL,
    modality TEXT DEFAULT 'CHEST_XRAY',
    body_part TEXT DEFAULT 'CHEST',
    study_timestamp TIMESTAMP NOT NULL,
    image_filename TEXT NOT NULL,
    image_width INTEGER DEFAULT 512,
    image_height INTEGER DEFAULT 512,
    mean_intensity REAL,
    contrast_ratio REAL,
    status TEXT DEFAULT 'COMPLETED',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES patients (patient_id)
);

CREATE TABLE IF NOT EXISTS diagnostic_findings (
    finding_id TEXT PRIMARY KEY,
    study_id TEXT NOT NULL,
    patient_id TEXT NOT NULL,
    pathology_detected TEXT NOT NULL,
    confidence_score REAL NOT NULL,
    severity_tier TEXT NOT NULL,
    affected_zone TEXT DEFAULT 'BILATERAL',
    radiologist_verified INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (study_id) REFERENCES imaging_studies (study_id),
    FOREIGN KEY (patient_id) REFERENCES patients (patient_id)
);

CREATE TABLE IF NOT EXISTS doctor_reviews (
    review_id TEXT PRIMARY KEY,
    finding_id TEXT NOT NULL,
    doctor_id TEXT NOT NULL,
    doctor_name TEXT NOT NULL,
    diagnosis_confirmed INTEGER DEFAULT 1,
    clinical_notes TEXT,
    review_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (finding_id) REFERENCES diagnostic_findings (finding_id)
);

CREATE INDEX IF NOT EXISTS idx_studies_patient ON imaging_studies(patient_id);
CREATE INDEX IF NOT EXISTS idx_findings_study ON diagnostic_findings(study_id);
CREATE INDEX IF NOT EXISTS idx_reviews_finding ON doctor_reviews(finding_id);
