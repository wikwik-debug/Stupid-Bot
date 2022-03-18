from discord.ext import commands
from discord import Embed

import requests
import asyncio
from dotenv import load_dotenv
import os
import json



class Api(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.cooldown(1, 30, commands.BucketType.user)
    @commands.command(aliases = ["ud"])
    async def userID(self, ctx, *, username):
        
        with open("apiCogsConfig.json", "r") as file:
            apiConfig = json.load(file)

        querystring = {"username":f"{username}"}

        headers = {
            'x-rapidapi-host': f"{apiConfig['1']}",
            'x-rapidapi-key': f"{os.getenv('INSTAGRAM_KEY')}"
        }

        response = requests.request("GET", apiConfig["0"], headers=headers, params=querystring)
        responseJSON = response.json()

        description = f"""
        **Username:** @{responseJSON["username"]}
        **User ID:** {responseJSON["user_id"]}
        """

        # colour = discord.Colour
        
        userIdInstragramEmbed = Embed(
            title = "Instragram User ID",
            description = description,
            color = 0x5851D8
        )

        await ctx.send(embed = userIdInstragramEmbed)
    
    @userID.error
    async def userID_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            message = await ctx.send("Slow it down, bruh. Youre in cooldown!")
            await asyncio.sleep(2.5)
            await message.edit(content=f"Try again in ``{round(error.retry_after)}s``")
        
        

def setup(bot):
  bot.add_cog(Api(bot))