@echo off

REM Clone repo (fails if folder exists)
git clone https://github.com/Sinclair-4/ytmp3.git

REM Move inside project folder
cd ytmp3

REM Create virtual environment
python -m venv venv

REM Activate venv
call venv\Scripts\activate.bat

REM Install dependencies
pip install -r requirements.txt

REM Run main program
python main.py

pause
