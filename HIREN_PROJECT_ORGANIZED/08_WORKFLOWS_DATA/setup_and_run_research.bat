@echo off
echo ============================================================
echo   HIREN KUMAR - COMPETITIVE RESEARCH SETUP AND RUN
echo ============================================================
echo.

cd /d "c:\Users\Sachin Kumar\OneDrive\Desktop\HirenTask"

echo [1/3] Installing Python dependencies...
pip install ddgs requests beautifulsoup4 lxml pandas openpyxl Pillow fake-useragent python-slugify colorama tqdm --quiet
if %errorlevel% neq 0 (
    echo ERROR: pip install failed. Check your Python installation.
    pause
    exit /b 1
)
echo      Done.

echo.
echo [2/3] Creating output folders...
if not exist "ScrappedMaterial\01_LongIslandConvenience\images" mkdir "ScrappedMaterial\01_LongIslandConvenience\images"
if not exist "ScrappedMaterial\02_LongIslandBalloons\images" mkdir "ScrappedMaterial\02_LongIslandBalloons\images"
if not exist "ScrappedMaterial\03_LIGiftBasket\images" mkdir "ScrappedMaterial\03_LIGiftBasket\images"
if not exist "ScrappedMaterial\04_LongIslandPrintMail\images" mkdir "ScrappedMaterial\04_LongIslandPrintMail\images"
if not exist "ScrappedMaterial\05_LongIslandCards\images" mkdir "ScrappedMaterial\05_LongIslandCards\images"
if not exist "ScrappedMaterial\06_HirenKumar\images" mkdir "ScrappedMaterial\06_HirenKumar\images"
if not exist "ScrappedMaterial\07_ConsultCyber\images" mkdir "ScrappedMaterial\07_ConsultCyber\images"
echo      Done.

echo.
echo [3/3] Starting competitive research (ALL 7 WEBSITES)...
echo      This will take 20-40 minutes. Coffee time!
echo      Results go to:  ScrappedMaterial\
echo.
python competitive_research\main.py

echo.
echo ============================================================
echo   DONE! Open ScrappedMaterial\ to see your results.
echo ============================================================
pause
