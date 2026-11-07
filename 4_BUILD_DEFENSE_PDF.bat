@echo off
title Project Sentinel - 4. Build 32-Page Bilingual Jury Defense PDF Manual
cd /d "%~dp0"
echo ==============================================================================
echo [PROJECT SENTINEL] Generating 32-Page Bilingual Jury Defense PDF Manual
echo Includes: 3 Personas, 14 Hardcore Q^&As, 4-Member Roles, 6 Crisis Protocols
echo Engine: Microsoft Edge Headless Vector PDF Renderer
echo ==============================================================================
python tools/build_bilingual_qa_manual.py
echo.
pause
