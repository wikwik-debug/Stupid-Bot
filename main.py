import discord
from discord.ext import commands
from discord_slash import SlashCommand


import json
from time import time
from utils import Pag, clean_code
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

intents = discord.Intents.all()

load_dotenv()

token = os.getenv("TOKEN")
api_key = os.getenv("Api_key")


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

  message = await ctx.send("Done!")

  await message.delete()

#The run command
@bot.command(name="run", aliases=["exec", "eval"])
@commands.is_owner()
async def run(ctx, *, code):
    code = clean_code(code)

    local_variables = {
        "discord": discord,
        "commands": commands,
        "bot": bot,
        "ctx": ctx,
        "channel": ctx.channel,
        "author": ctx.author,
        "guild": ctx.guild,
        "message": ctx.message
    }

    stdout = io.StringIO()

    try:
        with contextlib.redirect_stdout(stdout):
            exec(
                f"async def func():\n{textwrap.indent(code, '    ')}", local_variables,
            )

            obj = await local_variables["func"]()
            result = f"{stdout.getvalue()}\n-- {obj}\n"
    except Exception as e:
        result = "".join(format_exception(e, e, e.__traceback__))

    pager = Pag(
        timeout=100,
        entries=[result[i: i + 2000] for i in range(0, len(result), 2000)],
        length=1,
        prefix="```py\n",
        suffix="```"
    )

    await pager.start(ctx)

class DurationConverter(commands.Converter):
  async def convert(self, ctx, argument):
    amount = argument[:-1]
    unit = argument[-1]

    if amount.isdigit() and unit in ["h", "m", "s"]:
      return (int(amount), unit)

#The mute command
@bot.command()
@commands.has_permissions(manage_messages = True)
async def mute(ctx, member:discord.Member, duration: DurationConverter, reason = None):

  role = discord.utils.get(ctx.guild.roles, name="Muted")
    
  guild = ctx.guild
      
  if role not in guild.roles:
      
    perms = discord.Permissions(send_messages=False, speak=False)
      
    await guild.create_role(name="Muted", permissions=perms)
      
    multiplier = {"h": 60 * 60, "m": 60, "s": 1}
    amount, unit = duration 

    await member.add_roles(role)

    embed = discord.Embed(
      description = f"<a:ApprovedCheckBox:901378101605445642> {member.mention} have been muted for {duration}",
      color = 0x44b582
      )

    await ctx.send(embed = embed)
    
    await asyncio.sleep(amount * multiplier[unit])
    
    await member.remove_roles(role)
    
  elif reason == None:
    return await ctx.message.add_reaction("<a:DeniedBox:882782174208749608>")
    
  else:
      multiplier = {"h": 60 * 60, "m": 60, "s": 1}
      amount, unit = duration 
        
      await member.add_roles(role)
          
      embed2 = discord.Embed(
        description = f"<a:ApprovedCheckBox:901378101605445642> {member.mention} have been muted",
        color = 0x44b582
        )
      await ctx.send(embed = embed2)
      
      await asyncio.sleep(amount * multiplier[unit])
      
      await member.remove_roles(role)

#The numberinfo command
@bot.command(aliases = ["ni"])
async def numberinfo(ctx, nomer):

    number = phonenumbers.parse(nomer)

    colour = discord.Colour

    valid_number = "Yes" if phonenumbers.is_valid_number(number) else "No"

    description = f"""
    **- The carrier's number:** ``{carrier.name_for_number(number, "en")}``
    **- The number's region:** ``{geocoder.description_for_number(number, "en")}``
    **- Number's timezone:** ``{timezone.time_zones_for_number(number)}``
    **- Valid phone number:** ``{valid_number}``
    """

    numEmbed = discord.Embed(
        title = f"Phone number information for: `{phonenumbers.format_number(number, phonenumbers.PhoneNumberFormat.NATIONAL)}`",
        description = description,
        color = colour.random()
    )

    numEmbed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/900644202453549076/908989593876054016/Goblok.png")

    await ctx.send(embed = numEmbed)

#The weather command
@bot.command()
async def weather(ctx, *, location):

  url = f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=imperial"
  data = json.loads(requests.get(url).content)
  data = parse_data(data)
    
  aliases = {
    'temp': 'Temperature',
    'temp_max': "Maximum Temperature",
    "temp_min": "Minimum Temperature",
    "feels_like": "Feels like",
    "sea_level": "Sea level",
    "grnd_level": "Ground level"
    }
    
  colour = discord.Colour
    
  location = location.title()
        
  weatherEmbed = discord.Embed(
    title = f"{location} weather",
    description = f"Here is the data for {location}.",
    colour = colour.random()
  )

  for key in data:
    weatherEmbed.add_field(name = aliases[key], value = str(data[key]), inline = False)
        
  await ctx.send(embed = weatherEmbed)

@bot.command()
async def salatiga(ctx):
  await ctx.send("It is my dev's hometown")

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

@bot.command()
async def load(ctx, extension):
  bot.load_extension(f"cogs.{extension}")
  await ctx.send(f"The ``{extension}`` cogs have been successfully loaded")

@bot.command()
async def unload(ctx, extension):
  bot.unload_extension(f"cogs.{extension}")
  await ctx.send(f"The ``{extension}`` cogs have been successfully unloaded")

for filename in os.listdir("./cogs"):
  if filename.endswith(".py"):
    bot.load_extension(f"cogs.{filename[:-3]}")




bot.loop.create_task(ch_pr())
bot.run(token)