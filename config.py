import discord
from discord.ext import commands
import os

intents=discord.Intents.default()

Bot=commands.Bot(command_prefix='/', intents=intents)
TOKEN=os.getenv("DISCORD_BOT_TOKEN")
API_TOKEN=os.getenv("GOFILE_TOKEN")

