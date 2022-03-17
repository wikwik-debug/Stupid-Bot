from discord.ext import commands
from discord import Embed

import requests
from colour import Color
import asyncio

class Api(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.cooldown(1, 30, commands.BucketType.user)
    @commands.command(aliases = ["ud"])
    async def userID(self, ctx, *, username):
        url = "https://instagram47.p.rapidapi.com/get_user_id"

        querystring = {"username":f"{username}"}

        headers = {
            'x-rapidapi-host': "instagram47.p.rapidapi.com",
            'x-rapidapi-key': "9f35c1fc25msh39b4a7825015512p1df884jsn6005f4bfce74"
        }

        response = requests.request("GET", url, headers=headers, params=querystring)
        responseJSON = response.json()

        description = f"""
        **Username:** @{responseJSON["username"]}
        **User ID:** {responseJSON["user_id"]}
        """

        # colour = discord.Colour
        red = Color("red")
        colors = list(red.range_to(Color("green"),10))

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