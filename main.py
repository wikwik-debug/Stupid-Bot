from datetime import datetime
from pydoc import describe
from tokenize import group
import discord
from discord import Embed, Guild, Colour, Intents, Member, User, File
from discord.ext import commands
from discord.ext.commands import Bot
from discord.utils import snowflake_time

import json
import asyncio
import random
from dotenv import load_dotenv
import os
import requests
from datetime import datetime
import aiohttp
from bs4 import BeautifulSoup

from utils.randomSentences import getRandomSentences

load_dotenv()

def get_prefix(bot, message):
    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)
    return prefixes[f"{str(message.guild.name)}({str(message.guild.id)})"]

bot = Bot(command_prefix=get_prefix, intents=Intents.all(), case_insensitive=True, strip_after_prefix=True)
bot.remove_command("help")

snipe_message_content = None
snipe_message_author = None

@bot.event
async def on_message_delete(message):
    global snipe_message_content
    global snipe_message_author

    snipe_message_content = message.content
    snipe_message_author = message.author.name
    await asyncio.sleep(60)
    snipe_message_content = None
    snipe_message_author = None

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
async def randomSentence(ctx):
    await ctx.send(getRandomSentences())

@bot.command()
async def snow(ctx, id):
    parsedResult = int(id)
    timeFormatted = snowflake_time(parsedResult).strftime("Date: %A, %d %B %Y\nTime: %H:%M:%S %p")
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

@bot.command(name="gb")
async def guildBanner(ctx, guild: Guild):
    fetchedGuild = await bot.fetch_guild(guild.id)
    await ctx.send(fetchedGuild.banner_url)

@bot.command()
async def iplookup(ctx, ipAddress:str = "9.9.9.9"):
    res = requests.get(f"https://extreme-ip-lookup.com/json/{ipAddress}?key={os.getenv('IP_API')}")
    data = res.json()
    em = Embed()
    fields = [
        {"name": "IP", "value": data["query"]},
        {"name": "IP Type", "value": data["ipType"]},
        {"name": "Country", "value": data["country"]},
        {"name": "City", "value": data["city"]},
        {"name": "Continent", "value": data["continent"]},
        {"name": "IP Name", "value": data["ipName"]},
        {"name": "ISP", "value": data["isp"]},
        {"name": "Latitute", "value": data["lat"]},
        {"name": "Longitute", "value": data["lon"]},
        {"name": "Organization", "value": data["org"]},
        {"name": "Business", "value": data["businessName"]},
        {"name": "Region", "value": data["region"]}
    ]
    for field in fields:
        if field["value"]:
            em.set_footer(text="\u200b")
            em.timestamp = datetime.utcnow()
            em.add_field(name=field["name"], value=field["value"], inline=True)
    return await ctx.send(embed = em)

@bot.command()
async def snipe(message):
    if snipe_message_content == None:
        await message.channel.send("No message to snipe!")
    else:
        snipeEmbed = Embed(
            description = f"{snipe_message_content}",
            color = Colour.random()
        )
        snipeEmbed.set_footer(text=f"Requested by {message.author}")
        snipeEmbed.set_author(name=f"Sniped the message deleted by {snipe_message_author}")
        await message.channel.send(embed = snipeEmbed)

@bot.command()
async def gtl(ctx):
    # *, answer:str
    headers = {
        "Authorization": os.getenv("DAGAPI_KEY")
    }
    res = requests.get('https://api.dagpi.xyz/data/logo', headers=headers)
    data = res.json()
    
    guessTheLogoGameEmbed = Embed(
        title="Guess The Logo!",
        description="Your task here is to guess the logo shown below:",
        colour = 0xffffff
    )

    rightAnswerEmbed = Embed(
        title="You got it right! 🥳🎉",
        colour = 0x44b582
    )

    wrongAnswerEmbed = Embed(
        title="Wrong!",
        description="The right answer is:",
        colour = 0xff0000
    )

    guessTheLogoGameEmbed.set_image(url=data["question"])
    guessTheLogoGameEmbed.set_footer(text="You have 60 seconds to guess!")
    
    await ctx.send(embed = guessTheLogoGameEmbed)
    # await ctx.send(data["answer"])
    # await ctx.send(data)

async def web_scrape(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as res:
            status = res.status
            if status == 200:
                text = await res.text()
                return text

@bot.command()
async def wyr(ctx):
    text = await web_scrape("https://either.io/")
    
    soup = BeautifulSoup(text, "lxml")
    
    arr = []
    
    for choice in soup.find_all("span", {"class": "option-text"}):
        arr.append(choice.text)
    
    description = f"""
    **EITHER...**
    :regional_indicator_a: {arr[0]}

    **OR...**
    :regional_indicator_b: {arr[1]}
    """

    e = Embed(
        description = description,
        color = Colour.random()
    )

    e.set_author(name="Would you rather...", url="https://either.io/", icon_url=ctx.bot.user.avatar_url)
    e.set_footer(text=f"Requested by: {ctx.author}", icon_url=ctx.author.avatar_url)
    msg = await ctx.send(embed = e)
    await msg.add_reaction("🇦")
    await msg.add_reaction("🇧")

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


for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")

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

bot.loop.create_task(ch_pr())
bot.run(os.getenv("TOKEN"))