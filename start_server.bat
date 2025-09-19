@echo off
echo Starting GradeMate Backend Server...
echo.

REM Activate virtual environment
call env\Scripts\activate.bat

REM Start the server
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
