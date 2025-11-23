# Quick Replit Setup Guide

## Fast Setup Steps

### 1. Upload Files to Replit
Upload these files to your Replit project:
- `bot.py`
- `network_tools.py`
- `productivity_tools.py`
- `ai_handler.py`
- `requirements.txt`
- `.replit` (optional, but recommended)

### 2. Create config.py in Replit
Create a new file called `config.py` with this content:

```python
import os

BOT_TOKEN = os.getenv("BOT_TOKEN", "")
IPINFO_API_TOKEN = os.getenv("IPINFO_API_TOKEN", "")
WEATHERAPI_KEY = os.getenv("WEATHERAPI_KEY", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
```

### 3. Set Secrets in Replit
1. Click the **Secrets** icon (lock) in sidebar
2. Add these secrets:

```
BOT_TOKEN = 8386724698:AAHxQNNRCtj16Z31UQpSZFTl9eSTkxHdxFY
IPINFO_API_TOKEN = 510b2e9c93b6ef
WEATHERAPI_KEY = a006b3de5dd644ae993151839252311
GEMINI_API_KEY = AIzaSyDuYAt2QJFc1MPx5dpwWqcpKvagkviCftc
```

### 4. Install Dependencies
In Replit Shell, run:
```bash
pip install -r requirements.txt
```

### 5. Run the Bot
Click the **Run** button (green play button)

### 6. Keep It Running (Optional)
For free Replit accounts, the bot stops after inactivity. To keep it running:

**Option A: Upgrade to Hacker Plan** (Always On)

**Option B: Use Uptime Robot** (Free)
1. Add Flask to requirements.txt: `flask==3.0.0`
2. At the top of `bot.py`, add:
   ```python
   try:
       from keep_alive import keep_alive
       keep_alive()
   except:
       pass
   ```
3. Upload `keep_alive.py` to Replit
4. Get your Replit webview URL
5. Set up [Uptime Robot](https://uptimerobot.com/) to ping it every 5 minutes

## That's It!
Your bot should now be running on Replit!

