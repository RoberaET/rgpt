# Push to GitHub - Step by Step Guide

## Prerequisites

1. **Install Git** (if not already installed):
   - Download from: https://git-scm.com/download/win
   - Install with default settings
   - Restart your terminal/IDE after installation

2. **Create a GitHub Account** (if you don't have one):
   - Go to: https://github.com
   - Sign up for a free account

## Method 1: Using Git Commands (Recommended)

### Step 1: Open Terminal in Project Directory
Open PowerShell or Command Prompt in `D:\new project`

### Step 2: Initialize Git Repository
```bash
git init
```

### Step 3: Configure Git (if not already done)
```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### Step 4: Add All Files
```bash
git add .
```

### Step 5: Create Initial Commit
```bash
git commit -m "Initial commit: Telegram bot with network tools, productivity tools, and AI assistant"
```

### Step 6: Create GitHub Repository
1. Go to https://github.com/new
2. Repository name: `telegram-bot` (or any name you prefer)
3. Description: "Telegram bot with network tools, productivity tools, and AI assistant"
4. Choose **Public** or **Private**
5. **DO NOT** initialize with README, .gitignore, or license (we already have these)
6. Click **"Create repository"**

### Step 7: Add Remote and Push
GitHub will show you commands. Use these:

```bash
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git branch -M main
git push -u origin main
```

Replace `YOUR_USERNAME` and `YOUR_REPO_NAME` with your actual GitHub username and repository name.

### Step 8: Authenticate
- If prompted, use GitHub Personal Access Token (not password)
- Get token from: https://github.com/settings/tokens
- Create token with `repo` scope

## Method 2: Using GitHub Desktop (Easier)

1. **Download GitHub Desktop**: https://desktop.github.com/
2. **Install and sign in** with your GitHub account
3. **Add repository**:
   - File → Add Local Repository
   - Browse to `D:\new project`
   - Click "Add repository"
4. **Commit**:
   - Write commit message: "Initial commit: Telegram bot"
   - Click "Commit to main"
5. **Publish**:
   - Click "Publish repository"
   - Choose name and visibility
   - Click "Publish repository"

## Method 3: Using VS Code (If you use VS Code)

1. **Open project** in VS Code
2. **Open Source Control** (Ctrl+Shift+G)
3. **Initialize Repository** (if not already done)
4. **Stage all changes** (+ icon)
5. **Commit** with message
6. **Publish to GitHub** (click "Publish to GitHub" button)
7. **Follow prompts** to create repository

## Important Notes

### ✅ Files That Will Be Pushed:
- All Python files (`.py`)
- `README.md`
- `requirements.txt`
- `config.py.example` (safe template)
- `.gitignore`
- Documentation files (`.md`)
- `.replit` (if you want)

### ❌ Files That Will NOT Be Pushed (Protected by .gitignore):
- `config.py` (contains your real API keys - **NEVER commit this!**)
- `todos.json` (user data)
- `__pycache__/` (Python cache)
- IDE files

### Security Reminder:
- **NEVER** commit `config.py` with real API keys
- Always use `config.py.example` as template
- If you accidentally commit secrets, rotate them immediately!

## After Pushing

Your repository will be available at:
```
https://github.com/YOUR_USERNAME/YOUR_REPO_NAME
```

You can:
- Share the link with others
- Clone it on other machines
- Deploy from GitHub to Replit, Heroku, etc.

## Troubleshooting

### "git is not recognized"
- Install Git from https://git-scm.com/download/win
- Restart terminal after installation

### "Authentication failed"
- Use Personal Access Token instead of password
- Create token: https://github.com/settings/tokens

### "Repository not found"
- Check repository name and username
- Ensure repository exists on GitHub

### "Permission denied"
- Check you have write access to the repository
- Verify your GitHub credentials

