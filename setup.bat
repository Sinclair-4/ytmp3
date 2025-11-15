@echo off
echo ========================================
echo    Project Setup & Execution
echo ========================================

echo Step 1: Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python and ensure it's in your system PATH
    pause
    exit /b 1
)
python --version

echo Step 2: Creating virtual environment...
if exist "venv\" (
    echo Virtual environment already exists
) else (
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
        echo Please check your Python installation
        pause
        exit /b 1
    )
    echo Virtual environment created successfully
)

echo Step 3: Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)

echo Step 4: Upgrading pip...
pip install --upgrade pip >nul 2>&1
echo Pip upgraded to latest version

echo Step 5: Installing dependencies...
if exist "requirements.txt" (
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies from requirements.txt
        pause
        exit /b 1
    )
    echo Dependencies installed successfully
) else (
    echo WARNING: requirements.txt not found, skipping dependency installation
)

echo Step 6: Adding directory to PATH...
if exist "add_path.ps1" (
    powershell -ExecutionPolicy Bypass -File ".\add_path.ps1"
    if errorlevel 1 (
        echo WARNING: Could not add to PATH, but continuing...
    ) else (
        echo Directory added to PATH successfully
    )
) else (
    echo WARNING: add_path.ps1 not found, skipping PATH configuration
)

echo Step 7: Starting main program...
echo ========================================
python main.py
if errorlevel 1 (
    echo.
    echo ERROR: Program exited with error code %errorlevel%
    pause
    exit /b 1
)

echo.
echo ========================================
echo Program completed successfully!
echo.
echo Note: You may need to restart your terminal for PATH changes to take effect
pause