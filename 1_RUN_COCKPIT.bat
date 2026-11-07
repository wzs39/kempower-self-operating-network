@echo off
title Project Sentinel - 1. Launch Autonomous Command Cockpit
cd /d "%~dp0"
echo ==============================================================================
echo [PROJECT SENTINEL] Launching Autonomous Command Cockpit (Streamlit)
echo Track: Kempower Flagship Challenge - LahtiES Energy Tech Hackathon 2026
echo Interface: 4-View Cockpit (Executive / Scenario Player / Hardware / Commercial)
echo ==============================================================================
python -m streamlit run app.py --server.headless false
pause
