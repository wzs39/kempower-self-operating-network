@echo off
title Project Sentinel - 3. Run Demo Day Simulation Test Suite (28 Tests)
cd /d "%~dp0"
echo ==============================================================================
echo [PROJECT SENTINEL] Running Demo Day Simulation Tests (pytest 28 Tests)
echo Validates 10-Min Timeline, 4-Member Roles, 14 Hardcore Q^&As, and Crisis SOPs
echo ==============================================================================
pytest tests/test_demo_day_simulation.py -v
echo.
pause
