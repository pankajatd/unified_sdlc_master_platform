@echo off
cd /d "%~dp0"
echo Running AutoVision Automated Safety Tests (10 Test Suites)...
"C:\Users\panka\.gemini\antigravity\scratch\ocr_multiagent_system\venv_ocr\Scripts\python.exe" -m pytest tests/ -v
pause
