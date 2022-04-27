from pydoc import describe
import discord
from discord import TextChannel, User, Embed, Guild, PermissionOverwrite, Member, Permissions, AuditLogAction
from discord.ext import commands
from discord.ext.commands import MemberConverter
from discord.utils import get

import asyncio

class Moderation(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  #The kick command
  @commands.command(case_insensitive = True)
  @commands.has_permissions(kick_members = True)
  async def kick(self, ctx, member : Member, *, reason=None):
    if reason is None:
      await ctx.reply("Please provide a reason")
    else:
      try:
        kickEmbed = Embed(
          description = f"You have been kicked from ``{ctx.guild.name}``\nReason: {reason}",
          color = 0xff0000
        )
        
        await member.send(embed = kickEmbed)
      except:
        await ctx.send("cant send a DM to the user")
        # print("cant send a DM to the user")
      else:
        await member.kick(reason=reason)
        await ctx.message.add_reaction("<a:ApprovedCheckBox:882777440609521724>")

  #The ban command
  @commands.command()
  @commands.has_permissions(ban_members = True)
  async def ban(self, ctx, member : MemberConverter, *, reason=None):
    if member == ctx.author:
      await ctx.send("You cannot ban yourself")
    elif reason is None:
      await ctx.reply("Please provide a reason to ban")
    else:
      await member.ban(reason=reason)
      await ctx.message.add_reaction("<a:ApprovedCheckBox:882777440609521724>")

  #The unban command
  @commands.command()
  @commands.has_permissions(ban_members = True)
  async def unban(self, ctx, user: User):
    bannedUser = await self.bot.fetch_user(user.id)
    await ctx.guild.unban(bannedUser)
    await ctx.message.add_reaction("<a:ApprovedCheckBox:882777440609521724>")
  
  #The clear command
  @commands.command()
  @commands.has_permissions(manage_messages = True)
  async def clear(self, ctx, amount: int):
    await ctx.channel.purge(limit = amount)
  
  #The nickname command
  @commands.command(aliases = ["changeNick"])
  @commands.has_permissions(manage_nicknames = True)
  async def nickname(self, ctx, member:MemberConverter, *, nick = None):
    # await member.edit(nick=nick)
    # guild = ctx.guild
    
    # async for entries in guild.audit_logs(action=AuditLogAction.member_update):
    #   if nick is None:
    #     await member.edit(nick=None)
    #     await ctx.send(f"Nickname changed back to ``{entries.target.name}``")
    #     return
    #   else:
    #       if entries.target.id == member.id:
    #         if entries.changes.before.nick is None:
    #           await ctx.send(f'Nickname changed from ``{entries.target.name}`` to ``{entries.changes.after.nick}`` ')
    #         else:
    #           await ctx.send(f'Nickname changed from ``{entries.changes.before.nick}`` to ``{entries.changes.after.nick}`` ')
    #         return
    
    oldNickname = member.display_name
    await member.edit(nick=nick)
    newNickname = member.display_name
    await ctx.send(f"Nickname changed from ``{oldNickname}`` to ``{newNickname}``")

  class DurationConverter(commands.Converter):
    async def convert(self, ctx, args):
      amount = args[:-1]
      unit = args[-1]
      unitArr = ["d", "h", "m", "s"]

      if amount.isdigit() and unit in unitArr:
        return (int(amount), unit)

  # The mute command
  @commands.command()
  @commands.has_permissions(manage_messages = True)
  async def mute(self, ctx, member:Member, duration: DurationConverter, reason = None):
    role = get(ctx.guild.roles, name="Muted")
    guild = ctx.guild

    if role not in guild.roles:
      perms = Permissions(send_messages=False, speak=False)
      
      await guild.create_role(name="Muted", permissions=perms)
        
      multiplierDict1 = {"d": 86400, "h": 3600, "m": 60, "s": 1}
      amount, unit = duration

      await member.add_roles(role)

      if unit == "s":
        embed = Embed(
          description = f"<a:ApprovedCheckBox:901378101605445642> {member.mention} have been muted for ``{amount} Seconds``",
          color = 0x44b582
        )
        await ctx.send(embed = embed)
      
      elif unit == "m":
        embed = Embed(
          description = f"<a:ApprovedCheckBox:901378101605445642> {member.mention} have been muted for ``{amount} Minutes``",
          color = 0x44b582
        )
        await ctx.send(embed = embed)
      
      elif unit == "h":
        embed = Embed(
          description = f"<a:ApprovedCheckBox:901378101605445642> {member.mention} have been muted for ``{amount} Hours``",
          color = 0x44b582
        )
        await ctx.send(embed = embed)
      
      elif unit == "d":
        embed = Embed(
          description = f"<a:ApprovedCheckBox:901378101605445642> {member.mention} have been muted for ``{amount} Day``",
          color = 0x44b582
        )
        await ctx.send(embed = embed)
        
        if (amount, unit) == "1d":
          embed = Embed(
            description = f"<a:ApprovedCheckBox:901378101605445642> {member.mention} have been muted for ``a Day``",
            color = 0x44b582
          )
          await ctx.send(embed = embed)
      
      await asyncio.sleep(amount * multiplierDict1[unit])
      
      await member.remove_roles(role)
    
    elif reason is None:
      await ctx.message.add_reaction("<a:DeniedBox:882782174208749608>")
    
    elif role in member.roles:
      errorEmbed = Embed(
        description = f"<a:DeniedBox:882782174208749608> {member.mention} is already muted",
        color = 0xff0000
      )
      await ctx.reply(embed = errorEmbed)
    
    else:
      multiplierDict2 = {"d": 86400, "h": 3600, "m": 60, "s": 1}
      amount, unit = duration 
        
      await member.add_roles(role)

      if unit == "s":
        embed2 = Embed(
          description = f"<a:ApprovedCheckBox:901378101605445642> {member.mention} have been muted for ``{amount} Seconds```",
          color = 0x44b582
        )
        await ctx.send(embed = embed2)
      
      elif unit == "m":
        embed2 = Embed(
          description = f"<a:ApprovedCheckBox:901378101605445642> {member.mention} have been muted for ``{amount} Minutes``",
          color = 0x44b582
        )
        await ctx.send(embed = embed2)
      
      elif unit == "h":
        embed2 = Embed(
          description = f"<a:ApprovedCheckBox:901378101605445642> {member.mention} have been muted for ``{amount} Hours``",
          color = 0x44b582
        )
        await ctx.send(embed = embed2)

      elif unit == "d":
        embed2 = Embed(
          description = f"<a:ApprovedCheckBox:901378101605445642> {member.mention} have been muted for ``{amount} Day``",
          color = 0x44b582
        )
        await ctx.send(embed = embed2)

      await asyncio.sleep(amount *  multiplierDict2[unit])
      
      await member.remove_roles(role)


  #The unmute command
  @commands.command()
  @commands.has_permissions(manage_messages = True)
  async def unmute(self, ctx, member:Member):
    role = discord.utils.get(ctx.guild.roles, name="Muted")

    if role not in member.roles:
      roleErrorEmbed = Embed(
        description = f"<a:DeniedBox:882782174208749608> {member.mention} haven't been muted",
        color = 0xff0000
      )
      await ctx.reply(embed = roleErrorEmbed)
    else:
      roleEmbed = Embed(
        description = f"<a:ApprovedCheckBox:901378101605445642> {member.mention} have been unmuted",
        color = 0x44b582
      )
      await member.remove_roles(role)
      await ctx.send(embed = roleEmbed)

  #The slowmode command
  @commands.command()
  @commands.has_permissions(manage_channels = True)
  async def slowmode(self, ctx, seconds:str = None):
    if seconds == "reset":
      await ctx.channel.edit(slowmode_delay=0)
      await ctx.send("The slomode have been turned off")
    elif seconds is None:
      await ctx.reply("Please specify a value to slowmode")
    else:
      if isinstance(seconds, str):
        seconds = int(seconds)

      await ctx.channel.edit(slowmode_delay=seconds)
      await ctx.send(f'The slowmode have been set to ``{seconds}`` seconds')

  #The lock commmand
  @commands.command()
  @commands.has_permissions(manage_channels = True)
  async def lock(self, ctx, channelName: TextChannel = None):
    channel = ctx.channel if channelName is None else await self.bot.fetch_channel(channelName.id)

    defaultRole = ctx.guild.default_role
    
    overwrite = PermissionOverwrite()
    
    overwrite.send_messages = False
    overwrite.use_slash_commands = False

    await channel.set_permissions(defaultRole, overwrite=overwrite)

    await ctx.send(f"{channel.mention} have been successfully locked")
    
  
  #The unlock command
  @commands.command()
  @commands.has_permissions(manage_channels = True)
  async def unlock(self, ctx, channelName: TextChannel = None):

    channel = ctx.channel if channelName is None else await self.bot.fetch_channel(channelName.id)
    
    defaultRole = ctx.guild.default_role

    overwrite = PermissionOverwrite()
    
    overwrite.send_messages = True
    
    await channel.set_permissions(defaultRole, overwrite=overwrite)
    
    
    await ctx.send(f"{channel.mention} have been successfully unlocked")
  
  #The channelban command
  @commands.command(aliases = ["cb"])
  @commands.has_permissions(ban_members = True)
  async def channelban(self, ctx, member: discord.Member, reason = None):
    
    overwrite = PermissionOverwrite()
    
    overwrite.view_channel = False
    
    if reason is None:
      return await ctx.reply("Please provide a reason")
    
    await ctx.channel.set_permissions(member, overwrite=overwrite)
    
    await ctx.send(f"{member.mention} have been banned from this channel")
  
  @commands.command()
  async def random(self, ctx):
    colour = discord.Colour
    var = "Hello!"
    randomEmbed = Embed(
      title = "random",
      description = f"<a:ApprovedCheckBox:901378101605445642> {ctx.author.mention} This is random ``{var}``",
      color = colour.random()
    )
    
    await ctx.send(embed = randomEmbed)
  
  #The globalkick command (Owner commands only!)
  @commands.command()
  @commands.is_owner()
  async def globalkick(self, ctx, guild: Guild, user: User, *, reason = None):
    fetchedGuild = await self.bot.fetch_guild(guild.id)
    appinfo = await self.bot.application_info()
    
    if reason is None:
      await ctx.reply("Please provide a reason to kick")
    elif ctx.author != appinfo.owner:
      await ctx.reply("You cant execute this command because your not the owner of the bot")
    else:
      await fetchedGuild.kick(user, reason=reason)
      await ctx.send(f"Successfully kicked {user.mention} from `{guild.name}`")




def setup(bot):
  bot.add_cog(Moderation(bot))