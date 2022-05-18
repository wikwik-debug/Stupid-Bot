import asyncio
from discord import Embed, AuditLogAction
from discord.ext import commands
from discord.ext.commands import Cog
from discord.utils import find

import json
import requests

class Events(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        print("Bot is ready!")

    @Cog.listener()
    async def on_message(self, message):
        mentionForPC = f'<@!{self.bot.user.id}>'
        mentionForMobile = f"<@881735007893336084>"

        if message.content == mentionForPC:
            with open('prefixes.json', 'r') as f1:
                prefixes = json.load(f1) 
        
            serverPrefix = prefixes[f"{str(message.guild.name)}({str(message.guild.id)})"]
        
            await message.channel.send(f"My prefix for this server is `{serverPrefix}`")
        
        # For mobile compatibility
        elif message.content == mentionForMobile:
            with open('prefixes.json', 'r') as f2:
                prefixes = json.load(f2) 
        
            serverPrefix = prefixes[f"{str(message.guild.name)}({str(message.guild.id)})"]
        
            await message.channel.send(f"My prefix for this server is `{serverPrefix}`")
    
        elif message.content == "Noob":
            await message.reply("Your the only noob on this planet")
    
        mentionHelpForPC = f'<@{self.bot.user.id}> help'
        mentionHelpForMobile = f'<@!881735007893336084> help'

        if message.content == mentionHelpForPC:
            embed1 = Embed(title = "My list of commands", colour = 0xffffff)
            embed1.add_field(name = "Moderation Commands", value = "``ban`` ``unban`` ``kick`` ``slowmode`` ``nickname`` ``mute`` ``unmute`` ``purge`` ``lock`` ``unlock`` ``channelban``", inline = False)
            embed1.add_field(name = "Info Commands", value = "``whois`` ``serverinfo`` ``botinfo`` ``covid`` ``emojiinfo`` ``numberinfo``", inline = False)
            embed1.add_field(name = "Fun Commands", value = "``8ball`` ``avatar`` ``Konnichiwa`` ``meme`` ``emojify`` ``say`` ``catgif`` ``tweet`` ``fact`` ``owoify``", inline = False)
            embed1.add_field(name = "Utilities Commands", value = "``changeprefix`` ``addrole`` ``removerole`` ``toggle`` ``whoadd``", inline = False)
            embed1.add_field(name = "Miscellaneous Commands", value = "``run``", inline = False)
            await message.channel.send(embed = embed1)
        
        # For mobile compatibility
        elif message.content == mentionHelpForMobile:
            embed2 = Embed(title = "My list of commands", colour = 0xffffff)
            embed2.add_field(name = "Moderation Commands", value = "``ban``\n ``unban``\n ``kick``\n ``slowmode``\n ``nickname``\n ``mute``\n ``unmute``\n ``purge``\n ``lock``\n ``unlock``\n ``channelban``", inline = True)
            embed2.add_field(name = "Info Commands", value = "``whois``\n ``serverinfo``\n ``botinfo``\n ``covid``\n ``emojiinfo``\n ``numberinfo``", inline = False)
            embed2.add_field(name = "Fun Commands", value = "``8ball``\n ``avatar``\n ``Konnichiwa``\n ``meme``\n ``emojify``\n ``say``\n ``catgif``\n ``tweet``\n ``fact``\n ``owoify``", inline = False)
            embed2.add_field(name = "Utilities Commands", value = "``changeprefix``\n ``addrole``\n ``removerole``\n ``toggle``\n ``whoadd``", inline = False)
            embed2.add_field(name = "Miscellaneous Commands", value = "``run``", inline = False)
            await message.channel.send(embed = embed2)

    @Cog.listener()
    async def on_command_error(self, ctx, error) -> None:
        if isinstance(error, commands.MissingPermissions):
            await ctx.message.add_reaction("<a:DeniedBox:882782174208749608>")
    
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.message.add_reaction("<a:DeniedBox:882782174208749608>")
        
        elif isinstance(error, commands.CommandNotFound):
            await ctx.reply("Invalid command <a:DeniedBox:882782174208749608>")
        
        elif isinstance(error, commands.DisabledCommand):
            await ctx.reply("That command is disabled")

    @Cog.listener()
    async def on_guild_join(self, guild):
        with open("prefixes.json", "r") as f:
            prefixes = json.load(f)

        prefixes[f"{str(guild.name)}({str(guild.id)})"] = "sb!"

        with open("prefixes.json", "w") as f:
            json.dump(prefixes, f, indent = 4)
        
        post_url = "http://localhost:5000/utils/addNewPrefix"
        payload = {
            "serverID": guild.id,
            "serverName": guild.name
        }
        res = requests.post(post_url, json=payload)
        print(res.status_code)

        async for entries in guild.audit_logs(limit=1, action=AuditLogAction.bot_add):
            general = find(lambda x : x.name == 'general',  guild.text_channels)
            chat = find(lambda x : x.name == "chat", guild.text_channels)

            if entries.target.id == 881735007893336084:
                if general and general.permissions_for(guild.me).send_messages:
                    await general.send(f"Thank you for inviting me! {entries.user.mention}")

                elif chat and chat.permissions_for(guild.me).send_messages:
                    await chat.send(f"Thank you for inviting me! {entries.user.mention}")

    @Cog.listener()
    async def on_guild_remove(self, guild):
        with open("prefixes.json", "r") as f:
            prefixes = json.load(f)

        prefixes.pop(f"{str(guild.name)}({str(guild.id)})")

        with open("prefixes.json", "w") as f:
            json.dump(prefixes, f, indent = 4)

def setup(bot):
    bot.add_cog(Events(bot))