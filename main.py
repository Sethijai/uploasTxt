from pyrogram.errors.exceptions.bad_request_400 import StickerEmojiInvalid
import requests
import json
import subprocess
from pyrogram import Client, filters
from pyrogram.types import Message
from p_bar import progress_bar
from subprocess import getstatusoutput
import helper
from logger import logging
import time
import asyncio
import sys
import re
import os
import tempfile
from bs4 import BeautifulSoup
import aiohttp
from aiohttp import ClientSession

bot = Client("bot",
             bot_token=os.environ.get("BOT_TOKEN", "7251113580:AAFOIpTAGHALclWZBexgNbevU_z6qyZuGnU"),
             api_id=int(os.environ.get("API_ID", "23713783")),
             api_hash=os.environ.get("API_HASH", "2daa157943cb2d76d149c4de0b036a99"))

STOP_COMMAND = os.environ.get("STOPING", "Stop")

@bot.on_message(filters.command([STOP_COMMAND]))
async def restart_handler(_, m):
    await m.reply_text("🚦**STOPPED**🚦", True)
    os.execl(sys.executable, sys.executable, *sys.argv)

# Initialize a dictionary to store files and status per user
user_files = {}

@bot.on_message(filters.command('h2t'))
async def collect_files(bot: Client, m: Message):
    user_id = m.from_user.id
    user_files[user_id] = {'files': [], 'status': 'collecting'}
    editable = await m.reply_text("Send all your HTML files in bulk. When done, send /h2tm to process, or /cancel to cancel.")

@bot.on_message(filters.document & filters.create(lambda _, __, m: m.from_user.id in user_files and user_files[m.from_user.id]['status'] == 'collecting'))
async def save_file(bot: Client, m: Message):
    user_id = m.from_user.id
    if len(user_files[user_id]['files']) >= 20:
        await m.reply_text("You have reached the maximum limit of 20 files.")
        return
    html_file = await m.download()
    user_files[user_id]['files'].append(html_file)
    await m.reply_text(f"File received. Total files: {len(user_files[user_id]['files'])}")

@bot.on_message(filters.command('h2tm'))
async def process_files(bot: Client, m: Message):
    user_id = m.from_user.id
    if user_id not in user_files or user_files[user_id]['status'] != 'collecting':
        await m.reply_text("No files to process. Use /h2t to start collecting files.")
        return
    user_files[user_id]['status'] = 'processing'
    all_videos = []
    for html_file in user_files[user_id]['files']:
        with open(html_file, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')
            teacher_name = soup.title.text.split('-')[-1].strip() if soup.title else "Unknown Teacher"
            rows = soup.find_all('tr')
            for row in rows:
                td_elements = row.find_all('td')
                if len(td_elements) == 0:
                    continue
                title = td_elements[0].text.strip()
                download_button = row.find('button', class_='download-btn')
                pdf_button = row.find('button', class_='pdf-btn')
                download_link = download_button['onclick'].split("'")[1] if download_button else 'NONE'
                pdf_link = pdf_button['onclick'].split("'")[1] if pdf_button else 'NONE'
                if 'NONE' in download_link:
                    download_link = 'https://i.ibb.co/4Ng0nk7/6717abd0.jpg'
                if 'NONE' in pdf_link:
                    pdf_link = 'https://i.ibb.co/4Ng0nk7/6717abd0.jpg'
                all_videos.append(f"{title} {teacher_name}: {download_link}")
                all_videos.append(f"{title} {teacher_name}: {pdf_link}")
        os.remove(html_file)
    merged_txt_file = 'HACKHEIST_Merged.txt'
    with open(merged_txt_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(all_videos))
    await m.reply_document(document=merged_txt_file, caption=f"Processed {len(user_files[user_id]['files'])} files successfully.")
    os.remove(merged_txt_file)
    del user_files[user_id]

@bot.on_message(filters.command('cancel'))
async def cancel_process(bot: Client, m: Message):
    user_id = m.from_user.id
    if user_id in user_files:
        for file_path in user_files[user_id]['files']:
            if os.path.exists(file_path):
                os.remove(file_path)
        del user_files[user_id]
        await m.reply_text("Process canceled, and all collected files have been removed.")
    else:
        await m.reply_text("No process to cancel.")

# Handler for processing messages in the format "name: URL"
@bot.on_message(filters.text & ~filters.command(["h2t", "h2tm", "cancel", STOP_COMMAND]))
async def process_link(bot: Client, m: Message):
    # Regex to match the format "name: URL"
    pattern = r"^(.*?):\s*(https?://[^\s]+)$"
    match = re.match(pattern, m.text.strip())
    if not match:
        await m.reply_text("")
        return

    # Extract name and URL
    name1 = match.group(1).strip()
    url = match.group(2).strip()

    # Delete the input message
    await m.delete()

    # Default values
    b_name = "Default Batch"
    OP = "HACKHEIST"
    NO_BW = "NOISE"
    MR = "[@TEAM_OPTECH]"
    WEB = "WEB"
    thumb = "https://i.ibb.co/W6d91vd/66f7961e.jpg"
    raw_text2 = "720"
    res = "1280x720"

    # Process thumbnail
    if thumb.startswith("http://") or thumb.startswith("https://"):
        getstatusoutput(f"wget '{thumb}' -O 'thumb.jpg'")
        thumb = "thumb.jpg"
    else:
        thumb = "no"

    # Clean up name for filename
    name1_clean = name1.replace("\t", "").replace(":", "").replace("/", "").replace("+", "").replace("#", "").replace("|", "").replace("@", "@").replace("*", "").replace("https", "").replace("http", "").replace("NONE", "https://t.me/HIDEUC").strip()
    name = f'{OP}_{name1_clean[:60]}'

    # Process URL
    V = url.replace("file/d/", "uc?export=download&id=").replace("www.youtube-nocookie.com/embed", "youtu.be").replace("?modestbranding=1", "").replace("/view?usp=sharing", "")
    url = V if V.startswith("https://") else "https://" + V

    if "visionias" in url:
        async with ClientSession() as session:
            async with session.get(url, headers={
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'Accept-Language': 'en-US,en;q=0.9',
                'Cache-Control': 'no-cache',
                'Connection': 'keep-alive',
                'Pragma': 'no-cache',
                'Referer': 'http://www.visionias.in/',
                'Sec-Fetch-Dest': 'iframe',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'cross-site',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Linux; Android 12; RMX2121) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36',
                'sec-ch-ua': '"Chromium";v="107", "Not=A?Brand";v="24"',
                'sec-ch-ua-mobile': '?1',
                'sec-ch-ua-platform': '"Android"',
            }) as resp:
                text = await resp.text()
                url = re.search(r"(https://.*?playlist.m3u8.*?)\"", text).group(1)

    elif 'videos.classplusapp' in url:
        url = requests.get(f'https://api.classplusapp.com/cams/uploader/video/jw-signed-url?url={url}', headers={
            'x-access-token': 'eyJhbGciOiJIUzM4NCIsInR5cCI6IkpXVCJ9.eyJpZCI6MzgzNjkyMTIsIm9yZ0lkIjoyNjA1LCJ0eXBlIjoxLCJtb2JpbGUiOiI5MTcwODI3NzQyODkiLCJuYW1lIjoiQWNlIiwiZW1haWwiOm51bGwsImlzRmlyc3RMb2dpbiI6dHJ1ZSwiZGVmYXVsdExhbmd1YWdlIjpudWxsLCJjb3VudHJ5Q29kZSI6IklOIiwiaXNJbnRlcm5hdGlvbmFsIjowLCJpYXQiOjE2NDMyODE4NzcsImV4cCI6MTY0Mzg4NjY3N30.hM33P2ai6ivdzxPPfm01LAd4JWv-vnrSxGXqvCirCSpUfhhofpeqyeHPxtstXwe0'
        }).json()['url']

    elif '/master.mpd' in url:
        id = url.split("/")[-2]
        token_url = f"https://play.alphacbse.fun/token?videoId={id}"
        max_retries = 3
        retry_delay = 2  # seconds

        async with ClientSession() as session:
            # Fetch token
            try:
                async with session.get(token_url) as resp:
                    if resp.status != 200:
                        await m.reply_text(f"Failed to fetch token for videoId {id}: HTTP {resp.status}")
                        return
                    token_data = await resp.json()
                    if token_data.get("status") != 200:
                        await m.reply_text(f"Invalid token response: {token_data.get('message', 'No message')}")
                        return
                    message = token_data.get("message")
                    if not message:
                        await m.reply_text("No message found in token response")
                        return
            except Exception as e:
                await m.reply_text(f"Error fetching token for videoId {id}: {str(e)}")
                return

            # Construct and check m3u8 URL with retries
            m3u8_url = f"https://play.alphacbse.fun/{message}/hls/720/main.m3u8"
            for attempt in range(max_retries):
                try:
                    async with session.head(m3u8_url) as resp:
                        if resp.status == 200:
                            url = m3u8_url  # Use this URL for downloading
                            break
                        elif resp.status == 400:
                            if attempt < max_retries - 1:
                                await asyncio.sleep(retry_delay)
                                continue
                            else:
                                await m.reply_text(f"Failed to access {m3u8_url} after {max_retries} attempts: HTTP 400")
                                return
                        else:
                            await m.reply_text(f"Unexpected status for {m3u8_url}: HTTP {resp.status}")
                            return
                except Exception as e:
                    await m.reply_text(f"Error checking {m3u8_url}: {str(e)}")
                    return

    elif '/output.webm' in url:
        url = url.replace('/output.webm', '/hls/master.m3u8')

    # Determine ytf format for videos
    ytf = f"b[height<={raw_text2}][ext=mp4]/bv[height<={raw_text2}][ext=mp4]+ba[ext=m4a]/b[ext=mp4]" if "youtu" in url else f"b[height<={raw_text2}]/bv[height<={raw_text2}]+ba/b/bv+ba"

    # Construct download command for videos
    cmd = f'yt-dlp -o "{name}.mp4" "{url}"' if "jw-prod" in url else f'yt-dlp -f "{ytf}" "{url}" -o "{name}.mp4"'

    try:
        cc = f'**{name1}.mkv**'
        cc1 = f'**{name1}.pdf**'

        if "drive" in url:
            try:
                ka = await helper.download(url, name)
                await bot.send_document(chat_id=m.chat.id, document=ka, caption=cc1)
                os.remove(ka)
            except FloodWait as e:
                await m.reply_text(f"FloodWait: {e}. Retrying after {e.x} seconds.")
                time.sleep(e.x)
                return
            except Exception as e:
                await m.reply_text(f"Error downloading Google Drive file: {str(e)}")
                return

        elif ".pdf" in url:
            try:
                # Download PDF using aiohttp
                async with ClientSession() as session:
                    async with session.get(url) as resp:
                        if resp.status == 200:
                            pdf_path = f"{name}.pdf"
                            with open(pdf_path, 'wb') as f:
                                f.write(await resp.read())
                            await bot.send_document(chat_id=m.chat.id, document=pdf_path, caption=cc1)
                            os.remove(pdf_path)
                        else:
                            await m.reply_text(f"Failed to download PDF: HTTP {resp.status}")
            except Exception as e:
                await m.reply_text(f"Error downloading PDF: {str(e)}")
                return

        else:
            Show = f"**⥥ 📥 ＤＯＷＮＬＯＡＤＩＮＧ 📥 :-**\n\n**📝Name »** `{name}\n❄𝐐𝐮𝐚𝐥𝐢𝐭𝐲 » {raw_text2}`\n\n**Url :-** `Kya karega URL dekhke ☠️☠️`\n\n **Bot made by {MR} (Daddy)🧑🏻‍💻**"
            prog = await m.reply_text(Show)
            res_file = await helper.download_video(url, cmd, name)
            filename = res_file
            await prog.delete(True)
            await helper.send_vid(bot, m, cc, filename, thumb, name, prog)
            time.sleep(1)

    except Exception as e:
        await m.reply_text(f"Error processing {url}: {str(e)}")
        return

    # Send "Done✅" message and delete it after 5 seconds
    done_msg = await m.reply_text("**Done✅**")
    await asyncio.sleep(5)
    await done_msg.delete()

bot.run()
