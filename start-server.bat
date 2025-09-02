@echo off
cd /d "C:\Users\35387\Desktop\dataSite\website"
echo Starting server from: %CD%
python -m http.server 8007
pause
