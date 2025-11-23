# PowerShell script to push to GitHub

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Push Telegram Bot to GitHub" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if git is installed
try {
    $gitVersion = git --version
    Write-Host "[✓] Git is installed: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "[✗] ERROR: Git is not installed!" -ForegroundColor Red
    Write-Host "Please install Git from: https://git-scm.com/download/win" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "[1/6] Initializing git repository..." -ForegroundColor Yellow
git init
if ($LASTEXITCODE -ne 0) {
    Write-Host "[✗] ERROR: Failed to initialize git" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "[2/6] Checking git configuration..." -ForegroundColor Yellow
$gitName = git config user.name 2>$null
$gitEmail = git config user.email 2>$null

if (-not $gitName) {
    Write-Host "Git user name not configured." -ForegroundColor Yellow
    $gitName = Read-Host "Enter your name"
    git config --global user.name $gitName
}

if (-not $gitEmail) {
    Write-Host "Git email not configured." -ForegroundColor Yellow
    $gitEmail = Read-Host "Enter your email"
    git config --global user.email $gitEmail
}

Write-Host ""
Write-Host "[3/6] Adding files to git..." -ForegroundColor Yellow
git add .
if ($LASTEXITCODE -ne 0) {
    Write-Host "[✗] ERROR: Failed to add files" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "[4/6] Creating commit..." -ForegroundColor Yellow
git commit -m "Initial commit: Telegram bot with network tools, productivity tools, and AI assistant"
if ($LASTEXITCODE -ne 0) {
    Write-Host "[✗] ERROR: Failed to create commit" -ForegroundColor Red
    Write-Host "You may need to configure git user.name and user.email first" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "[5/6] Checking for remote repository..." -ForegroundColor Yellow
$remoteUrl = git remote get-url origin 2>$null

if (-not $remoteUrl) {
    Write-Host ""
    Write-Host "No remote repository configured." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Cyan
    Write-Host "1. Go to https://github.com/new"
    Write-Host "2. Create a new repository (don't initialize with README)"
    Write-Host "3. Copy the repository URL"
    Write-Host "4. Run these commands:" -ForegroundColor Yellow
    Write-Host "   git remote add origin YOUR_REPO_URL"
    Write-Host "   git branch -M main"
    Write-Host "   git push -u origin main"
    Write-Host ""
    $repoUrl = Read-Host "Or enter your GitHub repository URL now (or press Enter to skip)"
    
    if ($repoUrl) {
        git remote add origin $repoUrl
        git branch -M main
        Write-Host ""
        Write-Host "[6/6] Pushing to GitHub..." -ForegroundColor Yellow
        git push -u origin main
        if ($LASTEXITCODE -eq 0) {
            Write-Host ""
            Write-Host "[✓] SUCCESS! Your code has been pushed to GitHub!" -ForegroundColor Green
        } else {
            Write-Host ""
            Write-Host "[✗] ERROR: Failed to push. You may need to authenticate." -ForegroundColor Red
            Write-Host "Use GitHub Personal Access Token: https://github.com/settings/tokens" -ForegroundColor Yellow
        }
    }
} else {
    Write-Host "Remote repository found: $remoteUrl" -ForegroundColor Green
    Write-Host ""
    Write-Host "[6/6] Pushing to GitHub..." -ForegroundColor Yellow
    git push -u origin main
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "[✓] SUCCESS! Your code has been pushed to GitHub!" -ForegroundColor Green
    } else {
        Write-Host ""
        Write-Host "[✗] ERROR: Failed to push. You may need to authenticate." -ForegroundColor Red
        Write-Host "Use GitHub Personal Access Token: https://github.com/settings/tokens" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Read-Host "Press Enter to exit"

