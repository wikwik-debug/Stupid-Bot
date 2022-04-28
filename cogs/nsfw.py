from discord import Embed
from discord.ext import commands

import requests
import json
from datetime import datetime
import asyncio

class Nsfw(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def pussy(self, ctx):
        url = "https://nekobot.xyz/api/image?type=pussy"
        response = requests.get(url)
        data = json.loads(response.text)
        resEmbed = Embed(
            url=data["message"],
            title="<:NSFW:962289749954027571> Pussy",
            color = 0xffffff,
            timestamp = datetime.utcnow()
        )
        
        if ctx.channel.nsfw == True:
            imageUrl = data["message"]
            resEmbed.set_image(url=imageUrl)
            resEmbed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
            await ctx.send(embed = resEmbed)
        else:
            message = await ctx.reply(f"You cant execute this command here because {ctx.channel.mention} is not a NSFW channel")
            await asyncio.sleep(7)
            await message.edit(content="My Solution:  `Create a NSFW channel, duh`")

    @commands.command()
    async def boobs(self, ctx):
        url = "https://nekobot.xyz/api/image?type=boobs"
        response = requests.get(url)
        data = json.loads(response.text)
        resEmbed = Embed(
            url=data["message"],
            title="<:NSFW:962289749954027571> Boobs",
            color = 0xffffff,
            timestamp = datetime.utcnow()
        )
        if ctx.channel.nsfw == True:
            imageUrl = data["message"]
            resEmbed.set_image(url=imageUrl)
            resEmbed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
            await ctx.send(embed = resEmbed)
        else:
            message = await ctx.reply(f"You cant execute this command here because {ctx.channel.mention} is not a NSFW channel")
            await asyncio.sleep(7)
            await message.edit(content="My Solution:  `Create a NSFW channel, duh`")

    @commands.command()
    async def ass(self, ctx):
        url = "https://nekobot.xyz/api/image?type=ass"
        response = requests.get(url)
        data = json.loads(response.text)
        resEmbed = Embed(
            url=data["message"],
            title="<:NSFW:962289749954027571> Ass",
            color = 0xffffff,
            timestamp = datetime.utcnow()
        )
        if ctx.channel.nsfw == True:
            imageUrl = data["message"]
            resEmbed.set_image(url=imageUrl)
            resEmbed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
            await ctx.send(embed = resEmbed)
        else:
            message = await ctx.reply(f"You cant execute this command here because {ctx.channel.mention} is not a NSFW channel")
            await asyncio.sleep(7)
            await message.edit(content="My Solution:  `Create a NSFW channel, duh`")

    @commands.command(name="4k")
    async def four_k(self, ctx):
        url = "https://nekobot.xyz/api/image?type=4k"
        response = requests.get(url)
        data = json.loads(response.text)
        resEmbed = Embed(
            url=data["message"],
            title="<:NSFW:962289749954027571> 4k",
            color = 0xffffff,
            timestamp = datetime.utcnow()
        )
        if ctx.channel.nsfw == True:
            imageUrl = data["message"]
            resEmbed.set_image(url=imageUrl)
            resEmbed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
            await ctx.send(embed = resEmbed)
        else:
            message = await ctx.reply(f"You cant execute this command here because {ctx.channel.mention} is not a NSFW channel")
            await asyncio.sleep(7)
            await message.edit(content="My Solution:  `Create a NSFW channel, duh`")

    @commands.command()
    async def hentai(self, ctx):
        url = "https://nekobot.xyz/api/image?type=hentai"
        response = requests.get(url)
        data = json.loads(response.text)
        resEmbed = Embed(
            url=data["message"],
            title="<:NSFW:962289749954027571> Hentai",
            color = 0xffffff,
            timestamp = datetime.utcnow()
        )
        if ctx.channel.nsfw == True:
            imageUrl = data["message"]
            resEmbed.set_image(url=imageUrl)
            resEmbed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
            await ctx.send(embed = resEmbed)
        else:
            message = await ctx.reply(f"You cant execute this command here because {ctx.channel.mention} is not a NSFW channel")
            await asyncio.sleep(7)
            await message.edit(content="My Solution:  `Create a NSFW channel, duh`")

    @commands.command()
    async def anal(self, ctx):
        url = "https://nekobot.xyz/api/image?type=anal"
        response = requests.get(url)
        data = json.loads(response.text)
        resEmbed = Embed(
            url=data["message"],
            title="<:NSFW:962289749954027571> Anal",
            color = 0xffffff,
            timestamp = datetime.utcnow()
        )
        if ctx.channel.nsfw == True:
            imageUrl = data["message"]
            resEmbed.set_image(url=imageUrl)
            resEmbed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
            await ctx.send(embed = resEmbed)
        else:
            message = await ctx.reply(f"You cant execute this command here because {ctx.channel.mention} is not a NSFW channel")
            await asyncio.sleep(7)
            await message.edit(content="My Solution:  `Create a NSFW channel, duh`")

    @commands.command()
    async def gonewild(self, ctx):
        url = "https://nekobot.xyz/api/image?type=gonewild"
        response = requests.get(url)
        data = json.loads(response.text)
        resEmbed = Embed(
            url=data["message"],
            title="<:NSFW:962289749954027571> Gonewild",
            color = 0xffffff,
            timestamp = datetime.utcnow()
        )
        if ctx.channel.nsfw == True:
            imageUrl = data["message"]
            resEmbed.set_image(url=imageUrl)
            resEmbed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
            await ctx.send(embed = resEmbed)
        else:
            message = await ctx.reply(f"You cant execute this command here because {ctx.channel.mention} is not a NSFW channel")
            await asyncio.sleep(7)
            await message.edit(content="My Solution:  `Create a NSFW channel, duh`")

    @commands.command()
    async def paizuri(self, ctx):
        url = "https://nekobot.xyz/api/image?type=paizuri"
        response = requests.get(url)
        data = json.loads(response.text)
        resEmbed = Embed(
            url=data["message"],
            title="<:NSFW:962289749954027571> Paizuri",
            color = 0xffffff,
            timestamp = datetime.utcnow()
        )
        if ctx.channel.nsfw == True:
            imageUrl = data["message"]
            resEmbed.set_image(url=imageUrl)
            resEmbed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
            await ctx.send(embed = resEmbed)
        else:
            message = await ctx.reply(f"You cant execute this command here because {ctx.channel.mention} is not a NSFW channel")
            await asyncio.sleep(7)
            await message.edit(content="My Solution:  `Create a NSFW channel, duh`")

    @commands.command()
    async def thigh(self, ctx):
        url = "https://nekobot.xyz/api/image?type=thigh"
        response = requests.get(url)
        data = json.loads(response.text)
        resEmbed = Embed(
            url=data["message"],
            title="<:NSFW:962289749954027571> Thigh",
            color = 0xffffff,
            timestamp = datetime.utcnow()
        )
        if ctx.channel.nsfw == True:
            imageUrl = data["message"]
            resEmbed.set_image(url=imageUrl)
            resEmbed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
            await ctx.send(embed = resEmbed)
        else:
            message = await ctx.reply(f"You cant execute this command here because {ctx.channel.mention} is not a NSFW channel")
            await asyncio.sleep(7)
            await message.edit(content="My Solution:  `Create a NSFW channel, duh`")

def setup(bot):
    bot.add_cog(Nsfw(bot))