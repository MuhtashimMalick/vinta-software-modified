@echo off
REM Activate the virtual environment
call "%~dp0\.venv\Scripts\activate.bat"

REM Navigate to the project root (optional)
cd "%~dp0"

REM Run the FastAPI app with uvicorn
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

pause