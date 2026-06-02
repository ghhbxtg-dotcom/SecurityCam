@echo off
SETLOCAL

title SecurityCam

if not exist "venv" (

    echo Creating virtual environment...

    python -m venv venv

    call venv\Scripts\activate.bat

    echo Installing requirements...

    pip install -r requirements.txt

) else (

    call venv\Scripts\activate.bat
)

cls

python securitycam.py

pause
