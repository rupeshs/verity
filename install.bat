
@echo off
setlocal
echo Starting Verity backend installation...

set "PYTHON_COMMAND=python"

call python --version > nul 2>&1
if %errorlevel% equ 0 (
    echo Python command check :OK
) else (
    echo "Error: Python command not found,please install Python and try again."
    pause
    exit /b 1
    
)

call uv --version > nul 2>&1
if %errorlevel% equ 0 (
    echo uv command check :OK
) else (
    echo "Error: uv command not found,please install https://docs.astral.sh/uv/getting-started/installation/#__tabbed_1_2 and try again."
    pause
    exit /b 1
    
)
:check_python_version
for /f "tokens=2" %%I in ('%PYTHON_COMMAND% --version 2^>^&1') do (
    set "python_version=%%I"
)

echo Python version: %python_version%

uv venv "%~dp0env" 
call "%~dp0env\Scripts\activate.bat" && uv pip install -r "%~dp0requirements.txt"
call "%~dp0env\Scripts\activate.bat" && python -m playwright install
echo Verity backend installation completed.

echo.
echo ===============================
echo Setting up Verity Frontend 
echo ===============================


cd /d "%~dp0src\frontend" || (
  echo Failed to change directory to src\frontend
  exit /b 1
)
call npm install

pause