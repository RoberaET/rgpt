"""
Productivity Tools Module
Handles reminder, todo, weather, and quote commands
"""

import json
import os
import requests
import logging
from datetime import datetime, timedelta
from telegram import Update
from telegram.ext import ContextTypes

logger = logging.getLogger(__name__)

# File to store todos
TODO_FILE = "todos.json"


def load_todos():
    """Load todos from file"""
    if os.path.exists(TODO_FILE):
        try:
            with open(TODO_FILE, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}


def save_todos(todos):
    """Save todos to file"""
    with open(TODO_FILE, 'w') as f:
        json.dump(todos, f, indent=2)


async def handle_reminder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle reminder command"""
    try:
        if update.message:
            args = context.args if context.args else update.message.text.strip().split()
        else:
            args = context.args if context.args else []
        
        if not args or len(args) < 2:
            await update.message.reply_text(
                "❌ Please provide date/time and message.\n\n"
                "Usage: `/reminder <date/time> <message>`\n\n"
                "Examples:\n"
                "• `/reminder 2024-12-25 10:00 Buy gifts`\n"
                "• `/reminder in 30 minutes Call mom`\n"
                "• `/reminder tomorrow 15:00 Meeting`",
                parse_mode='Markdown'
            )
            return

        # Parse reminder time
        reminder_text = ' '.join(args)
        
        # Simple reminder storage (in production, use a proper scheduler)
        # For now, just acknowledge the reminder
        try:
            # Try to parse "in X minutes/hours"
            if reminder_text.lower().startswith('in '):
                parts = reminder_text.split()
                if len(parts) >= 4:
                    amount = int(parts[1])
                    unit = parts[2].lower()
                    message = ' '.join(parts[3:])
                    
                    if unit in ['minute', 'minutes', 'min', 'mins']:
                        reminder_time = datetime.now() + timedelta(minutes=amount)
                    elif unit in ['hour', 'hours', 'hr', 'hrs']:
                        reminder_time = datetime.now() + timedelta(hours=amount)
                    else:
                        raise ValueError("Unknown time unit")
                    
                    await update.message.reply_text(
                        f"✅ Reminder set!\n\n"
                        f"⏰ Time: {reminder_time.strftime('%Y-%m-%d %H:%M:%S')}\n"
                        f"📝 Message: {message}\n\n"
                        f"⚠️ Note: This is a basic implementation. "
                        f"For production use, integrate with a proper task scheduler.",
                        parse_mode='Markdown'
                    )
                    return
        except (ValueError, IndexError):
            pass
        
        # Try to parse date/time format
        try:
            # Format: YYYY-MM-DD HH:MM message
            date_str = f"{args[0]} {args[1]}"
            message = ' '.join(args[2:])
            reminder_time = datetime.strptime(date_str, "%Y-%m-%d %H:%M")
            
            await update.message.reply_text(
                f"✅ Reminder set!\n\n"
                f"⏰ Time: {reminder_time.strftime('%Y-%m-%d %H:%M:%S')}\n"
                f"📝 Message: {message}\n\n"
                f"⚠️ Note: This is a basic implementation. "
                f"For production use, integrate with a proper task scheduler.",
                parse_mode='Markdown'
            )
        except ValueError:
            await update.message.reply_text(
                "❌ Could not parse date/time format.\n\n"
                "Supported formats:\n"
                "• `YYYY-MM-DD HH:MM message`\n"
                "• `in X minutes/hours message`",
                parse_mode='Markdown'
            )
    except Exception as e:
        logger.error(f"Error in reminder: {e}")
        await update.message.reply_text(f"❌ Error: {str(e)}")


async def handle_todo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle todo command"""
    try:
        user_id = str(update.effective_user.id)
        todos = load_todos()
        
        if user_id not in todos:
            todos[user_id] = []
        
        user_todos = todos[user_id]
        
        if not context.args:
            await update.message.reply_text(
                "❌ Please specify an action.\n\n"
                "Usage:\n"
                "• `/todo add <task>` - Add a task\n"
                "• `/todo remove <number>` - Remove a task by number\n"
                "• `/todo list` - List all tasks",
                parse_mode='Markdown'
            )
            return
        
        action = context.args[0].lower()
        
        if action == 'add':
            if len(context.args) < 2:
                await update.message.reply_text("❌ Please provide a task to add.")
                return
            
            task = ' '.join(context.args[1:])
            user_todos.append(task)
            save_todos(todos)
            await update.message.reply_text(f"✅ Task added: {task}")
        
        elif action == 'remove':
            if len(context.args) < 2:
                await update.message.reply_text("❌ Please provide a task number to remove.")
                return
            
            try:
                index = int(context.args[1]) - 1
                if 0 <= index < len(user_todos):
                    removed = user_todos.pop(index)
                    save_todos(todos)
                    await update.message.reply_text(f"✅ Task removed: {removed}")
                else:
                    await update.message.reply_text("❌ Invalid task number.")
            except ValueError:
                await update.message.reply_text("❌ Please provide a valid task number.")
        
        elif action == 'list':
            if not user_todos:
                await update.message.reply_text("📋 Your todo list is empty!")
            else:
                todo_list = "📋 **Your Todo List:**\n\n"
                for i, task in enumerate(user_todos, 1):
                    todo_list += f"{i}. {task}\n"
                await update.message.reply_text(todo_list, parse_mode='Markdown')
        
        else:
            await update.message.reply_text(
                "❌ Unknown action. Use: `add`, `remove`, or `list`",
                parse_mode='Markdown'
            )
    except Exception as e:
        logger.error(f"Error in todo: {e}")
        await update.message.reply_text(f"❌ Error: {str(e)}")


async def handle_weather(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle weather command - Always returns weather for Ethiopia Addis Ababa"""
    try:
        message = update.message or update.callback_query.message
        await message.reply_text("🌤️ Fetching weather for Addis Ababa, Ethiopia...")

        try:
            from config import WEATHERAPI_KEY
            url = "https://api.weatherapi.com/v1/current.json"
            params = {
                'key': WEATHERAPI_KEY,
                'q': 'Addis Ababa, Ethiopia',
                'aqi': 'no'
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # Format weather information
            location = data.get('location', {})
            current = data.get('current', {})
            
            weather_text = f"🌤️ **Weather in {location.get('name', 'Addis Ababa')}, {location.get('country', 'Ethiopia')}**\n\n"
            weather_text += f"🌡️ **Temperature:** {current.get('temp_c', 'N/A')}°C ({current.get('temp_f', 'N/A')}°F)\n"
            weather_text += f"🌡️ **Feels like:** {current.get('feelslike_c', 'N/A')}°C ({current.get('feelslike_f', 'N/A')}°F)\n"
            weather_text += f"☁️ **Condition:** {current.get('condition', {}).get('text', 'N/A')}\n"
            weather_text += f"💨 **Wind:** {current.get('wind_kph', 'N/A')} km/h ({current.get('wind_mph', 'N/A')} mph)\n"
            weather_text += f"🧭 **Wind Direction:** {current.get('wind_dir', 'N/A')}\n"
            weather_text += f"💧 **Humidity:** {current.get('humidity', 'N/A')}%\n"
            weather_text += f"📊 **Pressure:** {current.get('pressure_mb', 'N/A')} mb\n"
            weather_text += f"👁️ **Visibility:** {current.get('vis_km', 'N/A')} km\n"
            weather_text += f"☀️ **UV Index:** {current.get('uv', 'N/A')}\n"
            weather_text += f"🌡️ **Dew Point:** {current.get('dewpoint_c', 'N/A')}°C\n"
            
            await message.reply_text(weather_text, parse_mode='Markdown')
        except ImportError:
            await message.reply_text(
                "❌ WeatherAPI key not configured.\n"
                "Please add WEATHERAPI_KEY to config.py\n"
                "Get a free key at: https://www.weatherapi.com/"
            )
        except requests.RequestException as e:
            logger.error(f"WeatherAPI error: {e}")
            await message.reply_text(f"❌ Error fetching weather: {str(e)}")
    except Exception as e:
        logger.error(f"Error in weather: {e}")
        message = update.message or update.callback_query.message
        await message.reply_text(f"❌ Error: {str(e)}")


async def handle_quote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle quote command using a free public API"""
    try:
        message = update.message or update.callback_query.message
        await message.reply_text("💬 Fetching a motivational quote...")

        # Using quotable.io (free, no API key required)
        try:
            response = requests.get("https://api.quotable.io/random", timeout=10)
            response.raise_for_status()
            data = response.json()
            
            quote_text = f"💬 **Quote of the Day**\n\n"
            quote_text += f"\"{data['content']}\"\n\n"
            quote_text += f"— {data['author']}"
            
            await message.reply_text(quote_text, parse_mode='Markdown')
        except requests.RequestException as e:
            logger.error(f"Quote API error: {e}")
            # Fallback quote
            await message.reply_text(
                "💬 **Quote of the Day**\n\n"
                "\"The only way to do great work is to love what you do.\"\n\n"
                "— Steve Jobs"
            )
    except Exception as e:
        logger.error(f"Error in quote: {e}")
        message = update.message or update.callback_query.message
        await message.reply_text(f"❌ Error: {str(e)}")

