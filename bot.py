#!/usr/bin/env python3
"""
Telegram Bot - Network Tools & Productivity Tools
Main bot file with command handlers and inline keyboards
"""

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters
)

from network_tools import (
    handle_ping,
    handle_traceroute,
    handle_ipinfo,
    handle_speedtest
)
from productivity_tools import (
    handle_reminder,
    handle_todo,
    handle_weather,
    handle_quote,
    handle_translate
)
from ai_handler import handle_ai_message

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def get_main_menu_keyboard():
    """Create the main menu inline keyboard"""
    keyboard = [
        [InlineKeyboardButton("🌐 Network Tools", callback_data="network_tools")],
        [InlineKeyboardButton("📋 Productivity Tools", callback_data="productivity_tools")],
    ]
    return InlineKeyboardMarkup(keyboard)


def get_network_tools_keyboard():
    """Create the Network Tools submenu keyboard"""
    keyboard = [
        [InlineKeyboardButton("📡 Ping", callback_data="cmd_ping")],
        [InlineKeyboardButton("🛤️ Traceroute", callback_data="cmd_traceroute")],
        [InlineKeyboardButton("📍 IP Info", callback_data="cmd_ipinfo")],
        [InlineKeyboardButton("⚡ Speedtest", callback_data="cmd_speedtest")],
        [InlineKeyboardButton("🔙 Back to Main Menu", callback_data="main_menu")],
    ]
    return InlineKeyboardMarkup(keyboard)


def get_productivity_tools_keyboard():
    """Create the Productivity Tools submenu keyboard"""
    keyboard = [
        [InlineKeyboardButton("⏰ Reminder", callback_data="cmd_reminder")],
        [InlineKeyboardButton("✅ Todo", callback_data="cmd_todo")],
        [InlineKeyboardButton("🌤️ Weather", callback_data="cmd_weather")],
        [InlineKeyboardButton("💬 Quote", callback_data="cmd_quote")],
        [InlineKeyboardButton("🌍 Translate", callback_data="cmd_translate")],
        [InlineKeyboardButton("🔙 Back to Main Menu", callback_data="main_menu")],
    ]
    return InlineKeyboardMarkup(keyboard)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /start is issued"""
    welcome_message = (
        "🤖 Welcome to the Network & Productivity Bot!\n\n"
        "Choose a category to get started:\n\n"
        "🌐 **Network Tools**: Ping, Traceroute, IP Info, Speedtest\n"
        "📋 **Productivity Tools**: Reminders, Todo, Weather, Quotes, Translation\n"
        "🤖 **AI Assistant**: Ask anything by starting your message with `@rbot`\n\n"
        "Use the buttons below or type /help for more information."
    )
    await update.message.reply_text(
        welcome_message,
        reply_markup=get_main_menu_keyboard(),
        parse_mode='Markdown'
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /help is issued"""
    help_text = (
        "📚 **Available Commands:**\n\n"
        "**Network Tools:**\n"
        "• `/ping <host>` - Ping an IP address or hostname\n"
        "• `/traceroute <host>` - Perform traceroute to a host\n"
        "• `/ipinfo <ip>` - Get IP geolocation and ASN info\n"
        "• `/speedtest` - Run internet speed test\n\n"
        "**Productivity Tools:**\n"
        "• `/reminder <time> <message>` - Set a reminder\n"
        "• `/todo <add|remove|list> [task]` - Manage todo list\n"
        "• `/weather <city>` - Get weather for a city\n"
        "• `/quote` - Get a motivational quote\n"
        "• `/translate <text> <target_lang>` - Translate text\n\n"
        "**AI Assistant:**\n"
        "• `@rbot <your question>` - Ask anything to the AI assistant\n"
        "  Example: `@rbot What is Python?`\n"
        "  Example: `@rbot Explain quantum computing`\n\n"
        "You can also use the inline buttons for easier navigation!"
    )
    await update.message.reply_text(
        help_text,
        reply_markup=get_main_menu_keyboard(),
        parse_mode='Markdown'
    )


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle button callbacks"""
    query = update.callback_query
    await query.answer()

    if query.data == "main_menu":
        await query.edit_message_text(
            "🤖 Choose a category:",
            reply_markup=get_main_menu_keyboard()
        )
    elif query.data == "network_tools":
        await query.edit_message_text(
            "🌐 **Network Tools**\n\nSelect a tool:",
            reply_markup=get_network_tools_keyboard(),
            parse_mode='Markdown'
        )
    elif query.data == "productivity_tools":
        await query.edit_message_text(
            "📋 **Productivity Tools**\n\nSelect a tool:",
            reply_markup=get_productivity_tools_keyboard(),
            parse_mode='Markdown'
        )
    elif query.data == "cmd_ping":
        await query.edit_message_text(
            "📡 **Ping Tool**\n\nSend me an IP address or hostname to ping.\n\n"
            "Example: `8.8.8.8` or `google.com`",
            parse_mode='Markdown'
        )
        context.user_data['waiting_for'] = 'ping'
    elif query.data == "cmd_traceroute":
        await query.edit_message_text(
            "🛤️ **Traceroute Tool**\n\nSend me an IP address or hostname for traceroute.\n\n"
            "Example: `8.8.8.8` or `google.com`",
            parse_mode='Markdown'
        )
        context.user_data['waiting_for'] = 'traceroute'
    elif query.data == "cmd_ipinfo":
        await query.edit_message_text(
            "📍 **IP Info Tool**\n\nSend me an IP address to get information.\n\n"
            "Example: `8.8.8.8`",
            parse_mode='Markdown'
        )
        context.user_data['waiting_for'] = 'ipinfo'
    elif query.data == "cmd_speedtest":
        await query.edit_message_text("⚡ Starting speedtest... This may take a moment.")
        await handle_speedtest(update, context)
    elif query.data == "cmd_reminder":
        await query.edit_message_text(
            "⏰ **Reminder Tool**\n\n"
            "Format: `<date/time> <message>`\n\n"
            "Example: `2024-12-25 10:00 Buy gifts`\n"
            "Or: `in 30 minutes Call mom`",
            parse_mode='Markdown'
        )
        context.user_data['waiting_for'] = 'reminder'
    elif query.data == "cmd_todo":
        await query.edit_message_text(
            "✅ **Todo Tool**\n\n"
            "Commands:\n"
            "• `/todo add <task>` - Add a task\n"
            "• `/todo remove <number>` - Remove a task\n"
            "• `/todo list` - List all tasks",
            parse_mode='Markdown'
        )
    elif query.data == "cmd_weather":
        await query.edit_message_text(
            "🌤️ **Weather Tool**\n\nSend me a city name to get weather information.\n\n"
            "Example: `London` or `New York`",
            parse_mode='Markdown'
        )
        context.user_data['waiting_for'] = 'weather'
    elif query.data == "cmd_quote":
        await query.edit_message_text("💬 Fetching a motivational quote...")
        await handle_quote(update, context)
    elif query.data == "cmd_translate":
        await query.edit_message_text(
            "🌍 **Translate Tool**\n\n"
            "Format: `<text> <target_language_code>`\n\n"
            "Example: `Hello world en` (translates to English)\n"
            "Example: `Bonjour fr` (translates to French)\n\n"
            "Common codes: en, es, fr, de, it, pt, ru, zh, ja",
            parse_mode='Markdown'
        )
        context.user_data['waiting_for'] = 'translate'


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle text messages based on what the user is waiting for"""
    # Check for AI messages first (messages starting with @rbot)
    if update.message and update.message.text:
        text = update.message.text.strip()
        if text.lower().startswith('@rbot'):
            await handle_ai_message(update, context)
            return
    
    waiting_for = context.user_data.get('waiting_for')
    text = update.message.text.strip()

    if waiting_for == 'ping':
        await handle_ping(update, context)
        context.user_data.pop('waiting_for', None)
    elif waiting_for == 'traceroute':
        await handle_traceroute(update, context)
        context.user_data.pop('waiting_for', None)
    elif waiting_for == 'ipinfo':
        await handle_ipinfo(update, context)
        context.user_data.pop('waiting_for', None)
    elif waiting_for == 'weather':
        await handle_weather(update, context)
        context.user_data.pop('waiting_for', None)
    elif waiting_for == 'reminder':
        await handle_reminder(update, context)
        context.user_data.pop('waiting_for', None)
    elif waiting_for == 'translate':
        await handle_translate(update, context)
        context.user_data.pop('waiting_for', None)
    else:
        await update.message.reply_text(
            "I'm not sure what you want to do. Use /start or /help to see available commands.",
            reply_markup=get_main_menu_keyboard()
        )


def main():
    """Start the bot"""
    # Optional: Start keep-alive server for Replit (if keep_alive.py exists)
    try:
        from keep_alive import keep_alive
        keep_alive()
        logger.info("Keep-alive server started")
    except ImportError:
        pass  # keep_alive.py not found, continue normally
    
    # Load configuration
    try:
        from config import BOT_TOKEN
    except ImportError:
        logger.error("config.py not found! Please create it with BOT_TOKEN.")
        return

    # Create application
    application = Application.builder().token(BOT_TOKEN).build()

    # Register command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    
    # Network Tools commands
    application.add_handler(CommandHandler("ping", handle_ping))
    application.add_handler(CommandHandler("traceroute", handle_traceroute))
    application.add_handler(CommandHandler("ipinfo", handle_ipinfo))
    application.add_handler(CommandHandler("speedtest", handle_speedtest))
    
    # Productivity Tools commands
    application.add_handler(CommandHandler("reminder", handle_reminder))
    application.add_handler(CommandHandler("todo", handle_todo))
    application.add_handler(CommandHandler("weather", handle_weather))
    application.add_handler(CommandHandler("quote", handle_quote))
    application.add_handler(CommandHandler("translate", handle_translate))
    
    # Button callback handler
    application.add_handler(CallbackQueryHandler(button_callback))
    
    # Message handler (for interactive commands)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start the bot
    logger.info("Bot is starting...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()

