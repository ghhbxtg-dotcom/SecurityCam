@echo off
SETLOCAL

REM 
if not exist "venv" (
    python -m venv venv
    echo Virtual environment created
)

REM 
call venv\Scripts\activate.bat

REM 
pip install --upgrade pip
pip install -r requirements.txt

REM 
securitycam.py

pause