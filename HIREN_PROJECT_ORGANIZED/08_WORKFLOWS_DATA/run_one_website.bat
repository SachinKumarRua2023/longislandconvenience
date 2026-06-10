@echo off
echo ============================================================
echo   HIREN KUMAR - RUN RESEARCH FOR ONE WEBSITE
echo ============================================================
echo.
echo Available site keys:
echo   LongIslandConvenience
echo   LongIslandBalloons
echo   LIGiftBasket
echo   LongIslandPrintMail
echo   LongIslandCards
echo   HirenKumar
echo   ConsultCyber
echo.
set /p SITE_KEY="Enter site key (e.g. LIGiftBasket): "
echo.
echo Running research for: %SITE_KEY%
echo.
cd /d "c:\Users\Sachin Kumar\OneDrive\Desktop\HirenTask"
python competitive_research\main.py %SITE_KEY%
echo.
pause
