from datetime import datetime
import discord
from discord import Embed, Guild, Colour, Intents, User, File
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
import giphy_client
from giphy_client.rest import ApiException
from io import BytesIO
from re import findall
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import logging

from utils.randomSentences import getRandomSentences

load_dotenv()

def get_prefix(bot, message):
    with open("./json/prefixes.json", "r") as f:
        prefixes = json.load(f)
    return prefixes[f"{str(message.guild.name)}({str(message.guild.id)})"]

bot = Bot(command_prefix=get_prefix, intents=Intents.all(), case_insensitive=True, strip_after_prefix=True)
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

@bot.command()
async def gif(ctx, *, q:str = "smile"):
    apiKey = os.environ.get("GIPHY_API_KEY")
    apiInstance = giphy_client.DefaultApi()
    try:
        apiRes = apiInstance.gifs_search_get(apiKey, q)
        ls = list(apiRes.data)
        gif = random.choice(ls)
        gifEmbed = Embed(title=q.title(), color = 0xffffff)
        gifEmbed.set_image(url=f"https://media.giphy.com/media/{gif.id}/giphy.gif")
        await ctx.send(embed = gifEmbed)
    except ApiException:
        print("An error has occured!")

@bot.command()
async def mosaic(ctx, pixels:int, imgType:str, picUrl:str):
    headers = {
        "Authorization": f"{os.environ.get('DAGAPI_KEY')}",
        "Content-Type": f"image/{imgType}"
    }

    if pixels > 32:
        await ctx.send("Too many pixels to render")

    r = requests.get(f"https://api.dagpi.xyz/image/mosiac/?url={picUrl}&pixels={pixels}", headers=headers)

    if findall(".webp", picUrl):
        await ctx.send("Image type is not supported")
    elif findall(".gif", picUrl):
        if r.status_code == 200:
            await ctx.send(file=File(BytesIO(r.content), "wanted.gif"))
        elif r.status_code == 413:
            errMsg = r.json()
            await ctx.reply(errMsg["message"])
    else:
        if r.status_code == 200:
            await ctx.send(file=File(BytesIO(r.content), "mosaic.png"))
        elif r.status_code == 413:
            errMsg = r.json()
            await ctx.reply(errMsg["message"])
        else:
            print(r.text)
            print(r.status_code)

@bot.command()
async def wanted(ctx, user:User = None):
    finalUser = ctx.author if user is None else user
    
    headers = {
        "Authorization": f"{os.environ.get('DAGAPI_KEY')}",
        "Content-Type": "image/png"
    }

    r = requests.get(f"https://api.dagpi.xyz/image/wanted/?url={finalUser.avatar_url_as(format='png', size=4096)}", headers=headers)

    if r.status_code == 200:
        await ctx.send(file=File(BytesIO(r.content), "wanted.png"))
    elif r.status_code == 413:
        errMsg = r.json()
        await ctx.reply(errMsg["message"])

@bot.command()
async def ss(ctx, url:str, delay:int = 1):
    logging.getLogger('WDM').setLevel(logging.NOTSET)
    
    option = Options()
    option.headless = True
    option.add_argument("--window-size=1920,1080")
    option.add_argument("--disable-gpu")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager(version="102.0.5005.61").install()), options=option)
    driver.get(url)
    await asyncio.sleep(10 * delay)
    await ctx.send(file=File(BytesIO(driver.get_screenshot_as_png()), "webCapture.png"))



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