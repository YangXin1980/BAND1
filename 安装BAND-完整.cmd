@echo off
setlocal
set "PACKAGE_DIR=%~dp0"
set "PS=%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe"
if exist "%SystemRoot%\Sysnative\WindowsPowerShell\v1.0\powershell.exe" set "PS=%SystemRoot%\Sysnative\WindowsPowerShell\v1.0\powershell.exe"
if not exist "%PS%" set "PS=powershell.exe"
if not exist "%PACKAGE_DIR%app\Install-App.ps1" (
  echo Cannot find app\Install-App.ps1. Please extract the whole BAND package first.
  pause
  exit /b 1
)
"%PS%" -NoProfile -ExecutionPolicy Bypass -File "%PACKAGE_DIR%app\Install-App.ps1"
if errorlevel 1 pause
