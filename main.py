import discord
from discord import Embed, Status
from discord.ext import commands
# from discord import app_commands
from discord_slash import SlashCommand


import json
from time import time
import asyncio
import requests
import random
from dotenv import load_dotenv
import os
from datetime import datetime
from randomSentences import getRandomSentences

def get_prefix(bot, message):
    with open("prefixes.json", "r") as f:
      prefixes = json.load(f)
    return prefixes[f"{str(message.guild.name)}({str(message.guild.id)})"]

def configure():
  load_dotenv()

intents = discord.Intents.all()

bot = commands.Bot(command_prefix=get_prefix, intents=intents)
bot.remove_command("help")
slash = SlashCommand(bot, sync_commands=True)

guild_id = [900562030723993631, 896429122358739034, 929595596413747261]

@slash.slash(name = "Ping", description = "Get the latency of the bot" , guild_ids = guild_id)
async def ping(ctx):
  start = time()
  message = await ctx.send(f"API latency: ``{bot.latency * 1000:,.0f}ms``")
  end = time()

  await message.edit(content = f"API latency: ``{bot.latency * 1000:,.0f}ms``\nResponse time: ``{(end-start)*1000:,.0f}ms``")

@slash.slash(name = "Clear", description = "To delete an amount of messages", guild_ids = guild_id)
async def clear(ctx, amount: int):

  await ctx.channel.purge(limit = amount)

  message = await ctx.send("Done!")

  await message.delete()


@bot.command()
async def salatiga(ctx):
  message = await ctx.send("It is <@!727482301667213352>'s hometown")
  await asyncio.sleep(5)
  await message.edit(content="Tapi boong 😂 😂")

@bot.command()
async def nsfw(ctx, type = None):

  if type == "food":
    await ctx.send("This type is blacklisted from the command\nReason: Not NSFW related")
  elif type == "coffee":
    await ctx.send("This type is blacklisted from the command\nReason: Not NSFW related")
  elif type == "kanna":
    await ctx.send("This type is blacklisted from the command\nReason: Not NSFW related")
  elif type == "neko":
    await ctx.send("This type is blacklisted from the command\nReason: Not NSFW related")
  elif type == "holo":
    await ctx.send("This type is blacklisted from the command\nReason: Not NSFW related")
  elif type == "kemonomimi":
    await ctx.send("This type is blacklisted from the command\nReason: Not NSFW related")
  elif type == "gah":
    await ctx.send("This type is blacklisted from the command\nReason: Not NSFW related")
  elif type == "tentacle":
    await ctx.send("This type is blacklisted from the command")
  elif type == "yaoi":
    await ctx.send("This type is blacklisted from the command\nReason: Homosexual")
  elif type == "porngif":
    urlType = f"https://nekobot.xyz/api/image?type=pgif"
    
    responseType = requests.get(urlType)
    
    dataType = json.loads(responseType.text)
    
    responseEmbedType = Embed(
      url = dataType["message"],
      title = "<:NSFW:962289749954027571> Pgif",
      color = 0xffffff
    )
    
    urlTypeEmbed = dataType["message"]
    
    responseEmbedType.set_image(url=urlTypeEmbed)
    
    responseEmbedType.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
    
    await ctx.send(embed = responseEmbedType)
  elif type == None:
      typeEmbed = Embed(
        title="List of available types:",
        description = """
        - hass
        - hmidriff
        - pgif
        - 4k
        - hentai
        - hneko
        - hkitsune
        - anal
        - hanal
        - gonewild
        - ass
        - pussy
        - thigh
        - hthigh
        - paizuri
        - boobs
        - hboobs
        """
      )

      await ctx.send(embed = typeEmbed)
  else:
    url = f"https://nekobot.xyz/api/image?type={type}"
    
    response = requests.get(url)
    
    data = json.loads(response.text)
    
    if data["message"] == "Unknown Image Type":
      message = await ctx.reply("Invalid type!")
      
      await asyncio.sleep(5)
      
      await message.delete()
      
      validEmbed = Embed(
        title="Current Valid types:",
        description = """
        - hass
        - hmidriff
        - pgif
        - 4k
        - hentai
        - hneko
        - hkitsune
        - anal
        - hanal
        - gonewild
        - ass
        - pussy
        - thigh
        - hthigh
        - paizuri
        - boobs
        - hboobs
        """
      )
      
      await ctx.reply(embed=validEmbed)
    else:
      responseEmbed = Embed(
        url = data["message"],
        title=f"<:NSFW:962289749954027571> {type.capitalize()}",
        color = 0xffffff,
        timestamp = datetime.now()
      )

      url = data["message"]
        
      responseEmbed.set_image(url=url)
        
      responseEmbed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
        
      await ctx.send(embed = responseEmbed)

@bot.command()
async def guild(ctx):
  for i in bot.guilds:
    await ctx.send(f"Server ID: {i.id}\nServer Name: {i.name}\nMember Count: {i.member_count}\n\n")

@bot.command()
async def catgif(ctx):
  url = "https://api.thecatapi.com/v1/images/search?mime_types=gif"
  header = {
    "x-api-key": os.getenv("CAT_KEY")
  }
  response = requests.get(url, headers=header)
  data = json.loads(response.text)
  await ctx.send(data[0]["url"])

@bot.command()
async def dog(ctx):
  url = "https://dog.ceo/api/breeds/image/random"
  response = requests.get(url)
  data = json.loads(response.text)
  await ctx.send(data["message"])

@bot.command()
async def test(ctx):
  await ctx.send(getRandomSentences())

print(bot.cached_messages)


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
    f"{len(bot.guilds)} server's | b!help",
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