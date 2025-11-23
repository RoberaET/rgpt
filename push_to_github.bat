@echo off
echo ========================================
echo   Push Telegram Bot to GitHub
echo ========================================
echo.

REM Check if git is installed
git --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Git is not installed!
    echo Please install Git from: https://git-scm.com/download/win
    echo.
    pause
    exit /b 1
)

echo [1/6] Initializing git repository...
git init
if errorlevel 1 (
    echo ERROR: Failed to initialize git
    pause
    exit /b 1
)

echo.
echo [2/6] Checking git configuration...
git config user.name >nul 2>&1
if errorlevel 1 (
    echo Git user name not configured.
    set /p GIT_NAME="Enter your name: "
    git config --global user.name "%GIT_NAME%"
)

git config user.email >nul 2>&1
if errorlevel 1 (
    echo Git email not configured.
    set /p GIT_EMAIL="Enter your email: "
    git config --global user.email "%GIT_EMAIL%"
)

echo.
echo [3/6] Adding files to git...
git add .
if errorlevel 1 (
    echo ERROR: Failed to add files
    pause
    exit /b 1
)

echo.
echo [4/6] Creating commit...
git commit -m "Initial commit: Telegram bot with network tools, productivity tools, and AI assistant"
if errorlevel 1 (
    echo ERROR: Failed to create commit
    echo You may need to configure git user.name and user.email first
    pause
    exit /b 1
)

echo.
echo [5/6] Checking for remote repository...
git remote get-url origin >nul 2>&1
if errorlevel 1 (
    echo.
    echo No remote repository configured.
    echo.
    echo Next steps:
    echo 1. Go to https://github.com/new
    echo 2. Create a new repository (don't initialize with README)
    echo 3. Copy the repository URL
    echo 4. Run this command:
    echo    git remote add origin YOUR_REPO_URL
    echo    git branch -M main
    echo    git push -u origin main
    echo.
    set /p REPO_URL="Or enter your GitHub repository URL now: "
    if not "%REPO_URL%"=="" (
        git remote add origin "%REPO_URL%"
        git branch -M main
        echo.
        echo [6/6] Pushing to GitHub...
        git push -u origin main
        if errorlevel 1 (
            echo.
            echo ERROR: Failed to push. You may need to authenticate.
            echo Use GitHub Personal Access Token: https://github.com/settings/tokens
        ) else (
            echo.
            echo SUCCESS! Your code has been pushed to GitHub!
        )
    )
) else (
    echo Remote repository found.
    echo.
    echo [6/6] Pushing to GitHub...
    git push -u origin main
    if errorlevel 1 (
        echo.
        echo ERROR: Failed to push. You may need to authenticate.
        echo Use GitHub Personal Access Token: https://github.com/settings/tokens
    ) else (
        echo.
        echo SUCCESS! Your code has been pushed to GitHub!
    )
)

echo.
echo ========================================
pause

