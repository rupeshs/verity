@echo off
setlocal
echo Starting verity WebUI...
cd /d "%~dp0src\frontend"
call npm run dev
pause

