@echo off
title MedVision AI - Clinical Radiology Console
cd /d "%~dp0"
echo ======================================================================
echo Starting MedVision AI Clinical Decision Support Console...
echo Dashboard URL: http://localhost:8506
echo ======================================================================
"C:\Users\panka\.gemini\antigravity\scratch\ocr_multiagent_system\venv_ocr\Scripts\python.exe" -m streamlit run app.py --server.port 8506
pause
