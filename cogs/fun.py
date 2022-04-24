import json
from pydoc import describe
import discord
from discord import Member, User, Embed
from discord.ext import commands

import random
import aiohttp
import requests
import os

class Fun(commands.Cog):

  def __init__(self, bot):
    self.bot = bot

  #The 8ball command
  @commands.command(name="8ball")
  async def _8ball(self, ctx, *, question):
    responses = [ "As I see it, yes.",
                "Oh hell yes.",
                "Ask again later.",
                "Better not tell you now.",
                "Cannot predict now.",
                "Concentrate and ask again.",
                "Don’t count on it.",
                "It is certain.",
                "It is decidedly so.", 
                "Most likely.",
                "My reply is no.",
                "My sources say no.",
                "Outlook not so good.",
                "Outlook good.",
                "Reply hazy, try again.",
                "Signs point to yes.",
                "Very doubtful.",
                "Oh hell no.",
                "Without a doubt.",
                "Yes.", 
                "Yes – definitely.",
                "You may rely on it."]
    await ctx.reply(f"{random.choice(responses)}")
  
  #The meme command
  @commands.command()
  async def meme(self, ctx: commands.Context):
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

    header = {
      "Authorization": f"Bot {os.getenv('TOKEN')}"
    }

    res = requests.get(f"https://discord.com/api/v9/users/{user.id}", headers=header)
    data = json.loads(res.text)
    pngLink = f"https://cdn.discordapp.com/avatars/{data['id']}/{data['avatar']}.png"
    jpegLink = f"https://cdn.discordapp.com/avatars/{data['id']}/{data['avatar']}.jpeg"
    gifLink = f"https://cdn.discordapp.com/avatars/{data['id']}/{data['avatar']}.gif"
    webpLink = f"https://cdn.discordapp.com/avatars/{data['id']}/{data['avatar']}.webp"
    
    if data["avatar"].startswith("a_"):
      description = f"[``PNG``]({pngLink}) [``JPEG``]({jpegLink}) [``WEBP``]({webpLink}) [``GIF``]({gifLink})"
    else:
      description = f"[``PNG``]({pngLink}) [``JPEG``]({jpegLink}) [``WEBP``]({webpLink})"

    avatarEmbed = Embed(
      title = f"**{user.name}'s avatar**",
      description=description,
      color = user.colour,
      timestamp = ctx.message.created_at,
      url=f"https://discordapp.com/users/{data['id']}/"
    )

    avatarEmbed.set_image(url=user.avatar_url)
    avatarEmbed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)

    await ctx.send(embed = avatarEmbed)

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
  
  @commands.command()
  async def dog(self, ctx):
    url = "https://dog.ceo/api/breeds/image/random"
    response = requests.get(url)
    data = json.loads(response.text)
    await ctx.send(data["message"])
  
  @commands.command()
  async def catgif(self, ctx):
    url = "https://api.thecatapi.com/v1/images/search?mime_types=gif"
    header = {
      "x-api-key": os.getenv("CAT_KEY")
    }
    response = requests.get(url, headers=header)
    data = json.loads(response.text)
    await ctx.send(data[0]["url"])

def setup(bot):
  bot.add_cog(Fun(bot))