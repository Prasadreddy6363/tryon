@echo off
echo ============================================
echo GitHub Repository Setup
echo ============================================
echo.

echo Step 1: Checking git status...
git status
echo.

echo Step 2: Adding new files...
git add .gitignore
git add README_GITHUB.md
git add GITHUB_SETUP_INSTRUCTIONS.md
git add push_to_github.bat
echo.

echo Step 3: Committing changes...
git commit -m "Prepare repository for GitHub - Add documentation and setup instructions"
echo.

echo ============================================
echo NEXT STEPS:
echo ============================================
echo.
echo 1. Go to https://github.com/new
echo 2. Create a new repository (don't initialize with README)
echo 3. Copy the repository URL
echo 4. Run ONE of these commands:
echo.
echo    For NEW repository:
echo    git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git
echo    git push -u origin main
echo.
echo    For EXISTING repository (replace remote):
echo    git remote set-url origin https://github.com/YOUR_USERNAME/REPO_NAME.git
echo    git push -u origin main
echo.
echo ============================================
echo.

pause
