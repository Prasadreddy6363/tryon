@echo off
REM VITON-HD Dataset Download Helper for Windows
REM This script helps you download and set up the keypoints dataset

echo ========================================
echo VITON-HD Dataset Download Helper
echo ========================================
echo.

echo This script will help you download the VITON-HD dataset with keypoints.
echo.
echo What you'll get:
echo   - 2,032 person images
echo   - 2,032 clothing images  
echo   - OpenPose keypoints (JSON files)
echo   - Keypoint visualizations (PNG files)
echo   - Total size: ~2.5 GB
echo.

pause

echo.
echo ========================================
echo Step 1: Opening GitHub Repository
echo ========================================
echo.

REM Open the GitHub repository
start https://github.com/shadow2496/VITON-HD

echo Opened in your browser!
echo.
echo On the GitHub page:
echo   1. Scroll to "Dataset" section
echo   2. Click the Google Drive link for "test" dataset
echo   3. Download the ZIP file (~2.5 GB)
echo.

pause

echo.
echo ========================================
echo Step 2: Extract Location
echo ========================================
echo.

set "EXTRACT_PATH=%~dp0VITON-HD\datasets"
echo After downloading the ZIP file:
echo.
echo 1. Extract the ZIP file
echo 2. Move the "test" folder to:
echo    %EXTRACT_PATH%
echo.
echo Final structure should be:
echo    VITON-HD\datasets\test\image\
echo    VITON-HD\datasets\test\cloth\
echo    VITON-HD\datasets\test\openpose-json\      ^<-- Keypoints!
echo    VITON-HD\datasets\test\openpose-img\       ^<-- Keypoint images!
echo    VITON-HD\datasets\test\image-parse\
echo    VITON-HD\datasets\test\cloth-mask\
echo.

REM Create the directories if they don't exist
if not exist "%EXTRACT_PATH%" (
    echo Creating directories...
    mkdir "%EXTRACT_PATH%"
    echo Done!
)

echo.
echo Press any key when you've extracted the dataset...
pause

echo.
echo ========================================
echo Step 3: Verifying Dataset
echo ========================================
echo.

set "TEST_PATH=%EXTRACT_PATH%\test"

if exist "%TEST_PATH%" (
    echo [✓] Found test directory
    
    if exist "%TEST_PATH%\openpose-json" (
        echo [✓] Found openpose-json directory
        dir "%TEST_PATH%\openpose-json\*.json" /b 2>nul | find /c /v "" > temp.txt
        set /p JSON_COUNT=<temp.txt
        del temp.txt
        echo     Contains keypoint JSON files
    ) else (
        echo [✗] openpose-json directory NOT found!
    )
    
    if exist "%TEST_PATH%\openpose-img" (
        echo [✓] Found openpose-img directory
        echo     Contains keypoint visualization images
    ) else (
        echo [✗] openpose-img directory NOT found!
    )
    
    if exist "%TEST_PATH%\image" (
        echo [✓] Found image directory
    ) else (
        echo [✗] image directory NOT found!
    )
    
    if exist "%TEST_PATH%\cloth" (
        echo [✓] Found cloth directory
    ) else (
        echo [✗] cloth directory NOT found!
    )
    
    echo.
    echo ========================================
    echo Dataset Setup Complete!
    echo ========================================
    echo.
    echo You now have:
    echo   - Person images with pose keypoints
    echo   - Clothing images
    echo   - OpenPose JSON keypoint data
    echo   - Keypoint visualization images
    echo.
    echo Your VITON-HD system is ready to use!
    echo.
    
) else (
    echo [✗] Dataset not found!
    echo.
    echo Please make sure you:
    echo   1. Downloaded the ZIP file from Google Drive
    echo   2. Extracted it
    echo   3. Moved the "test" folder to: %EXTRACT_PATH%
    echo.
    echo Then run this script again.
)

echo.
pause
