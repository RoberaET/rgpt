# Telegram Bot - Network Tools & Productivity Tools

A comprehensive Telegram bot built with Python that provides network diagnostic tools and productivity features.

## Features

### 🌐 Network Tools
- **Ping** - Ping an IP address or hostname
- **Traceroute** - Perform traceroute to a host
- **IP Info** - Get IP geolocation and ASN information
- **Speedtest** - Run internet speed test
- **Wake-on-LAN** - Wake up a PC remotely (authorized users only)

### 📋 Productivity Tools
- **Reminder** - Set reminders for specific dates/times
- **Todo** - Add, remove, and list tasks
- **Weather** - Get current weather for Addis Ababa, Ethiopia
- **Quote** - Fetch motivational quotes

### 🤖 AI Assistant
- **Gemini AI** - Ask any question by starting your message with `@rbot`

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Clone or Download
Download all the project files to your local machine.

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Configure API Keys

1. Copy the example config file:
   ```bash
   cp config.py.example config.py
   ```

2. Edit `config.py` and add your API keys:

   **Required:**
   - `BOT_TOKEN`: Get this from [@BotFather](https://t.me/BotFather) on Telegram
     1. Open Telegram and search for @BotFather
     2. Send `/newbot` command
     3. Follow the instructions to create your bot
     4. Copy the token provided

   **Optional (for specific features):**
   - `IPINFO_API_TOKEN`: For IP Info feature (recommended for better rate limits)
     - Get a free token at: https://ipinfo.io/
     - Sign up and get your API token from the dashboard
   
   - `WEATHERAPI_KEY`: For Weather feature
     - Get a free key at: https://www.weatherapi.com/
     - Sign up and get your API key from the dashboard
   
   - `GEMINI_API_KEY`: For AI Assistant feature
     - Get a free key at: https://makersuite.google.com/app/apikey
     - Sign up and get your API key from Google AI Studio

### Step 4: Run the Bot
```bash
python bot.py
```

## Usage

### Starting the Bot
1. Start a chat with your bot on Telegram
2. Send `/start` command
3. Use the inline buttons to navigate through categories

### Command Reference

#### Network Tools
- `/ping <host>` - Ping an IP or hostname
  - Example: `/ping 8.8.8.8` or `/ping google.com`

- `/traceroute <host>` - Perform traceroute
  - Example: `/traceroute 8.8.8.8`

- `/ipinfo <ip>` - Get IP information
  - Example: `/ipinfo 8.8.8.8`
  - Uses IPinfo Lite API (token recommended for better rate limits)

- `/speedtest` - Run speed test
  - No arguments needed

- `/wol <MAC>` or `/wake_pc <MAC>` - Wake up a PC remotely
  - Example: `/wol 00:11:22:33:44:55`
  - Example: `/wake_pc 00-11-22-33-44-55`
  - **Security:** Only authorized users (configured in config.py)
  - MAC formats: `00:11:22:33:44:55`, `00-11-22-33-44-55`, or `001122334455`

#### Productivity Tools
- `/reminder <time> <message>` - Set a reminder
  - Example: `/reminder 2024-12-25 10:00 Buy gifts`
  - Example: `/reminder in 30 minutes Call mom`

- `/todo add <task>` - Add a task
- `/todo remove <number>` - Remove a task
- `/todo list` - List all tasks

- `/weather` - Get weather for Addis Ababa, Ethiopia
  - No arguments needed
  - Requires: WeatherAPI.com API key

- `/quote` - Get a motivational quote
  - No arguments needed

#### AI Assistant
- `@rbot <your question>` - Ask anything to the AI assistant
  - Example: `@rbot What is Python?`
  - Example: `@rbot Explain quantum computing`
  - Requires: Gemini API key

## Project Structure

```
.
├── bot.py                 # Main bot file with handlers
├── network_tools.py       # Network tools module
├── productivity_tools.py  # Productivity tools module
├── ai_handler.py          # AI assistant module (Gemini)
├── config.py             # Configuration (create from config.py.example)
├── config.py.example     # Example configuration file
├── requirements.txt      # Python dependencies
├── README.md             # This file
└── todos.json            # Todo list storage (created automatically)
```

## API Keys Configuration

### Where to Insert API Keys

All API keys should be added to `config.py`:

1. **BOT_TOKEN** (Required)
   - Location: `config.py` → `BOT_TOKEN`
   - Get from: [@BotFather](https://t.me/BotFather) on Telegram

2. **IPINFO_API_TOKEN** (Optional - for IP Info, recommended)
   - Location: `config.py` → `IPINFO_API_TOKEN`
   - Get from: https://ipinfo.io/
   - Free tier available (50,000 requests/month)

3. **WEATHERAPI_KEY** (Optional - for Weather)
   - Location: `config.py` → `WEATHERAPI_KEY`
   - Get from: https://www.weatherapi.com/
   - Free tier available (1 million calls/month)

4. **GEMINI_API_KEY** (Optional - for AI Assistant)
   - Location: `config.py` → `GEMINI_API_KEY`
   - Get from: https://makersuite.google.com/app/apikey
   - Free tier available (generous free quota)

### Features That Don't Require API Keys

- Ping, Traceroute, Speedtest (use system commands)
- IP Info (uses free IPinfo Lite API - token recommended but not required)
- Quote (uses free quotable.io API)
- Reminder and Todo (local storage)

### Features That Require API Keys

- Weather (requires WeatherAPI.com key)
- AI Assistant (requires Gemini API key)

## Extending the Bot

The bot is designed to be modular. To add new commands:

1. **Add to network_tools.py or productivity_tools.py:**
   ```python
   async def handle_newcommand(update: Update, context: ContextTypes.DEFAULT_TYPE):
       # Your command logic here
       pass
   ```

2. **Import in bot.py:**
   ```python
   from network_tools import handle_newcommand
   ```

3. **Register the handler:**
   ```python
   application.add_handler(CommandHandler("newcommand", handle_newcommand))
   ```

4. **Add to inline keyboard** (if needed):
   - Update `get_network_tools_keyboard()` or `get_productivity_tools_keyboard()`
   - Add callback handler in `button_callback()`

## Troubleshooting

### Bot not responding
- Check that `BOT_TOKEN` is correct in `config.py`
- Ensure the bot is running (`python bot.py`)
- Check for error messages in the console

### Weather not working
- Verify `WEATHERAPI_KEY` is set in `config.py`
- Check your API key is valid at https://www.weatherapi.com/
- Ensure you haven't exceeded the free tier limit

### AI Assistant not working
- Verify `GEMINI_API_KEY` is set in `config.py`
- Check your API key is valid at https://makersuite.google.com/app/apikey
- Install the package: `pip install google-generativeai`
- Ensure you haven't exceeded the free tier quota

### Speedtest not working
- Install speedtest-cli: `pip install speedtest-cli`
- Some systems may require additional permissions

### Ping/Traceroute not working
- These commands require system-level access
- On Windows, ensure you have administrator privileges if needed
- On Linux/Mac, the commands should work by default

## License

This project is open source and available for personal and commercial use.

## Support

For issues or questions:
1. Check the troubleshooting section
2. Verify all API keys are correctly configured
3. Check the console for error messages

## Notes

- The reminder feature is a basic implementation. For production use, integrate with a proper task scheduler (e.g., APScheduler).
- Todos are stored locally in `todos.json` per user.
- Some commands may take time to execute (especially speedtest and traceroute).

