@echo off
title Установка KeySound Overlay
echo ==============================================
echo Installing KeySound Overlay...
echo ==============================================
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0installer.ps1"
pause
