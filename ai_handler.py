"""
AI Handler Module
Handles Gemini AI integration for general-purpose AI conversations
"""

import logging
from telegram import Update
from telegram.ext import ContextTypes

logger = logging.getLogger(__name__)


async def handle_ai_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle AI messages starting with @rbot"""
    try:
        if not update.message or not update.message.text:
            return
        
        message_text = update.message.text.strip()
        
        # Check if message starts with @rbot
        if not message_text.lower().startswith('@rbot'):
            return
        
        # Extract the query (remove @rbot prefix)
        query = message_text[6:].strip()  # Remove '@rbot' (6 characters)
        
        if not query:
            await update.message.reply_text(
                "🤖 **AI Assistant**\n\n"
                "Send me a message starting with `@rbot` followed by your question.\n\n"
                "Example: `@rbot What is Python?`\n"
                "Example: `@rbot Explain quantum computing`",
                parse_mode='Markdown'
            )
            return
        
        # Show typing indicator
        await update.message.chat.send_action(action="typing")
        
        try:
            import google.generativeai as genai
            from config import GEMINI_API_KEY
            
            # Configure Gemini
            genai.configure(api_key=GEMINI_API_KEY)
            
            # Create model instance
            model = genai.GenerativeModel('gemini-pro')
            
            # Generate response
            response = model.generate_content(query)
            
            # Get the text response
            ai_response = response.text
            
            # Limit response length (Telegram has a 4096 character limit per message)
            if len(ai_response) > 4000:
                ai_response = ai_response[:4000] + "\n\n... (response truncated)"
            
            await update.message.reply_text(
                f"🤖 **AI Response:**\n\n{ai_response}",
                parse_mode='Markdown'
            )
            
        except ImportError:
            await update.message.reply_text(
                "❌ Gemini AI not configured.\n"
                "Please add GEMINI_API_KEY to config.py\n"
                "Install: `pip install google-generativeai`"
            )
        except Exception as e:
            logger.error(f"Gemini AI error: {e}")
            await update.message.reply_text(
                f"❌ Error getting AI response: {str(e)}\n\n"
                "Please try again later."
            )
            
    except Exception as e:
        logger.error(f"Error in AI handler: {e}")
        if update.message:
            await update.message.reply_text(f"❌ Error: {str(e)}")

