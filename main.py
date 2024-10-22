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
             bot_token=os.environ.get("BOT_TOKEN"),                                                        
             api_id=int(os.environ.get("API_ID")),                                                        
             api_hash=os.environ.get("API_HASH"))                                                        
                                                        
                                                        
@bot.on_message(filters.command("Stop"))                                                        
async def restart_handler(_, m):                                                        
    await m.reply_text("🚦**STOPPED**🚦", True)                                                        
    os.execl(sys.executable, sys.executable, *sys.argv)

@bot.on_message(filters.command('h2t'))
async def run_bot(bot: Client, m: Message):
    editable = await m.reply_text("Send Your HTML file\n")
    input: Message = await bot.listen(editable.chat.id)
    html_file = await input.download()
    await input.delete(True)
    await editable.delete()

    # Open and read the HTML file using BeautifulSoup
    with open(html_file, 'r') as f:
        soup = BeautifulSoup(f, 'html.parser')
        
        # Extract teacher name from the title
        teacher_name = soup.title.text.split('-')[-1].strip()
        
        # Find all rows
        rows = soup.find_all('tr')
        videos = []

        for row in rows:
            td_elements = row.find_all('td')
            if len(td_elements) == 0:
                continue

            # Extract video title
            title = td_elements[0].text.strip()

            # Extract download and PDF links
            download_button = row.find('button', class_='download-btn')
            pdf_button = row.find('button', class_='pdf-btn')

            download_link = download_button['onclick'].split("'")[1] if download_button else 'No download link'
            pdf_link = pdf_button['onclick'].split("'")[1] if pdf_button else 'No PDF link'

            # Append both download and PDF links with the teacher's name to the list
            videos.append(f"{title} {teacher_name}: {download_link}")
            videos.append(f"{title} {teacher_name}: {pdf_link}")

    # Create a text file to save the extracted data
    txt_file = os.path.splitext(html_file)[0] + '.txt'
    with open(txt_file, 'w') as f:
        f.write('\n'.join(videos))

    # Send the text file as a reply
    await m.reply_document(document=txt_file, caption="Le Gand me Dable BSDK 😡\nWords By - 𝗛𝗔𝗖𝗞𝗛𝗘𝗜𝗦𝗧")
    
    # Remove the local text file after sending it
    os.remove(txt_file)
                                                        
                                                        
                                                        
@bot.on_message(filters.command(["op"]))                                                        
async def account_login(bot: Client, m: Message):                                                        
    editable = await m.reply_text('**Send TXT file for download**')                                                        
    input: Message = await bot.listen(editable.chat.id)                                                        
    x = await input.download()                                                        
    await input.delete(True)                                                        
    file_name, ext = os.path.splitext(os.path.basename(x))                                                        
                                                            
                                                        
                                                        
    path = f"./downloads/{m.chat.id}"                                                        
                                                        
    try:                                                        
       with open(x, "r") as f:                                                        
           content = f.read()                                                        
       content = content.split("\n")                                                        
       links = []                                                        
       for i in content:                                                        
           links.append(i.split("://", 1))                                                        
       os.remove(x)                                                        
            # print(len(links)                                                        
    except:                                                        
           await m.reply_text("Invalid file input.")                                                        
           os.remove(x)                                                        
           return                                                        
                                                            
                                                           
    await editable.edit(f"Total links found are **{len(links)}**\n\nSend From where you want to download initial is **1**")                                                        
    input0: Message = await bot.listen(editable.chat.id)                                                        
    raw_text = input0.text                                                        
    await input0.delete(True)                                                        
                                                        
    await editable.edit("**Enter Batch Name or send /d for grabing from text filename.**")                                                        
    input1: Message = await bot.listen(editable.chat.id)                                                        
    raw_text0 = input1.text                                                        
    await input1.delete(True)                                                        
    if raw_text0 == '/d':                                                        
        b_name = file_name                                                        
    else:                                                        
        b_name = raw_text0                                                        
    
    await editable.edit("**Enter Your Name like `HACKHEIST` or send  `op` for use default**")                                                        
    input15: Message = await bot.listen(editable.chat.id)                                                        
    raw_text15 = input15.text                                                        
    await input15.delete(True)                                                        
    highlighter  = f"️ ⁪⁬⁮⁮⁮"
    if raw_text15 == 'op':
        OP = highlighter 
    else:
        OP = raw_text15

    await editable.edit("**Enter resolution**")                                                        
    input2: Message = await bot.listen(editable.chat.id)                                                        
    raw_text2 = input2.text                                                        
    await input2.delete(True)                                                        
    try:                                                        
        if raw_text2 == "144":                                                        
            res = "256x144"                                                        
        elif raw_text2 == "240":                                                        
            res = "426x240"                                                        
        elif raw_text2 == "360":                                                        
            res = "640x360"                                                        
        elif raw_text2 == "480":                                                        
            res = "854x480"                                                        
        elif raw_text2 == "720":                                                        
            res = "1280x720"                                                        
        elif raw_text2 == "1080":                                                        
            res = "1920x1080"                                                         
        else:                                                         
            res = "UN"                                                        
    except Exception:                                                        
            res = "UN"                                                        
                                                            
                                                            
                                                        
    await editable.edit("**Enter Your Name like `[@TEAM_OPTECH]` or send `de` for use default**")                                                        
    input3: Message = await bot.listen(editable.chat.id)                                                        
    raw_text3 = input3.text                                                        
    await input3.delete(True)                                                        
    highlighter  = f"️ ⁪⁬⁮⁮⁮"
    if raw_text3 == 'de':
        MR = highlighter 
    else:
        MR = raw_text3
      
    await editable.edit("**Enter Your Website Url ☠️ or send `WEB` for use default\n\nAsk from HACKHEIST 🙏 or Leave this**")                                                        
    input8: Message = await bot.listen(editable.chat.id)                                                        
    raw_text8 = input8.text                                                        
    await input8.delete(True)                                                        
    highlighter  = f"️ ⁪⁬⁮⁮⁮"
    if raw_text8 == 'WEB':
        WEB = highlighter 
    else:
        WEB = raw_text8
                                                           
    await editable.edit("**USE THIS - `https://i.ibb.co/W6d91vd/66f7961e.jpg` **")  
    input6 = message = await bot.listen(editable.chat.id)
    raw_text6 = input6.text
    await input6.delete(True)
    #await editable.delete()
    thumb = input6.text
                                                            
                                                            
    if thumb.startswith("http://") or thumb.startswith("https://"):                                                        
        getstatusoutput(f"wget '{thumb}' -O 'thumb.jpg'")                                                        
        thumb = "thumb.jpg"                                                        
    else:                                                        
        thumb == "no"                                                        
                                                        
    if len(links) == 1:                                                        
        count = 1                                                        
    else:                                                        
        count = int(raw_text)                                                        
                                                        
    try:                                                        
        for i in range(count - 1, len(links)):                                                        
                                                        
            V = links[i][1].replace("file/d/","uc?export=download&id=").replace("www.youtube-nocookie.com/embed", "youtu.be").replace("?modestbranding=1", "").replace("/view?usp=sharing","") # .replace("mpd","m3u8")                                                        
            url = "https://" + V                                                        
                                                        
            if "visionias" in url:                                                        
                async with ClientSession() as session:                                                        
                    async with session.get(url, headers={'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'Accept-Language': 'en-US,en;q=0.9', 'Cache-Control': 'no-cache', 'Connection': 'keep-alive', 'Pragma': 'no-cache', 'Referer': 'http://www.visionias.in/', 'Sec-Fetch-Dest': 'iframe', 'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-Site': 'cross-site', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (Linux; Android 12; RMX2121) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36', 'sec-ch-ua': '"Chromium";v="107", "Not=A?Brand";v="24"', 'sec-ch-ua-mobile': '?1', 'sec-ch-ua-platform': '"Android"',}) as resp:                                                        
                        text = await resp.text()                                                        
                        url = re.search(r"(https://.*?playlist.m3u8.*?)\"", text).group(1)                                                        
                                                        
            elif 'videos.classplusapp' in url:                                                        
             url = requests.get(f'https://api.classplusapp.com/cams/uploader/video/jw-signed-url?url={url}', headers={'x-access-token': 'eyJhbGciOiJIUzM4NCIsInR5cCI6IkpXVCJ9.eyJpZCI6MzgzNjkyMTIsIm9yZ0lkIjoyNjA1LCJ0eXBlIjoxLCJtb2JpbGUiOiI5MTcwODI3NzQyODkiLCJuYW1lIjoiQWNlIiwiZW1haWwiOm51bGwsImlzRmlyc3RMb2dpbiI6dHJ1ZSwiZGVmYXVsdExhbmd1YWdlIjpudWxsLCJjb3VudHJ5Q29kZSI6IklOIiwiaXNJbnRlcm5hdGlvbmFsIjowLCJpYXQiOjE2NDMyODE4NzcsImV4cCI6MTY0Mzg4NjY3N30.hM33P2ai6ivdzxPPfm01LAd4JWv-vnrSxGXqvCirCSpUfhhofpeqyeHPxtstXwe0'}).json()['url']                                                        
                                                        
            elif '/master.mpd' in url:                                                        
             id =  url.split("/")[-2]                                                        
             url =  "https://d26g5bnklkwsh4.cloudfront.net/" + id + "/master.m3u8"                                                        
                                                        
            name1 = links[i][0].replace("\t", "").replace(":", "").replace("/", "").replace("+", "").replace("#", "").replace("|", "").replace("@", "@").replace("*", "").replace(".", "").replace("https", "").replace("http", "").strip()                                                        
            name = f'{OP} {MR} {name1[:60]}'                                                        
                                                        
            if "youtu" in url:                                                        
                ytf = f"b[height<={raw_text2}][ext=mp4]/bv[height<={raw_text2}][ext=mp4]+ba[ext=m4a]/b[ext=mp4]"                                                        
            else:                                                        
                ytf = f"b[height<={raw_text2}]/bv[height<={raw_text2}]+ba/b/bv+ba"                                                        
                                                        
            if "jw-prod" in url:                                                        
                cmd = f'yt-dlp -o "{name}.mp4" "{url}"'                                                        
            else:                                                        
                cmd = f'yt-dlp -f "{ytf}" "{url}" -o "{name}.mp4"'                                                        
                                                        
            try:                                                          
                                                                        
                cc = f'**{name1} {MR}.mkv**\n\n**❃ 𝗕𝗮𝘁𝗰𝗵 » {b_name}**\n\n**♛ 𝔻𝕆𝕎ℕ𝕃𝕆𝔸𝔻𝔼𝔻 𝔹𝕐 ★ {MR}**\n**━━━━━━━✦✗✦━━━━━━━**\n**{WEB}**'
                cc1 = f'**{name1} {MR}.pdf**\n\n**❃ 𝗕𝗮𝘁𝗰𝗵 » {b_name}**\n\n**♛ 𝔻𝕆𝕎ℕ𝕃𝕆𝔸𝔻𝔼𝔻 𝔹𝕐 ★ {MR}**\n**━━━━━━━✦✗✦━━━━━━━**\n**{WEB}**'
                if "drive" in url:                                                        
                    try:                                                        
                        ka = await helper.download(url, name)                                                        
                        copy = await bot.send_document(chat_id=m.chat.id,document=ka, caption=cc1)                                                        
                        count+=1                                                        
                        os.remove(ka)                                                        
                        time.sleep(1)                                                        
                    except FloodWait as e:                                                        
                        await m.reply_text(str(e))                                                        
                        time.sleep(e.x)                                                        
                        continue                                                        
                                                                        
                elif ".pdf" in url:                                                        
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
                    f"**Failed to Download/Extract 😫**\n\n**Name** - {cc}\n**𝗟𝗜𝗡𝗞** - {url}\n\nSorry {MR} 🙏**"                                                        
                )                                                        
                continue                                                        
                                                        
    except Exception as e:                                                        
        await m.reply_text(e)                                                        
    await m.reply_text("**Done✅**")                                                        
                                                        
                                                        
bot.run()                                                        
                                                        
