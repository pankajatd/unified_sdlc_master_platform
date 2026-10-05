@echo off
TITLE Launch Master Platform & Public Share Link
echo ===============================================================================
echo Starting Autonomous 7-Agent Master Platform (Port 8508)...
echo ===============================================================================

start "Master Platform - Local Server" cmd /k "cd /d C:\Users\panka\.gemini\antigravity\scratch\unified_sdlc_master_platform && C:\Users\panka\.gemini\antigravity\scratch\ocr_multiagent_system\venv_ocr\Scripts\python.exe -m streamlit run app.py --server.port 8508"

echo Waiting 5 seconds for local server to initialize...
timeout /t 5 /nobreak >nul

echo ===============================================================================
echo Starting Cloudflare Public Internet Tunnel...
echo Look for the link ending in: trycloudflare.com
echo Copy that link and send it to your testers!
echo (Keep this window open while testers are using it)
echo ===============================================================================
echo.

"C:\Program Files (x86)\cloudflared\cloudflared.exe" tunnel --url http://localhost:8508
pause
