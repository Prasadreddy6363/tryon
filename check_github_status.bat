@echo off
echo ============================================
echo Checking GitHub Push Status
echo ============================================
echo.

echo Checking local git status...
git status
echo.

echo ============================================
echo Checking if push completed...
echo ============================================
git log --oneline -1 origin/main 2>nul
if %ERRORLEVEL% EQU 0 (
    echo.
    echo ✓ Push appears to be complete!
    echo Visit: https://github.com/Prasadreddy6363/vton
) else (
    echo.
    echo ⏳ Push may still be in progress...
    echo The push is running in the background.
    echo.
    echo To manually push again, run:
    echo git push origin main
)

echo.
echo ============================================
pause
