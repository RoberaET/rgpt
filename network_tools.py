"""
Network Tools Module
Handles ping, traceroute, IP info, and speedtest commands
"""

import subprocess
import requests
import logging
import platform
from telegram import Update
from telegram.ext import ContextTypes

logger = logging.getLogger(__name__)

# Detect OS for command compatibility
IS_WINDOWS = platform.system().lower() == 'windows'


async def handle_ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle ping command"""
    try:
        # Get host from command args or message text
        if update.message:
            host = ' '.join(context.args) if context.args else update.message.text.strip()
        else:
            host = ' '.join(context.args) if context.args else None
        
        if not host or host.startswith('/'):
            await update.message.reply_text(
                "❌ Please provide an IP address or hostname.\n"
                "Usage: `/ping <host>`\n"
                "Example: `/ping 8.8.8.8`",
                parse_mode='Markdown'
            )
            return

        message = update.message or update.callback_query.message
        await message.reply_text(f"📡 Pinging {host}...")

        # Run ping command (4 packets, timeout 5 seconds)
        try:
            if IS_WINDOWS:
                ping_cmd = ['ping', '-n', '4', '-w', '5000', host]
            else:
                ping_cmd = ['ping', '-c', '4', '-W', '5', host]
            
            result = subprocess.run(
                ping_cmd,
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                output = result.stdout
                # Extract summary if available
                lines = output.split('\n')
                summary = '\n'.join(lines[-5:]) if len(lines) > 5 else output
                await message.reply_text(f"✅ Ping Results:\n\n```\n{summary}\n```", parse_mode='Markdown')
            else:
                await message.reply_text(f"❌ Ping failed or host unreachable.\n\n```\n{result.stderr or result.stdout}\n```", parse_mode='Markdown')
        except subprocess.TimeoutExpired:
            await message.reply_text("⏱️ Ping timeout. The host may be unreachable.")
        except FileNotFoundError:
            await message.reply_text("❌ Ping command not available on this system.")
    except Exception as e:
        logger.error(f"Error in ping: {e}")
        message = update.message or update.callback_query.message
        await message.reply_text(f"❌ Error: {str(e)}")


async def handle_traceroute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle traceroute command"""
    try:
        # Get host from command args or message text
        if update.message:
            host = ' '.join(context.args) if context.args else update.message.text.strip()
        else:
            host = ' '.join(context.args) if context.args else None
        
        if not host or host.startswith('/'):
            message = update.message or update.callback_query.message
            await message.reply_text(
                "❌ Please provide an IP address or hostname.\n"
                "Usage: `/traceroute <host>`\n"
                "Example: `/traceroute 8.8.8.8`",
                parse_mode='Markdown'
            )
            return

        message = update.message or update.callback_query.message
        await message.reply_text(f"🛤️ Running traceroute to {host}... This may take a while.")

        # Run traceroute command
        try:
            if IS_WINDOWS:
                traceroute_cmd = ['tracert', '-h', '15', host]
            else:
                traceroute_cmd = ['traceroute', '-m', '15', host]
            
            result = subprocess.run(
                traceroute_cmd,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                output = result.stdout
                # Limit output length
                if len(output) > 3000:
                    output = output[:3000] + "\n... (truncated)"
                await message.reply_text(f"✅ Traceroute Results:\n\n```\n{output}\n```", parse_mode='Markdown')
            else:
                await message.reply_text(f"❌ Traceroute failed.\n\n```\n{result.stderr or result.stdout}\n```", parse_mode='Markdown')
        except subprocess.TimeoutExpired:
            await message.reply_text("⏱️ Traceroute timeout.")
        except FileNotFoundError:
            await message.reply_text("❌ Traceroute command not available on this system.")
    except Exception as e:
        logger.error(f"Error in traceroute: {e}")
        message = update.message or update.callback_query.message
        await message.reply_text(f"❌ Error: {str(e)}")


async def handle_ipinfo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle IP info command using IPinfo Lite API"""
    try:
        # Get IP from command args or message text
        if update.message:
            ip = ' '.join(context.args) if context.args else update.message.text.strip()
        else:
            ip = ' '.join(context.args) if context.args else None
        
        if not ip or ip.startswith('/'):
            message = update.message or update.callback_query.message
            await message.reply_text(
                "❌ Please provide an IP address.\n"
                "Usage: `/ipinfo <ip>`\n"
                "Example: `/ipinfo 8.8.8.8`",
                parse_mode='Markdown'
            )
            return

        message = update.message or update.callback_query.message
        await message.reply_text(f"📍 Fetching IP information for {ip}...")

        # IPinfo Lite API with token
        try:
            from config import IPINFO_API_TOKEN
            url = f"https://api.ipinfo.io/lite/{ip}"
            params = {'token': IPINFO_API_TOKEN}
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.text.strip().split('\n')
            
            # Parse lite API response (format: key:value per line)
            info_dict = {}
            for line in data:
                if ':' in line:
                    key, value = line.split(':', 1)
                    info_dict[key.strip()] = value.strip()
            
            # Format response
            info_text = f"📍 **IP Information for {ip}**\n\n"
            if info_dict.get('Country'):
                info_text += f"🌍 **Country:** {info_dict.get('Country', 'N/A')}\n"
            if info_dict.get('Region'):
                info_text += f"📍 **Region:** {info_dict.get('Region', 'N/A')}\n"
            if info_dict.get('City'):
                info_text += f"🏙️ **City:** {info_dict.get('City', 'N/A')}\n"
            if info_dict.get('Org'):
                info_text += f"🏢 **Organization:** {info_dict.get('Org', 'N/A')}\n"
            if info_dict.get('Postal'):
                info_text += f"📮 **Postal Code:** {info_dict.get('Postal', 'N/A')}\n"
            if info_dict.get('Timezone'):
                info_text += f"🌐 **Timezone:** {info_dict.get('Timezone', 'N/A')}\n"
            
            if not info_dict:
                # Fallback to JSON API if lite doesn't work
                url_json = f"https://ipinfo.io/{ip}/json"
                params_json = {'token': IPINFO_API_TOKEN}
                response_json = requests.get(url_json, params=params_json, timeout=10)
                response_json.raise_for_status()
                data_json = response_json.json()
                
                info_text = f"📍 **IP Information for {ip}**\n\n"
                info_text += f"🌍 **Location:** {data_json.get('city', 'N/A')}, {data_json.get('region', 'N/A')}, {data_json.get('country', 'N/A')}\n"
                info_text += f"📮 **Postal Code:** {data_json.get('postal', 'N/A')}\n"
                info_text += f"📍 **Coordinates:** {data_json.get('loc', 'N/A')}\n"
                info_text += f"🏢 **Organization:** {data_json.get('org', 'N/A')}\n"
                info_text += f"🌐 **Timezone:** {data_json.get('timezone', 'N/A')}\n"
            
            await message.reply_text(info_text, parse_mode='Markdown')
        except ImportError:
            await message.reply_text(
                "❌ IPinfo API token not configured.\n"
                "Please add IPINFO_API_TOKEN to config.py"
            )
        except requests.RequestException as e:
            logger.error(f"IPinfo API error: {e}")
            await message.reply_text(f"❌ Error fetching IP info: {str(e)}")
    except Exception as e:
        logger.error(f"Error in ipinfo: {e}")
        message = update.message or update.callback_query.message
        await message.reply_text(f"❌ Error: {str(e)}")


async def handle_speedtest(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle speedtest command using speedtest-cli"""
    try:
        message = update.message or update.callback_query.message
        await message.reply_text("⚡ Running speedtest... This may take 30-60 seconds.")

        # Run speedtest-cli
        try:
            result = subprocess.run(
                ['speedtest-cli', '--simple'],
                capture_output=True,
                text=True,
                timeout=120
            )
            
            if result.returncode == 0:
                output = result.stdout
                await message.reply_text(f"⚡ **Speedtest Results:**\n\n```\n{output}\n```", parse_mode='Markdown')
            else:
                # Try with --secure flag
                result = subprocess.run(
                    ['speedtest-cli', '--simple', '--secure'],
                    capture_output=True,
                    text=True,
                    timeout=120
                )
                if result.returncode == 0:
                    output = result.stdout
                    await message.reply_text(f"⚡ **Speedtest Results:**\n\n```\n{output}\n```", parse_mode='Markdown')
                else:
                    await message.reply_text(
                        f"❌ Speedtest failed.\n\n"
                        f"Make sure speedtest-cli is installed:\n"
                        f"`pip install speedtest-cli`\n\n"
                        f"Error: {result.stderr or result.stdout}",
                        parse_mode='Markdown'
                    )
        except subprocess.TimeoutExpired:
            await message.reply_text("⏱️ Speedtest timeout.")
        except FileNotFoundError:
            await message.reply_text(
                "❌ speedtest-cli not found.\n\n"
                "Install it with: `pip install speedtest-cli`",
                parse_mode='Markdown'
            )
    except Exception as e:
        logger.error(f"Error in speedtest: {e}")
        message = update.message or update.callback_query.message
        await message.reply_text(f"❌ Error: {str(e)}")

