@echo off
echo Installing Python dependencies for GradeMate Backend...
echo.

REM Activate virtual environment
call env\Scripts\activate.bat

REM Install dependencies
pip install -r requirements.txt

echo.
echo Installation complete!
echo.
echo To start the backend server, run:
echo python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
echo.
pause
