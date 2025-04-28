from pyrogram.errors.exceptions.bad_request_400 import StickerEmojiInvalid                                                        
import requests                                                        
import json                                                        
import subprocess                                                        
from pyrogram import Client, filters                   
from pyrogram.types.messages_and_media import message                                                        
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup                                                
from pyrogram.errors import FloodWait                                                        
from pyromod import listen                                                        
from pyrogram.types import Message                                                        
from pyrogram import Client, filters                                                        
from p_bar import progress_bar                                                        
from subprocess import getstatusoutput                                                        
from aiohttp import ClientSession                                                        
import helper                                                        
from logger import logging                                                        
import time                                                        
import asyncio                                                        
from pyrogram.types import User, Message                                                        
import sys                                                        
import re                                                        
import os
import tempfile
from urllib.parse import urlparse, parse_qs
from bs4 import BeautifulSoup
import datetime
import aiohttp
                                                        
bot = Client("bot",                                                        
             bot_token=os.environ.get("BOT_TOKEN", "7251113580:AAFOIpTAGHALclWZBexgNbevU_z6qyZuGnU"),                                                        
             api_id=int(os.environ.get("API_ID", "23713783")),                                                        
             api_hash=os.environ.get("API_HASH", "2daa157943cb2d76d149c4de0b036a99"))

OP_COMMAND = os.environ.get("COMMAND", "op")
STOP_COMMAND = os.environ.get("STOPING", "Stop")
                                                        
                                                        
@bot.on_message(filters.command([STOP_COMMAND]))                                                        
async def restart_handler(_, m):                                                        
    await m.reply_text("🚦**STOPPED**🚦", True)                                                        
    os.execl(sys.executable, sys.executable, *sys.argv)

@bot.on_message(filters.command([OP_COMMAND]))
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
                                                        
thumb == "no"                                                
                                                        
            if '/master.mpd' in url:                                                        
             id =  url.split("/")[-2]                                                        
             url =  f"https://madxapi-d0cbf6ac738c.herokuapp.com/{id}/master.m3u8&token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MzgzNzI5NDkuNDkyLCJkYXRhIjp7Il9pZCI6IjY0YjY0NDhkNjAxYWM2MDAxOGQ5ODE1MyIsInVzZXJuYW1lIjoiOTM1MjYzMTczMSIsImZpcnN0TmFtZSI6Ik5hbWFuIiwibGFzdE5hbWUiOiIiLCJvcmdhbml6YXRpb24iOnsiX2lkIjoiNWViMzkzZWU5NWZhYjc0NjhhNzlkMTg5Iiwid2Vic2l0ZSI6InBoeXNpY3N3YWxsYWguY29tIiwibmFtZSI6IlBoeXNpY3N3YWxsYWgifSwiZW1haWwiOiJvcG1hc3Rlcjk4NTRAZ21haWwuY29tIiwicm9sZXMiOlsiNWIyN2JkOTY1ODQyZjk1MGE3NzhjNmVmIl0sImNvdW50cnlHcm91cCI6IklOIiwidHlwZSI6IlVTRVIifSwiaWF0IjoxNzM3NzY4MTQ5fQ.2XmPDj4eXBQc1Hn23Ssy8aPIURrgYnikLqgkYi6qHYY"


                                                        
            name1 = links[i][0].replace("\t", "").replace(":", "").replace("/", "").replace("+", "").replace("#", "").replace("|", "").replace("@", "@").replace("*", "").replace("https", "").replace("http", "").replace("NONE", "https://t.me/HIDEUC").strip()                                                        
            name = f'{name1[:60]}'                                                        
                                                        
            if "youtu" in url:                                                        
                ytf = f"b[height<=720][ext=mp4]/bv[height<=720][ext=mp4]+ba[ext=m4a]/b[ext=mp4]"                                                        
            else:                                                        
                ytf = f"b[height<=720]/bv[height<=720]+ba/b/bv+ba"                                                                                                                
                                                        
            try:                                                          
                                                                        
                cc = f'**{name1}.mkv**\n\n**𝗕𝗮𝘁𝗰𝗵 - OP **'
                cc1 = f'**{name1}.pdf**\n\n**𝗕𝗮𝘁𝗰𝗵 - OP **'
                                                                        
                if ".pdf" in url:                                                        
                    try:                                                        
                        cmd = f'yt-dlp -o "{name}.pdf" "{url}"'                                                        
                        download_cmd = f"{cmd} -R 25 --fragment-retries 25"                                                        
                        os.system(download_cmd)                                                        
                        copy = await bot.send_document(chat_id=m.chat.id, document=f'{name}.pdf', caption=cc1)                                                        
                        count += 1                                                        
                        os.remove(f'{name}.pdf')                                                        
                    except FloodWait as e:                                                        
                        await m.reply_text(str(e))                                                        
                        time.sleep(e.x)                                                        
                        continue                                                        
                else:                                                        
                    Show = f"**⥥ 📥 ＤＯＷＮＬＯＤＩＮＧ 📥 :-**\n\n**📝Name »** `{name}\n❄𝐐𝐮𝐚𝐥𝐢𝐭𝐲 » {raw_text2}`\n\n**Url :-** `Kya karega URL dekhke ☠️☠️`\n\n **Bot made by {MR} (Daddy)🧑🏻‍💻**"                                                        
                    prog = await m.reply_text(Show)                                                        
                    res_file = await helper.download_video(url, cmd, name)                                                        
                    filename = res_file                                                        
                    await prog.delete(True)                                                        
                    await helper.send_vid(bot, m, cc, filename, thumb, name, prog)                                                        
                    count += 1                                                        
                    time.sleep(1)                                                        
                                                        
            except Exception as e:                                                        
                await m.reply_text(                                                        
                    f"**𝐖𝐚𝐭𝐜𝐡 𝐓𝐡𝐢𝐬 𝐎𝐧 𝐘𝐎𝐔𝐓𝐔𝐁𝐄 🙏**\n\n**{url}**\n\n**{cc}**"                                                        
                )                                                        
                continue                                                        
                                                        
    except Exception as e:                                                        
        await m.reply_text(e)                                                        
    await m.reply_text("**Done✅**")                                                        
                                                        
                                                        
bot.run()                                                        
                                                        
