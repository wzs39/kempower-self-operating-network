@echo off
title Project Sentinel - 5. Verify 12-Slide Pitch Deck Structure & Zero-CJK
cd /d "%~dp0"
echo ==============================================================================
echo [PROJECT SENTINEL] Verifying 12-Slide Pitch Deck (python verify_pitch_deck.py)
echo Validates 16:9 Aspect Ratio, 12 Slides Strict, Speaker Notes, Zero CJK
echo ==============================================================================
python verify_pitch_deck.py
echo.
pause
