@echo off
TITLE Autonomous 7-Agent SDLC Multi-Project Master Platform
echo ===============================================================================
echo Starting Autonomous 7-Agent SDLC Master Platform...
echo Projects Integrated:
echo   1. Moving Car & Road Object Detection (AutoVision AI)
echo   2. Medical Image Analysis Platform (MedVision AI)
echo   3. Banking Fraud Detection System (FraudGuard AI)
echo ===============================================================================
echo.
cd /d "C:\Users\panka\.gemini\antigravity\scratch\unified_sdlc_master_platform"
"C:\Users\panka\.gemini\antigravity\scratch\ocr_multiagent_system\venv_ocr\Scripts\python.exe" -m streamlit run app.py --server.port 8508
pause
