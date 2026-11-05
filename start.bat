@echo off
echo ====================================================
echo Starting HarvestProof Server...
echo ====================================================
cd /d "%~dp0"
call .venv\Scripts\activate.bat
set HP_SECRET=harvestproof-secure-key-32-characters-long
python -m uvicorn api.main:app --port 8000 --reload
pause
