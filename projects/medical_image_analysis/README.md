# MedVision AI — Clinical Decision Support & Radiologist Console
### Built & Verified Autonomously by 7 LangGraph SDLC Multi-Agents

MedVision AI is a standalone medical image analysis platform designed for automated chest radiograph (CXR) screening, cardiomegaly CTR measurement, pneumonia consolidation detection, pulmonary nodule identification, and digital attending doctor review audit trails.

---

## 🚀 Quick Start

### 1. Launch the Executive Radiologist Dashboard
Double-click `run_dashboard.bat` or run:
```bash
"C:\Users\panka\.gemini\antigravity\scratch\ocr_multiagent_system\venv_ocr\Scripts\python.exe" -m streamlit run app.py --server.port 8506
```
Open **`http://localhost:8506`** in your browser.

### 2. Run Automated Pytest Suite
```bash
"C:\Users\panka\.gemini\antigravity\scratch\ocr_multiagent_system\venv_ocr\Scripts\python.exe" -m pytest -v tests/test_medical_analysis.py
```

### 3. Re-Run the Autonomous 7-Agent SDLC Pipeline
Double-click `run_sdlc.bat` or run:
```bash
"C:\Users\panka\.gemini\antigravity\scratch\ocr_multiagent_system\venv_ocr\Scripts\python.exe" run_sdlc.py
```

---

## 🏛️ System Topology

```
medical_image_analysis/
├── core/
│   ├── graph.py               # LangGraph 7-agent workflow & conditional edges
│   ├── llm.py                 # Resilient clinical LLM client & domain synthesizer
│   └── state.py               # Typed clinical SDLC state definition
├── agents/
│   ├── pm_agent.py            # Requirements analysis & Clinical SRS
│   ├── architect_agent.py     # System topology & HIPAA data model architecture
│   ├── planner_agent.py       # Agile sprint backlog planning & task breakdown
│   ├── developer_agent.py     # Medical code implementation
│   ├── reviewer_agent.py      # Security, safety & boundary audit
│   ├── qa_agent.py            # Automated Pytest suite verification
│   └── healer_agent.py        # Self-healing diagnostic & patch loop
├── database/
│   ├── schema.sql             # Relational DDL (patients, imaging_studies, findings, reviews)
│   └── db_manager.py          # SQLite connection and query helper
├── models/
│   └── study.py               # Typed dataclasses: Patient, ImagingStudy, Finding, DoctorReview
├── imaging/
│   └── image_processor.py     # Synthetic 512x512 radiograph synthesizer & contrast analysis
├── rules/
│   └── clinical_rules.py      # 5 clinical rules (Pneumonia, CTR, Nodule, Quality, Asymmetry)
├── services/
│   └── diagnostic_scorer.py   # Composite diagnostic scorer & triaging engine
├── data/
│   └── sample_scans/          # High-res synthetic CXR scans (normal, pneumonia, cardiomegaly, nodule)
├── tests/
│   └── test_medical_analysis.py # 100% passing Pytest suite
├── app.py                     # Streamlit Radiologist Executive Console
├── run_dashboard.bat          # 1-Click Dashboard launcher (Port 8506)
└── run_sdlc.bat               # 1-Click SDLC pipeline runner
```
