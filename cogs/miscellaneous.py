import textwrap
import discord
from discord.ext import commands
import io
import contextlib
from traceback import format_exception

from utils.utils import Pag, clean_code
from main import bot

class Miscellaneous(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def run(self, ctx, *, code):
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
                    f"async def func():\n{textwrap.indent(code, '    ')}", local_variables
                )

                obj = await local_variables["func"]()
                result = f"{stdout.getvalue()} \n-- {obj}\n"
        except Exception as e:
            result = "".join(format_exception(e, e, e.__traceback__))
        
        pager = Pag(
            timeout=100,
            entries=[result[i: i + 200] for i in range(0, len(result), 2000)],
            length=1,
            prefix="```py\n",
            suffix="```"
        )

        await pager.start(ctx)












def setup(bot):
    bot.add_cog(Miscellaneous(bot))