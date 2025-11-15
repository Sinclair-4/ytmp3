@echo off
REM Save the current directory
set "ORIG_DIR=%CD%"

REM Switch to the directory of the batch file
cd /d "%~dp0"

REM Run Python using the venv interpreter directly
"%~dp0venv\Scripts\python.exe" main.py

REM Return to the original directory
cd /d "%ORIG_DIR%"

REM Pause so the user can see any output
pause
