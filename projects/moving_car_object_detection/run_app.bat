@echo off
cd /d "%~dp0"
echo Starting AutoVision AI Dashboard on port 8507...
"C:\Users\panka\.gemini\antigravity\scratch\ocr_multiagent_system\venv_ocr\Scripts\python.exe" -m streamlit run app.py --server.port 8507
