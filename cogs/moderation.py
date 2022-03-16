import discord
from discord import User
from discord.ext import commands
import asyncio

class Moderation(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  #The kick command
  @commands.command(case_insective = True)
  @commands.has_permissions(kick_members = True)
  async def kick(self, ctx, member : discord.Member, *, reason=None):
    embed = discord.Embed(
      description = f"You have been kicked from {ctx.guild.name}",
      color = 0xff0000
    )

    await member.send(embed = embed)
  
    await member.kick(reason=reason)
  
    await ctx.message.add_reaction("<a:ApprovedCheckBox:882777440609521724>")
  
  #The ban command
  @commands.command()
  @commands.has_permissions(ban_members = True)
  async def ban(self, ctx, member : commands.MemberConverter, *, reason=None):
    await member.ban(reason=reason)
    await ctx.message.add_reaction("<a:ApprovedCheckBox:882777440609521724>")

  #The unban command
  @commands.command()
  @commands.has_permissions(ban_members = True)
  async def unban(self, ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')
  
    for ban_entry in banned_users:
      user = ban_entry.user

      if (user.name, user.discriminator) == (member_name, member_discriminator):
        await ctx.guild.unban(user)
        await ctx.message.add_reaction("")
        return
  
  #The clear command
  @commands.command()
  @commands.has_permissions(manage_messages = True)
  async def clear(self, ctx, amount: int):
    
    await ctx.channel.purge(limit = amount)
  
  #The nickname command
  @commands.command(pass_content=False, aliases = ["changeNick"])
  @commands.has_permissions(manage_nicknames = True)
  async def nickname(self, ctx, member: discord.Member, *, nick):
    await member.edit(nick=nick)
    await ctx.send(f'Nickname was changed for {member.mention} ')
  
  class DurationConverter(commands.Converter):
    async def convert(self, ctx, argument):
      amount = argument[:-1]
      unit = argument[-1]

      if amount.isdigit() and unit in ["h", "m", "s"]:
        return (int(amount), unit)
  
  #The mute command
  @commands.command()
  @commands.has_permissions(manage_messages = True)
  async def mute(self, ctx, member:discord.Member, duration: DurationConverter, reason = None):
    role = discord.utils.get(ctx.guild.roles, name="Muted")
    guild = ctx.guild


    if role not in guild.roles:
      perms = discord.Permissions(send_messages=False, speak=False)
      
      await guild.create_role(name="Muted", permissions=perms)
        
      multiplier = {"h": 60 * 60, "m": 60, "s": 1}
      amount, unit = duration 

      await member.add_roles(role)

      embed = discord.Embed(
        description = f"<a:ApprovedCheckBox:901378101605445642> {member.mention} have been muted for {duration}",
        color = 0x44b582
      )

      await ctx.send(embed = embed)
      
      await asyncio.sleep(amount * multiplier[unit])
      
      await member.remove_roles(role)
    
    elif reason == None:
      await ctx.message.add_reaction("<a:DeniedBox:882782174208749608>") 
    
    else:
      multiplier = {"h": 60 * 60, "m": 60, "s": 1}
      amount, unit = duration 
        
      await member.add_roles(role)
          
      embed2 = discord.Embed(
        description = f"<a:ApprovedCheckBox:901378101605445642> {member.mention} have been muted for {duration}",
        color = 0x44b582
      )
      
      await ctx.send(embed = embed2)
      
      await asyncio.sleep(amount * multiplier[unit])
      
      await member.remove_roles(role)


  #The unmute command
  @commands.command()
  @commands.has_permissions(manage_messages = True)
  async def unmute(self, ctx, member : discord.Member):
    role = discord.utils.get(ctx.guild.roles, name="Muted")
    
    await member.remove_roles(role)

    embed3 = discord.Embed(
          description = f"<a:ApprovedCheckBox:901378101605445642> {member.mention} have been unmuted",
          color = 0x44b582
        )

    await ctx.send(embed = embed3)
  
  #The slowmode command
  @commands.command()
  @commands.has_permissions(manage_channels = True)
  async def slowmode(ctx, seconds: int):
    await ctx.channel.edit(slowmode_delay=seconds)
    await ctx.send(f'The slowmode have been set to ``{seconds}`` seconds')
  
  #The lock commmand
  @commands.command()
  @commands.has_permissions(manage_channels = True)
  async def lock(self, ctx, *, channel):
    
    defaultRole = ctx.guild.default_role
    
    overwrite = discord.PermissionOverwrite()
    
    overwrite.send_messages = False
    
    await ctx.channel.set_permissions(defaultRole, overwrite=overwrite)
    
    await ctx.send(f"{ctx.channel.mention} have been successfully locked")
  
  #The unlock command
  @commands.command()
  @commands.has_permissions(manage_channels = True)
  async def unlock(self, ctx):
    
    defaultRole = ctx.guild.default_role

    overwrite = discord.PermissionOverwrite()
    
    overwrite.send_messages = True
    
    await ctx.channel.set_permissions(defaultRole, overwrite=overwrite)
    
    await ctx.send(f"{ctx.channel.mention} have been successfully unlocked")
  
  #The channelban command
  @commands.command(aliases = ["cb"])
  async def channelban(self, ctx, member: discord.Member, reason = None):
    
    overwrite = discord.PermissionOverwrite()
    
    overwrite.view_channel = False
    
    if reason == None:
      return await ctx.send("Please provide a reason")
    
    await ctx.channel.set_permissions(member, overwrite=overwrite)
    
    await ctx.send(f"{member.mention} have been banned from this channel")
  
  @commands.command()
  async def random(self, ctx):
    colour = discord.Colour
    
    randomEmbed = discord.Embed(
      description = "This is random",
      color = colour.random()
    )
    
    await ctx.send(embed = randomEmbed)




def setup(bot):
  bot.add_cog(Moderation(bot))