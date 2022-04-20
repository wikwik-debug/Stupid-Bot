import discord
from discord.ext import commands

class Nsfw(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def pussy(self, ctx):
        url = "https://nekobot.xyz/api/image?type=pussy"
    

def setup(bot):
    bot.add_cog(Nsfw(bot))