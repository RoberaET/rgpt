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

