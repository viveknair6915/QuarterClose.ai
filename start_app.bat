@echo off
echo Starting QuarterClose.ai Platform...

echo Starting Backend (FastAPI)...
start "Backend API" uvicorn backend.app.main:app --host 0.0.0.0 --port 8000

echo Waiting for Backend to initialize...
timeout /t 5

echo Starting Frontend (Streamlit)...
start "Frontend UI" streamlit run frontend/Home.py --server.port 8501

echo Application Launched!
echo Frontend: http://localhost:8501
echo Backend: http://localhost:8000/docs
pause
