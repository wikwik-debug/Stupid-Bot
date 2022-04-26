import discord
from discord import User, AppInfo
from discord.ext import commands
import asyncio
from time import time


class Bot(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  #The ping command
  @commands.command()
  async def ping(self, ctx):
    start = time()
    message = await ctx.send(f"API latency: ``{self.bot.latency * 1000:,.0f}ms``")
    end = time()

    await message.edit(content = f"API latency: ``{self.bot.latency * 1000:,.0f}ms``\nResponse time: ``{(end-start)*1000:,.0f}ms``")

  
  #The botinfo command
  @commands.command(aliases = ["bot", "bi"])
  async def botinfo(self, ctx):
    appinfo = await self.bot.application_info()
    
    botInfoEmbed = discord.Embed(
      color = 0xffffff
    )
    botInfoEmbed.set_author(name= "Stupid Bot", icon_url=appinfo.icon_url)
    # https://cdn.discordapp.com/avatars/881735007893336084/83080f50240798459dfc45a6b60ab746.png?size=128
    botInfoEmbed.add_field(name = "Version <a:Info:903501224014385192>", value = "1.0.0")
    botInfoEmbed.add_field(name = "Libary <:Python:903496492256473118>", value = "Discord.py")
    botInfoEmbed.add_field(name = "Creator <:Bot_owner:903494195975684127> <:Bot_dev:903502947290333245>", value = appinfo.owner)
    botInfoEmbed.add_field(name = "Servers <:Servers:903501984273932298>", value= len(self.bot.guilds))
    botInfoEmbed.add_field(name = "Users <:Person:903497301828444181>", value = len(self.bot.users))
    botInfoEmbed.add_field(name = "Invite link ✉", value="https://dsc.gg/stupid-bot")
    botInfoEmbed.add_field(name = "This bot was created at:", value = f'{self.bot.user.created_at.strftime("%A, %d %B %Y  %H:%M %p %Z")} (<t:1630335607:R>)', inline=False)

    await ctx.send(embed = botInfoEmbed)

  #The bot source code command
  @commands.command()
  async def source(self, ctx):
    await ctx.send("https://github.com/wikwik-debug/Stupid-Bot")

def setup(bot):
  bot.add_cog(Bot(bot))