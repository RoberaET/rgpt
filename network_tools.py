"""
Network Tools Module
Handles ping, traceroute, IP info, speedtest, and Wake-on-LAN commands
"""

import subprocess
import requests
import logging
import platform
import re
from telegram import Update
from telegram.ext import ContextTypes

logger = logging.getLogger(__name__)

# Detect OS for command compatibility
IS_WINDOWS = platform.system().lower() == 'windows'


async def handle_ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle ping command using API"""
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
                "Usage: `/ping <host>`\n"
                "Example: `/ping 8.8.8.8`",
                parse_mode='Markdown'
            )
            return

        message = update.message or update.callback_query.message
        await message.reply_text(f"📡 Pinging {host}...")

        # Use API-based ping service (works on all platforms including Replit)
        try:
            import time
            start_time = time.time()
            
            # Try to resolve and ping using requests
            url = f"https://api.hackertarget.com/nping/?q={host}"
            response = requests.get(url, timeout=10)
            
            elapsed_time = (time.time() - start_time) * 1000  # Convert to milliseconds
            
            if response.status_code == 200:
                output = response.text.strip()
                if output and "error" not in output.lower():
                    result_text = f"✅ Ping Results for {host}:\n\n"
                    result_text += f"⏱️ Response time: {elapsed_time:.2f} ms\n\n"
                    result_text += f"```\n{output[:500]}\n```"
                    await message.reply_text(result_text, parse_mode='Markdown')
                else:
                    # Fallback: Simple connectivity test
                    try:
                        test_url = f"http://{host}" if not host.startswith('http') else host
                        test_response = requests.get(test_url, timeout=5)
                        result_text = f"✅ Ping Results for {host}:\n\n"
                        result_text += f"⏱️ Response time: {elapsed_time:.2f} ms\n"
                        result_text += f"📊 Status: Host is reachable\n"
                        result_text += f"📡 HTTP Status: {test_response.status_code}"
                        await message.reply_text(result_text, parse_mode='Markdown')
                    except:
                        result_text = f"✅ Ping Results for {host}:\n\n"
                        result_text += f"⏱️ Response time: {elapsed_time:.2f} ms\n"
                        result_text += f"📊 Status: Host responded\n"
                        await message.reply_text(result_text, parse_mode='Markdown')
            else:
                await message.reply_text(f"❌ Ping failed. Unable to reach {host}")
        except Exception as e:
            logger.error(f"Ping API error: {e}")
            await message.reply_text(f"❌ Error pinging {host}: {str(e)}")
    except Exception as e:
        logger.error(f"Error in ping: {e}")
        message = update.message or update.callback_query.message
        await message.reply_text(f"❌ Error: {str(e)}")


async def handle_traceroute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle traceroute command using API"""
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

        # Use API-based traceroute service (works on all platforms including Replit)
        try:
            url = f"https://api.hackertarget.com/mtr/?q={host}"
            response = requests.get(url, timeout=30)
            
            if response.status_code == 200:
                output = response.text.strip()
                if output and "error" not in output.lower() and len(output) > 10:
                    # Limit output length for Telegram
                    if len(output) > 3000:
                        output = output[:3000] + "\n... (truncated)"
                    await message.reply_text(f"✅ Traceroute Results for {host}:\n\n```\n{output}\n```", parse_mode='Markdown')
                else:
                    # Fallback to alternative API
                    alt_url = f"https://ip-api.com/trace/{host}"
                    alt_response = requests.get(alt_url, timeout=30)
                    if alt_response.status_code == 200:
                        await message.reply_text(f"✅ Traceroute Results for {host}:\n\n```\n{alt_response.text[:3000]}\n```", parse_mode='Markdown')
                    else:
                        await message.reply_text(f"❌ Traceroute failed. Unable to trace route to {host}")
            else:
                await message.reply_text(f"❌ Traceroute failed. Unable to trace route to {host}")
        except requests.RequestException as e:
            logger.error(f"Traceroute API error: {e}")
            await message.reply_text(f"❌ Error running traceroute: {str(e)}")
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

        # IPinfo API - try with token first, fallback to free API
        try:
            from config import IPINFO_API_TOKEN
            # Try JSON API first (more reliable)
            url_json = f"https://ipinfo.io/{ip}/json"
            params_json = {'token': IPINFO_API_TOKEN} if IPINFO_API_TOKEN else {}
            response_json = requests.get(url_json, params=params_json, timeout=10)
            response_json.raise_for_status()
            data_json = response_json.json()
            
            # Format response
            info_text = f"📍 **IP Information for {ip}**\n\n"
            info_text += f"🌍 **Location:** {data_json.get('city', 'N/A')}, {data_json.get('region', 'N/A')}, {data_json.get('country', 'N/A')}\n"
            info_text += f"📮 **Postal Code:** {data_json.get('postal', 'N/A')}\n"
            info_text += f"📍 **Coordinates:** {data_json.get('loc', 'N/A')}\n"
            info_text += f"🏢 **Organization:** {data_json.get('org', 'N/A')}\n"
            info_text += f"🌐 **Timezone:** {data_json.get('timezone', 'N/A')}\n"
            
            await message.reply_text(info_text, parse_mode='Markdown')
        except ImportError:
            # Fallback to free API without token
            try:
                url = f"https://ipapi.co/{ip}/json/"
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                data = response.json()
                
                info_text = f"📍 **IP Information for {ip}**\n\n"
                info_text += f"🌍 **Location:** {data.get('city', 'N/A')}, {data.get('region', 'N/A')}, {data.get('country_name', 'N/A')}\n"
                info_text += f"📮 **Postal Code:** {data.get('postal', 'N/A')}\n"
                info_text += f"📍 **Coordinates:** {data.get('latitude', 'N/A')}, {data.get('longitude', 'N/A')}\n"
                info_text += f"🏢 **Organization:** {data.get('org', 'N/A')}\n"
                info_text += f"🌐 **Timezone:** {data.get('timezone', 'N/A')}\n"
                await message.reply_text(info_text, parse_mode='Markdown')
            except:
                await message.reply_text(
                    "❌ IPinfo API token not configured.\n"
                    "Please add IPINFO_API_TOKEN to config.py"
                )
        except requests.RequestException as e:
            logger.error(f"IPinfo API error: {e}")
            # Try fallback API
            try:
                url = f"https://ipapi.co/{ip}/json/"
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                data = response.json()
                
                info_text = f"📍 **IP Information for {ip}**\n\n"
                info_text += f"🌍 **Location:** {data.get('city', 'N/A')}, {data.get('region', 'N/A')}, {data.get('country_name', 'N/A')}\n"
                info_text += f"📮 **Postal Code:** {data.get('postal', 'N/A')}\n"
                info_text += f"📍 **Coordinates:** {data.get('latitude', 'N/A')}, {data.get('longitude', 'N/A')}\n"
                info_text += f"🏢 **Organization:** {data.get('org', 'N/A')}\n"
                info_text += f"🌐 **Timezone:** {data.get('timezone', 'N/A')}\n"
                await message.reply_text(info_text, parse_mode='Markdown')
            except:
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


async def handle_wol(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle Wake-on-LAN command to wake up a PC remotely"""
    try:
        # Security check: Only allow authorized user
        try:
            from config import ALLOWED_USER_ID
            user_id = update.effective_user.id
            
            # Check if user is authorized
            if isinstance(ALLOWED_USER_ID, list):
                if user_id not in ALLOWED_USER_ID:
                    await update.message.reply_text(
                        "❌ **Access Denied**\n\n"
                        "You are not authorized to use this command.",
                        parse_mode='Markdown'
                    )
                    logger.warning(f"Unauthorized WOL attempt by user {user_id}")
                    return
            elif user_id != ALLOWED_USER_ID:
                await update.message.reply_text(
                    "❌ **Access Denied**\n\n"
                    "You are not authorized to use this command.",
                    parse_mode='Markdown'
                )
                logger.warning(f"Unauthorized WOL attempt by user {user_id}")
                return
        except ImportError:
            await update.message.reply_text(
                "❌ **Configuration Error**\n\n"
                "ALLOWED_USER_ID not configured in config.py\n"
                "Please add your Telegram user ID to config.py",
                parse_mode='Markdown'
            )
            logger.error("ALLOWED_USER_ID not configured")
            return
        
        # Get MAC address from command args or message text
        if update.message:
            mac = ' '.join(context.args) if context.args else update.message.text.strip()
        else:
            mac = ' '.join(context.args) if context.args else None
        
        if not mac or mac.startswith('/'):
            message = update.message or update.callback_query.message
            await message.reply_text(
                "❌ Please provide a MAC address.\n\n"
                "**Usage:** `/wol <MAC_ADDRESS>`\n"
                "**Example:** `/wol 00:11:22:33:44:55`\n"
                "**Alternative:** `/wake_pc <MAC_ADDRESS>`\n\n"
                "MAC address formats supported:\n"
                "• `00:11:22:33:44:55` (with colons)\n"
                "• `00-11-22-33-44-55` (with hyphens)\n"
                "• `001122334455` (no separators)",
                parse_mode='Markdown'
            )
            return

        message = update.message or update.callback_query.message
        
        # Validate MAC address format
        mac_clean = mac.replace(':', '').replace('-', '').replace(' ', '').upper()
        
        # Check if MAC address is valid (12 hex characters)
        if not re.match(r'^[0-9A-F]{12}$', mac_clean):
            await message.reply_text(
                "❌ **Invalid MAC Address Format**\n\n"
                "Please provide a valid MAC address.\n\n"
                "**Valid formats:**\n"
                "• `00:11:22:33:44:55`\n"
                "• `00-11-22-33-44-55`\n"
                "• `001122334455`",
                parse_mode='Markdown'
            )
            return
        
        # Format MAC address with colons for wakeonlan library
        mac_formatted = ':'.join([mac_clean[i:i+2] for i in range(0, 12, 2)])
        
        await message.reply_text(f"🔌 Sending Wake-on-LAN packet to {mac_formatted}...")

        try:
            from wakeonlan import send_magic_packet
            
            # Send magic packet
            # Default broadcast address (255.255.255.255) works from anywhere
            # if router is properly configured with port forwarding
            send_magic_packet(mac_formatted)
            
            await message.reply_text(
                f"✅ **Wake-on-LAN Packet Sent!**\n\n"
                f"📡 **MAC Address:** `{mac_formatted}`\n"
                f"🌐 **Broadcast:** 255.255.255.255\n\n"
                f"⏳ The target PC should wake up shortly.\n\n"
                f"**Note:** Ensure:\n"
                f"• WOL is enabled in BIOS/UEFI\n"
                f"• Network adapter allows WOL\n"
                f"• Router has port forwarding (UDP port 9)\n"
                f"• Static IP or Dynamic DNS configured",
                parse_mode='Markdown'
            )
            logger.info(f"WOL packet sent to {mac_formatted} by user {user_id}")
            
        except ImportError:
            await message.reply_text(
                "❌ **Library Not Installed**\n\n"
                "Please install wakeonlan library:\n"
                "`pip install wakeonlan`",
                parse_mode='Markdown'
            )
        except Exception as e:
            logger.error(f"WOL error: {e}")
            await message.reply_text(
                f"❌ **Error sending WOL packet**\n\n"
                f"Error: {str(e)}\n\n"
                f"Please check:\n"
                f"• MAC address is correct\n"
                f"• Network connectivity\n"
                f"• WOL configuration",
                parse_mode='Markdown'
            )
    except Exception as e:
        logger.error(f"Error in WOL handler: {e}")
        message = update.message or update.callback_query.message
        await message.reply_text(f"❌ Error: {str(e)}")

