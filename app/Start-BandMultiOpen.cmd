@echo off
setlocal
set APP_DIR=%~dp0
set INSTALLED_APP=%LOCALAPPDATA%\Programs\BAND\BAND.exe
if exist "%INSTALLED_APP%" (
  start "" "%INSTALLED_APP%"
  exit /b 0
)
if not exist "%APP_DIR%BAND.exe" (
  echo Cannot find BAND.exe. Please extract the whole BAND package first.
  pause
  exit /b 1
)
start "" "%APP_DIR%BAND.exe"
