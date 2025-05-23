import asyncio
import aiohttp
from typing import Dict, List
from datetime import datetime
from pyrogram.errors import FloodWait
import os
import re
import subprocess
import helper  # Ensure this module is available
from pyrogram.errors.exceptions.bad_request_400 import StickerEmojiInvalid
import requests
import json
from pyrogram import Client, filters
from pyrogram.types import Message
from p_bar import progress_bar
from subprocess import getstatusoutput
from aiohttp import ClientSession
import logging as std_logging
import time
import sys
import tempfile
from urllib.parse import urlparse, parse_qs
from bs4 import BeautifulSoup
import pyrogram

# Configure logging
print(f"Logging module: {std_logging.__file__}")
print(f"Pyrogram version: {pyrogram.__version__}")

try:
    logger = std_logging.getLogger('PenPencilBot')
    if not logger.handlers:
        logger.setLevel(std_logging.DEBUG)
        console_handler = std_logging.StreamHandler()
        console_handler.setFormatter(std_logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        logger.addHandler(console_handler)
        file_handler = std_logging.FileHandler('bot.log')
        file_handler.setFormatter(std_logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        logger.addHandler(file_handler)
except Exception as e:
    print(f"Failed to configure logging: {e}")
    class FallbackLogger:
        @staticmethod
        def info(msg): print(f"INFO: {msg}")
        @staticmethod
        def warning(msg): print(f"WARNING: {msg}")
        @staticmethod
        def error(msg): print(f"ERROR: {msg}")
        @staticmethod
        def debug(msg): print(f"DEBUG: {msg}")
    logger = FallbackLogger()

# PenPencil API credentials
ACCESS_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE3NDYzMzkwMzkuMDQ0LCJkYXRhIjp7Il9pZCI6IjY0YjY0NDhkNjAxYWM2MDAxOGQ5ODE1MyIsInVzZXJuYW1lIjoiOTM1MjYzMTczMSIsImZpcnN0TmFtZSI6Ik5hbWFuIiwibGFzdE5hbWUiOiIiLCJvcmdhbml6YXRpb24iOnsiX2lkIjoiNWViMzkzZWU5NWZhYjc0NjhhNzlkMTg5Iiwid2Vic2l0ZSI6InBoeXNpY3N3YWxsYWguY29tIiwibmFtZSI6IlBoeXNpY3N3YWxsYWgifSwiZW1haWwiOiJvcG1hc3Rlcjk4NTRAZ21haWwuY29tIiwicm9sZXMiOlsiNWIyN2JkOTY1ODQyZjk1MGE3NzhjNmVmIl0sImNvdW50cnlHcm91cCI6IklOIiwidHlwZSI6IlVTRVIifSwiaWF0IjoxNzQ1NzM0MjM5fQ.GNUr2USwCUeV7Y8gWsyIp3yuGnaSdrg7bbjkCBSdguI"
BATCH_ID = "67738e4a5787b05d8ec6e07f"

# PenPencil API headers
HEADERS = {
    'Host': 'api.penpencil.co',
    'client-id': '5eb393ee95fab7468a79d189',
    'client-version': '1910',
    'user-agent': 'Mozilla/5.0 (Linux; Android 12; M2101K6P) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36',
    'randomid': '72012511-256c-4e1c-b4c7-29d67136af37',
    'client-type': 'WEB',
    'content-type': 'application/json; charset=utf-8',
    'authorization': f"Bearer {ACCESS_TOKEN}",
}

# Telegram bot setup
bot = Client(
    "bot",
    bot_token=os.environ.get("BOT_TOKEN", "7251113580:AAFOIpTAGHALclWZBexgNbevU_z6qyZuGnU"),
    api_id=int(os.environ.get("API_ID", "23713783")),
    api_hash=os.environ.get("API_HASH", "2daa157943cb2d76d149c4de0b036a99")
)

# Destination chat ID for sending content
DESTINATION_CHAT_ID = "5487643307"  # Replace with your chat ID

async def fetch_pwwp_data(session: aiohttp.ClientSession, url: str, headers: Dict):
    async with session.get(url, headers=headers) as response:
        if response.status == 200:
            return await response.json()
        else:
            logger.warning(f"Failed to fetch data from {url}")
            return None

async def get_pwwp_todays_schedule_content_details(session: aiohttp.ClientSession, selected_batch_id, subject_id, schedule_id, headers: Dict) -> List[str]:
    url = f"https://api.penpencil.co/v1/batches/{selected_batch_id}/subject/{subject_id}/schedule/{schedule_id}/schedule-details"
    data = await fetch_pwwp_data(session, url, headers)
    content = []

    if data and data.get("success") and data.get("data"):
        data_item = data["data"]
        
        video_details = data_item.get('videoDetails', {})
        if video_details:
            name = data_item.get('topic')
            videoUrl = video_details.get('videoUrl') or video_details.get('embedCode')
            if videoUrl and ("/master.mpd" in videoUrl or ".pdf" in videoUrl):
                line = f"{name}: {videoUrl}"
                content.append(line)
               
        homework_ids = data_item.get('homeworkIds', [])
        for homework in homework_ids:
            attachment_ids = homework.get('attachmentIds', [])
            name = homework.get('topic')
            for attachment in attachment_ids:
                url = attachment.get('baseUrl', '') + attachment.get('key', '')
                if url and ("/master.mpd" in url or ".pdf" in url):
                    line = f"{name}: {url}"
                    content.append(line)
                
        dpp = data_item.get('dpp')
        if dpp:
            dpp_homework_ids = dpp.get('homeworkIds', [])
            for homework in dpp_homework_ids:
                attachment_ids = homework.get('attachmentIds', [])
                name = homework.get('topic')
                for attachment in attachment_ids:
                    url = attachment.get('baseUrl', '') + attachment.get('key', '')
                    if url and ("/master.mpd" in url or ".pdf" in url):
                        line = f"{name}: {url}"
                        content.append(line)
    else:
        logger.warning(f"No Data Found For Schedule ID - {schedule_id}")
    return content

async def get_pwwp_all_todays_schedule_content(session: aiohttp.ClientSession, selected_batch_id: str, headers: Dict) -> List[str]:
    url = f"https://api.penpencil.co/v1/batches/{selected_batch_id}/todays-schedule"
    todays_schedule_details = await fetch_pwwp_data(session, url, headers)
    all_content = []

    if todays_schedule_details and todays_schedule_details.get("success") and todays_schedule_details.get("data"):
        tasks = []
        for item in todays_schedule_details['data']:
            schedule_id = item.get('_id')
            subject_id = item.get('batchSubjectId')
            task = asyncio.create_task(get_pwwp_todays_schedule_content_details(session, selected_batch_id, subject_id, schedule_id, headers))
            tasks.append(task)
        results = await asyncio.gather(*tasks)
        for result in results:
            all_content.extend(result)
    else:
        logger.warning("No today's schedule data found.")
    return all_content

async def process_and_send_content(content: str, bot: Client, chat_id: str):
    try:
        name, url = content.split(":", 1)
        name = name.strip()
        url = url.strip()

        name1 = name.replace("\t", "").replace(":", "").replace("/", "").replace("+", "").replace("#", "").replace("|", "").replace("@", "@").replace("*", "").replace("https", "").replace("http", "").strip()
        name = f'{name1[:60]}'

        cc = f'**{name1}.mkv**\n\n**𝗕𝗮𝘁𝗰𝗵 - OP**'
        cc1 = f'**{name1}.pdf**\n\n**𝗕𝗮𝘁𝗰𝗵 - OP**'

        ytf = f"b[height<=720]/bv[height<=720]+ba/b/bv+ba"

        if '/master.mpd' in url:
            id = url.split("/")[-2]
            url = f"https://as-multiverse-b0b2769da88f.herokuapp.com/{id}/master.m3u8?token={ACCESS_TOKEN}"

        thumb = "no"

        if ".pdf" in url:
            try:
                cmd = f'yt-dlp -o "{name}.pdf" "{url}"'
                download_cmd = f"{cmd} -R 25 --fragment-retries 25"
                subprocess.run(download_cmd, shell=True, check=True)
                await bot.send_document(
                    chat_id=chat_id,
                    document=f'{name}.pdf',
                    caption=cc1
                )
                os.remove(f'{name}.pdf')
            except Exception as e:
                logger.error(f"Error downloading PDF {url}: {e}")
                await bot.send_message(chat_id, f"Failed to download PDF: {url}")
        elif "/master.m3u8" in url:
            try:
                Show = f"**⥥ 📥 ＤＯＷＮＬＯＡＤＩＮＧ 📥 :-**\n\n**📝Name »** `{name}`\n**❄𝐐𝐮𝐚𝐥𝐢𝐭𝐲 » 720p**\n\n**Bot made by MR (Daddy)🧑🏻‍💻**"
                prog = await bot.send_message(chat_id, Show)
                res_file = await helper.download_video(url, f'yt-dlp -f "{ytf}" -o "{name}.%(ext)s" "{url}"', name)
                filename = res_file
                await prog.delete(True)
                await helper.send_vid(bot, None, cc, filename, thumb, name, prog)
            except Exception as e:
                logger.error(f"Error processing video {url}: {e}")
                await bot.send_message(chat_id, f"Failed to process video: {url}\n\n**{cc}**")
    except Exception as e:
        logger.error(f"Error processing content {content}: {e}")
        await bot.send_message(chat_id, f"Error processing content: {content}")

async def monitor_todays_schedule(bot: Client, chat_id: str):
    seen_items = set()
    async with aiohttp.ClientSession() as session:
        while True:
            try:
                all_content = await get_pwwp_all_todays_schedule_content(session, BATCH_ID, HEADERS)
                new_items = [item for item in all_content if item not in seen_items]

                if new_items:
                    current_time = datetime.now().strftime("%H:%M:%S")
                    await bot.send_message(chat_id, f"**New Content Found at {current_time}:**")
                    for item in new_items:
                        await process_and_send_content(item, bot, chat_id)
                    seen_items.update(new_items)
                else:
                    logger.debug(f"No new content. Checked at {datetime.now().strftime('%H:%M:%S')}")

                await asyncio.sleep(300)
            except Exception as e:
                logger.error(f"Error occurred in monitoring for chat {chat_id}: {e}")
                await bot.send_message(chat_id, f"Error in monitoring: {e}")
                await asyncio.sleep(300)

# Catch-all message handler to debug incoming messages
@bot.on_message()
async def catch_all_messages(client: Client, message: Message):
    logger.debug(f"Received message in chat {message.chat.id}: {message.text or 'No text'}")

# Handler for /start command
@bot.on_message(filters.command("start") & filters.private)
async def start_command(client: Client, message: Message):
    chat_id = str(message.chat.id)
    logger.debug(f"Received /start command in private chat {chat_id}")
    await message.reply("Bot is running! Use /now to start monitoring.")

# Handler for /now command
@bot.on_message(filters.command("now") & filters.private)
async def start_monitoring(client: Client, message: Message):
    chat_id = str(message.chat.id)
    logger.debug(f"Received /now command in private chat {chat_id}")
    
    try:
        destination_chat = DESTINATION_CHAT_ID
        logger.debug(f"Monitoring will send content to chat {destination_chat}")

        await client.send_message(chat_id, f"Bot started monitoring. Content will be sent to chat {destination_chat}.")
        logger.info(f"Started monitoring for destination chat {destination_chat}")

        asyncio.create_task(monitor_todays_schedule(client, destination_chat))
    except Exception as e:
        logger.error(f"Error starting monitoring for chat {chat_id}: {e}")
        await client.send_message(chat_id, f"Failed to start monitoring: {e}")

# Health check
async def health_check(bot: Client):
    while True:
        try:
            me = await bot.get_me()
            logger.debug(f"Health check: Bot is connected as @{me.username}")
        except Exception as e:
            logger.error(f"Health check failed: {e}")
        await asyncio.sleep(600)

async def main():
    try:
        logger.info(f"Bot initialized: {bot.is_initialized}, Connected: {bot.is_connected}")

        if bot.is_connected:
            logger.info("Bot is already connected. Stopping existing session.")
            await bot.stop()

        await bot.start()
        logger.info("Bot started successfully.")

        asyncio.create_task(health_check(bot))

        await asyncio.Event().wait()
    except Exception as e:
        logger.error(f"Startup error: {e}")
        print(f"ERROR: Startup failed: {e}")
        raise
    finally:
        if bot.is_connected:
            await bot.stop()
            logger.info("Bot stopped successfully.")

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        logger.info("Bot terminated by user.")
    except Exception as e:
        logger.error(f"Main loop error: {e}")
        print(f"Main loop error: {e}")
    finally:
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()
        logger.info("Event loop closed.")
