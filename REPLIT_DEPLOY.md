# Deploying Telegram Bot on Replit

This guide will help you deploy your Telegram bot on Replit.

## Step 1: Create a New Replit Project

1. Go to [Replit](https://replit.com/) and sign in
2. Click **"Create Repl"** or **"+"** button
3. Select **"Python"** as the template
4. Name your project (e.g., "telegram-bot")
5. Click **"Create Repl"**

## Step 2: Upload Your Files

### Option A: Using Replit's File Upload
1. In Replit, click the **"Files"** icon in the sidebar
2. Click the **"..."** menu (three dots) next to Files
3. Select **"Upload file"** or drag and drop files
4. Upload all these files:
   - `bot.py`
   - `network_tools.py`
   - `productivity_tools.py`
   - `ai_handler.py`
   - `requirements.txt`
   - `config.py` (or create it manually - see Step 3)

### Option B: Using Git (Recommended)
1. Push your code to GitHub
2. In Replit, click **"Version control"** icon
3. Click **"Import from GitHub"**
4. Enter your repository URL
5. Click **"Import"**

## Step 3: Set Up Environment Variables (Secrets)

**IMPORTANT:** Never commit your `config.py` with real API keys to public repositories!

Instead, use Replit's **Secrets** feature:

1. In Replit, click the **"Secrets"** icon (lock icon) in the sidebar
2. Add the following secrets (click **"New secret"** for each):

   - **Key:** `BOT_TOKEN`
     **Value:** `8386724698:AAHxQNNRCtj16Z31UQpSZFTl9eSTkxHdxFY`

   - **Key:** `IPINFO_API_TOKEN`
     **Value:** `510b2e9c93b6ef`

   - **Key:** `WEATHERAPI_KEY`
     **Value:** `a006b3de5dd644ae993151839252311`

   - **Key:** `GEMINI_API_KEY`
     **Value:** `AIzaSyDuYAt2QJFc1MPx5dpwWqcpKvagkviCftc`

3. Click **"Add secret"** for each one

## Step 4: Create config.py for Replit

Create a `config.py` file that reads from environment variables:

```python
"""
Configuration file for the Telegram Bot (Replit version)
Reads from environment variables (Replit Secrets)
"""

import os

# Required: Telegram Bot Token
BOT_TOKEN = os.getenv("BOT_TOKEN", "")

# IPinfo Lite API Token (for IP Info)
IPINFO_API_TOKEN = os.getenv("IPINFO_API_TOKEN", "")

# WeatherAPI.com API Key (for Weather)
WEATHERAPI_KEY = os.getenv("WEATHERAPI_KEY", "")

# Google Gemini AI API Key (for AI Assistant)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
```

## Step 5: Configure .replit File

Replit should auto-detect Python, but you can create a `.replit` file to ensure proper configuration:

```toml
run = "python bot.py"
entrypoint = "bot.py"
language = "python3"

[nix]
channel = "stable-22_11"

[deploy]
run = ["sh", "-c", "python bot.py"]
```

## Step 6: Install Dependencies

1. In Replit, open the **Shell** (terminal) tab
2. Run:
   ```bash
   pip install -r requirements.txt
   ```

   Or install manually:
   ```bash
   pip install python-telegram-bot==20.7 requests==2.31.0 speedtest-cli==2.1.3 google-generativeai==0.3.2
   ```

## Step 7: Run the Bot

1. Click the **"Run"** button (green play button) at the top
2. The bot should start and you'll see: `Bot is starting...`
3. Check the console for any errors

## Step 8: Keep the Bot Running (Always On)

### For Free Replits:
- Replit free tier stops running after inactivity
- The bot will stop when you close the browser
- Consider upgrading to **Hacker** plan for always-on

### For Always-On (Hacker Plan):
1. Go to Replit settings
2. Enable **"Always On"** feature
3. Your bot will stay running 24/7

### Alternative: Use Uptime Robot (Free)
1. Get your Replit webview URL (if you add a simple web server)
2. Set up [Uptime Robot](https://uptimerobot.com/) to ping it every 5 minutes
3. This keeps your Repl "awake"

## Step 9: Add a Simple Web Server (Optional - for Uptime Robot)

To keep the bot alive with Uptime Robot, add a simple web server:

Create `keep_alive.py`:

```python
from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.daemon = True
    t.start()
```

Then modify `bot.py` to import it:

```python
# At the top of bot.py, add:
from keep_alive import keep_alive

# At the end of main(), before application.run_polling():
keep_alive()
```

## Troubleshooting

### Bot stops after inactivity
- This is normal for free Replit accounts
- Upgrade to Hacker plan or use Uptime Robot

### Import errors
- Make sure all dependencies are installed: `pip install -r requirements.txt`
- Check that all files are uploaded correctly

### API key errors
- Verify all secrets are set correctly in Replit Secrets
- Check that `config.py` reads from `os.getenv()`

### Speedtest not working
- Speedtest-cli may have limitations on Replit
- Consider removing speedtest or handling errors gracefully

### Port already in use
- If using keep_alive, change the port in `keep_alive.py`
- Or remove the web server if not needed

## Security Notes

1. **Never commit `config.py` with real API keys**
2. Always use Replit Secrets for sensitive data
3. Keep your Repl private if it contains sensitive code
4. Rotate API keys if they're accidentally exposed

## Monitoring

- Check Replit console for bot logs
- Monitor for errors in the output
- Set up error notifications if needed

## Next Steps

1. Test all bot commands
2. Monitor the bot for 24 hours
3. Set up Uptime Robot if using free tier
4. Consider upgrading to Hacker plan for production use

