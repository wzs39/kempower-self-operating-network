@echo off
title Project Sentinel - 2. Run Deterministic Verifier (29 Checks)
cd /d "%~dp0"
echo ==============================================================================
echo [PROJECT SENTINEL] Running Deterministic Verifier (python verify_all.py)
echo Validates 29 Core Physical, Invariant, and Commercial Assertions in ^< 0.5s
echo ==============================================================================
python verify_all.py
echo.
pause
