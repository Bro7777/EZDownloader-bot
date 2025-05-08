import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import asyncio

load_dotenv()

from config import *
from commands import schedule_midnight_deletion

@Bot.event
async def on_ready():
    try:
      synced=await Bot.tree.sync()
      print(f"Synced {len(synced)} command(s)")
      print(f"Bot is ready: {Bot.user}")
      asyncio.create_task(schedule_midnight_deletion())
    except Exception as e:
       print(f"Error: {e}")


Bot.run(TOKEN)