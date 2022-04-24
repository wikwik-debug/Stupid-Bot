import discord
from discord import Embed, Guild, Colour, User
from discord.ext.commands import Bot
from discord.utils import snowflake_time
# from discord import app_commands

import json
import asyncio
import random
from dotenv import load_dotenv
import os
import requests


from randomSentences import getRandomSentences

def get_prefix(bot, message):
    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)
    return prefixes[f"{str(message.guild.name)}({str(message.guild.id)})"]

def configure():
    load_dotenv()

intents = discord.Intents.all()

bot = Bot(command_prefix=get_prefix, intents=intents, case_insensitive=True, strip_after_prefix=True)
bot.remove_command("help")

@bot.command()
async def salatiga(ctx):
    message = await ctx.send("It is <@!727482301667213352>'s hometown")
    await asyncio.sleep(5)
    await message.edit(content="Tapi boong 😂 😂")

@bot.command()
async def guilds(ctx):
    for i in bot.guilds:
        botGuildEmbed = Embed(
            title=i.name,
            color = Colour.random()
        ) 
        botGuildEmbed.set_thumbnail(url=i.owner.avatar_url)
        botGuildEmbed.set_image(url=i.icon_url)
        
        botGuildEmbed.add_field(name="Server ID:", value=i.id, inline=False)
        botGuildEmbed.add_field(name="Server Owner:", value=f"{i.owner} ({i.owner_id})", inline=True)
        botGuildEmbed.add_field(name="Member Count:", value=i.member_count, inline=False)

        await ctx.send(embed=botGuildEmbed)

@bot.command()
async def test(ctx):
    await ctx.send(getRandomSentences())

@bot.command()
async def snow(ctx, id):
    parsedResult = int(id)
    timeFormatted = snowflake_time(parsedResult).strftime("Date: %A, %d %B %Y\nTime: %H:%M %p")
    await ctx.send(timeFormatted)

@bot.command()
async def leave(ctx, guild: Guild = None):
    fetchedGuild = await bot.fetch_guild(guild.id)
    appinfo = await bot.application_info()

    if guild is None:
        await ctx.reply("Pleave provide a guild/server to leave")
    elif ctx.author != appinfo.owner:
        await ctx.reply("You cant execute this command because your not the owner of the bot")
    else:
        await fetchedGuild.leave()
        await ctx.send(f"I have left the guild called: {fetchedGuild.name} (`{fetchedGuild.id}`)")


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

    appinfo = await bot.application_info()

    botStatuses = [
        f"{appinfo.owner}",
        "discord.py",
        "You're mom",
        "Am pro",
        "Simon Says",
        "everything's go wrong",
        f"{len(bot.guilds)} server's | sb!help",
        "Mr. Denjayu is a simp",
        "overspeculation"
    ]

    activityType = [discord.ActivityType.watching, discord.ActivityType.streaming, discord.ActivityType.playing, discord.ActivityType.listening, discord.ActivityType.competing]

    while not bot.is_closed():
        botStatus = random.choice(botStatuses)
        botStatusType = random.choice(activityType)

        await bot.change_presence(activity=discord.Activity(type = botStatusType, name = botStatus))

        await asyncio.sleep(25)


for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")


bot.loop.create_task(ch_pr())
configure()
bot.run(os.getenv("TOKEN"))