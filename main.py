import discord
from discord.ext import commands
# from discord import app_commands
from discord_slash import SlashCommand


import json
from time import time
import contextlib
import io
from traceback import format_exception
import textwrap
import asyncio
import phonenumbers
from phonenumbers import carrier, geocoder, timezone
from weather import parse_data
import requests
import random
from dotenv import load_dotenv
import os

def get_prefix(bot, message):
    with open("prefixes.json", "r") as f:
      prefixes = json.load(f)
    return prefixes[str(message.guild.id)]

def configure():
  load_dotenv()

intents = discord.Intents.all()

bot = commands.Bot(command_prefix=get_prefix, intents=intents)
bot.remove_command("help")
slash = SlashCommand(bot, sync_commands=True)

guild_id = [900562030723993631, 896429122358739034]

@slash.slash(name = "Ping", description = "Get the latency of the bot" , guild_ids = guild_id)
async def ping(ctx):
  start = time()
  message = await ctx.send(f"API latency: ``{bot.latency * 1000:,.0f}ms``")
  end = time()

  await message.edit(content = f"API latency: ``{bot.latency * 1000:,.0f}ms``\nResponse time: ``{(end-start)*1000:,.0f}ms``")

@slash.slash(name = "Clear", description = "To delete an amount of messages", guild_ids = guild_id)
async def clear(ctx, amount: int):

  await ctx.channel.purge(limit = amount)

  await message.delete()
  
  message = await ctx.send("Done!")


@bot.command()
async def salatiga(ctx):
  message = await ctx.send("It is <@!727482301667213352>'s hometown")
  await asyncio.sleep(5)
  await message.edit(content="Tapi boong 😂 😂")

# @bot.command()
# async def load(ctx, extension):
#   bot.load_extension(f"cogs.{extension}")
#   await ctx.send(f"The ``{extension}`` cogs have been successfully loaded")

# @bot.command()
# async def unload(ctx, extension):
#   bot.unload_extension(f"cogs.{extension}")
#   await ctx.send(f"The ``{extension}`` cogs have been successfully unloaded")

# @bot.command()
# async def check_cogs(ctx, extension):
#     try:
#         bot.load_extension(f"cogs.{extension}")
#     except commands.ExtensionAlreadyLoaded:
#         await ctx.send("Cog is loaded")
#     except commands.ExtensionNotFound:
#         await ctx.send("Cog not found")
#     else:
#         await ctx.send("Cog is unloaded")
#         bot.unload_extension(f"cogs.{extension}")


async def ch_pr():
    
    await bot.wait_until_ready()

    botStatuses = ["bijaksana2000", 
                   "discord.py", 
                   "You're mom", 
                   "Am pro",
                   "Simon Says",
                   "everything's go wrong",
                   f"{len(bot.guilds)} server's | b!help",
                   "Mr. Denjayu is a simp",
                   "Happy birthday Daniel"
                  ]

    activityType = [discord.ActivityType.watching, discord.ActivityType.streaming, discord.ActivityType.playing, discord.ActivityType.listening, discord.ActivityType.competing]

    while not bot.is_closed():
        botStatus = random.choice(botStatuses)
        botStatusType = random.choice(activityType)

        await bot.change_presence(status=discord.Status.do_not_disturb, activity=discord.Activity(type = botStatusType, name = botStatus))

        await asyncio.sleep(25)

for filename in os.listdir("./cogs"):
  if filename.endswith(".py"):
    bot.load_extension(f"cogs.{filename[:-3]}")


bot.loop.create_task(ch_pr())
configure()
bot.run(os.getenv("TOKEN"))