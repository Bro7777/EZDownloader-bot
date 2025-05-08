import discord
from discord.ext import commands
import os
from typing import Literal
import yt_dlp
import requests
from config import *
import uuid
import aiohttp
import asyncio
import datetime


async def download_media(url: str, format: str) -> str:
    unique_id= str(uuid.uuid4()) 
    out=unique_id if format == "mp3" else unique_id+"." + format
    ydl_opts = {
        'outtmpl': out,
        'quiet': True
    }

    if format == "mp3":
        ydl_opts.update({
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        })
    elif format == "mp4":
        ydl_opts.update({
            'format': 'bestvideo+bestaudio/best',
            'merge_output_format': 'mp4'
        })

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    return out + ".mp3" if format == "mp3" else out

async def upload_to_gofile(file_path: str, token: str =API_TOKEN):
    with open(file_path, 'rb') as f:
        files = {'file': f}
        data = {'token': token} if token else {}

        resp = requests.post("https://upload.gofile.io/uploadFile", files=files, data=data,timeout=120)

    try:
        result = resp.json()
    except Exception:
        raise RuntimeError(f"There is an error with GoFile : {resp.text}")

    if result.get("status") != "ok" or 'data' not in result or 'downloadPage' not in result['data']:
        raise RuntimeError(f"Unsuccessful upload process: {result}")

    return result['data']['downloadPage']




@Bot.tree.command(name="download",description="Download a video and get a link")
async def download(interaction : discord.Interaction,url : str,format:Literal['mp4','mp3']):
    await interaction.response.defer(ephemeral=True)
    try:
        file_path = await download_media(url, format)
        gofile_link = await upload_to_gofile(file_path)
        await interaction.followup.send(f"✅ File uploaded!\n🔗 {gofile_link}",ephemeral=True)
    except Exception as e:
        await interaction.followup.send(f"❌ Error: {e}",ephemeral=True)

@Bot.tree.command(name='info',description="Information about the bot")
async def info(interaction:discord.Interaction):
    dev_id = "<@800233701907759189>"
    about_bot=(
            "**EZDownloader** is a simple and powerful media downloading bot.\n\n"
            "🛠️ **Features:**\n"
            "• Download videos or audio (MP4/MP3) from supported URLs (e.g., YouTube, Twitter).\n"
            "• Files are uploaded to Gofile and a private link is sent to you.\n"
            "• All uploaded files are automatically deleted every night at 00:00 (server time).\n\n"
            "⚙️ **How to Use:**\n"
            "`/download <url> <format>` — Downloads the file from the URL (format: mp4 or mp3).\n\n"
            f"👨‍💻 **Developed by:** {dev_id}\n"
            "📌 **Version:** v1.0"
        )
    info_embed=discord.Embed(title="📥 EZDownloader Bot",description=about_bot)
    await interaction.response.send_message(embed=info_embed)





async def delete_all_files():
    async with aiohttp.ClientSession() as session:
        url = f"https://api.gofile.io/getAccountDetails?token={API_TOKEN}"
        async with session.get(url) as res:
            data = await res.json()
            if data["status"] != "ok":
                print("❌ Failed to fetch account details.")
                return
            contents = data["data"]["contents"]
            file_ids = list(contents.keys())

        print(f"📦 Found {len(file_ids)} file(s). Deleting...")


        for file_id in file_ids:
            delete_url = f"https://api.gofile.io/deleteUpload?fileId={file_id}&token={API_TOKEN}"
            async with session.delete(delete_url) as del_res:
                del_data = await del_res.json()
                if del_data["status"] == "ok":
                    print(f"✅ Deleted {file_id}")
                else:
                    print(f"❌ Failed to delete {file_id}: {del_data}")




async def schedule_midnight_deletion():
    while True:
        now = datetime.datetime.now()
        next_run = (now + datetime.timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        wait_seconds = (next_run - now).total_seconds()
        await asyncio.sleep(wait_seconds)
        await delete_all_files()




async def add_commands():
   Bot.tree.add_command(download)


