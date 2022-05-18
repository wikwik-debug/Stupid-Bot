import json
from pydoc import describe
import discord
from discord import Member, User, Embed
from discord.ext import commands
from discord.ext.commands import Context, Cog


import random
import aiohttp
import requests
import os

class Fun(Cog):

  def __init__(self, bot):
    self.bot = bot


  #The 8ball command
  @commands.command(name="8ball")
  async def _8ball(self, ctx, *, question):
    res = requests.get("https://nekos.life/api/v2/img/8ball")
    data = res.json()
    _8ballEmbed = Embed(
      title = "8ball",
      color = 0xffffff
    )
    
    _8ballEmbed.set_image(url=data["url"])
    
    await ctx.send(embed = _8ballEmbed)
    
    messageArr = []
    messageArr.append(question)
  
  #The meme command
  @commands.command()
  async def meme(self, ctx: Context):
    async with aiohttp.ClientSession() as session:
      # listOfUrls = ["https://www.reddit.com/r/memes/hot.json", "https://www.reddit.com/r/dankmemes/top.json?t=all"]
      
      # randomChoiceUrl = random.choice(listOfUrls)
      
      async with session.get("https://www.reddit.com/r/dankmemes/hot.json?t=all") as resp:
        data = await resp.json()
        print(data)
        data = data["data"]
        children = data["children"]
        post = random.choice(children)["data"]
        title = post["title"]
        url = post["url_overridden_by_dest"]

        memeEmbed = Embed(
          title = title
        )
        memeEmbed.set_image(url = url)

        await ctx.send(embed = memeEmbed)
  
  #The Konnichiwa Command (Wich send out a japanese word)
  @commands.command()
  async def konnichiwa(self, ctx):
    await ctx.send('Konnichiwa watashinonamaeha orokana bottodesu.')
  
  #The noob command
  @commands.command()
  async def noob(self, ctx):
    await ctx.send("https://cdn.discordapp.com/attachments/896429122920779778/903527338619306005/get_hangouts_attachment_url.png")
  
  #The user/member avatar command
  @commands.command(aliases = ["av", "pfp"])
  async def avatar(self, ctx, user: User = None):
  
    user = ctx.author if not user else user

    headers = {
      "Authorization": f"Bot {os.getenv('TOKEN')}"
    }

    res = requests.get(f"https://discord.com/api/v9/users/{user.id}", headers=headers)
    data = json.loads(res.text)
    
    pngLink = f"https://cdn.discordapp.com/avatars/{data['id']}/{data['avatar']}.png?size=1024"
    jpegLink = f"https://cdn.discordapp.com/avatars/{data['id']}/{data['avatar']}.jpeg?size=1024"
    gifLink = f"https://cdn.discordapp.com/avatars/{data['id']}/{data['avatar']}.gif?size=1024"
    webpLink = f"https://cdn.discordapp.com/avatars/{data['id']}/{data['avatar']}.webp?size=1024"
    
    if data["avatar"].startswith("a_"):
      description = f"[``PNG``]({pngLink}) [``JPEG``]({jpegLink}) [``WEBP``]({webpLink}) [``GIF``]({gifLink})"
    else:
      description = f"[``PNG``]({pngLink}) [``JPEG``]({jpegLink}) [``WEBP``]({webpLink})"

    if "bot" in data:
      url = ""
    else:
      url = f"https://discordapp.com/users/{data['id']}/"
    
    if data["banner_color"] is None:
      color = user.color
    else:
      color = int(data["banner_color"].replace("#", "0x"), 16)

    avatarEmbed = Embed(
      title = f"**{user.name}'s avatar**",
      description = description,
      color = color,
      timestamp = ctx.message.created_at,
      url = url
    )

    avatarEmbed.set_image(url=user.avatar_url)
    avatarEmbed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)

    await ctx.send(embed = avatarEmbed)

  #The user banner command
  @commands.command(name="banner")
  async def userBanner(self, ctx, user: User = None):
    user = ctx.author if not user else user
    
    header = {
      "Authorization": f"Bot {os.getenv('TOKEN')}"
    }

    res = requests.get(f"https://discord.com/api/v9/users/{user.id}", headers=header)
    data = json.loads(res.text)
    
    if data["banner"] is None:
      await ctx.send(f"{user.mention} doesnt have a banner")
    else:
      if data["banner"].startswith("a_"):
        bannerUrl = f"https://cdn.discordapp.com/banners/{data['id']}/{data['banner']}.gif?size=1024"
      else:
        bannerUrl = f"https://cdn.discordapp.com/banners/{data['id']}/{data['banner']}.jpeg?size=1024"
    
    if "bot" in data:
      url = ""
    else:
      url = f"https://discordapp.com/users/{data['id']}/"
    
    bannerEmbed = Embed(
      title = f"{user.display_name}'s banner",
      timestamp = ctx.message.created_at,
      url=url
    )

    bannerEmbed.set_image(url=bannerUrl)
    bannerEmbed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
    
    await ctx.send(embed=bannerEmbed)

  #The emojify command
  @commands.command()
  async def emojify(self, ctx, *, text):
    
    emojis = []
    
    for beans in text.lower():
      if beans.isdecimal():
        num2word = {
          "0": "zero",
          "1": "one",
          "2": "two",
          "3": "three",
          "4": "four",
          "5": "five",
          "6": "six",
          "7": "seven",
          "8": "eight",
          "9": "nine",
        }
        
        emojis.append(f":{num2word.get(beans)}:")
      
      elif beans.isalpha():
        emojis.append(f":regional_indicator_{beans}:")
      
      else:
        emojis.append(beans)
    
    await ctx.send(''.join(emojis))

  #The tweet command
  @commands.command()
  async def tweet(self, ctx, *, message, member: discord.Member = None):
    member = ctx.author if not member else member
    
    url = f"https://nekobot.xyz/api/imagegen?type=tweet&username={member.name}&text={message}"
      
    response = requests.get(url)
      
    data = json.loads(response.text)
      
    await ctx.send(data["message"])

  @commands.command()
  async def say(self, ctx, *, message):
    await ctx.send(message)
  
  #The dog command
  @commands.command()
  async def dog(self, ctx):
    url = "https://dog.ceo/api/breeds/image/random"
    response = requests.get(url)
    data = json.loads(response.text)
    await ctx.send(data["message"])
  
  #The catgif command
  @commands.command()
  async def catgif(self, ctx):
    url = "https://api.thecatapi.com/v1/images/search?mime_types=gif"
    header = {
      "x-api-key": os.getenv("CAT_KEY")
    }
    response = requests.get(url, headers=header)
    data = json.loads(response.text)
    await ctx.send(data[0]["url"])
  
  #the fact command
  @commands.command(aliases=["facts"])
  async def fact(self, ctx):
    res = requests.get("https://nekos.life/api/v2/fact")
    data = res.json()
    await ctx.reply(data["fact"])

  @commands.command()
  async def owoify(self, ctx, *, message:str):
    res = requests.get(f"https://nekos.life/api/v2/owoify?text={message}")
    data = res.json()
    await ctx.reply(data["owo"])

def setup(bot):
  bot.add_cog(Fun(bot))