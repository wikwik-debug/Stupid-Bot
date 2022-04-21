from  discord import User, Role, Member, AuditLogAction, Embed
from discord.ext import commands

import json
from datetime import datetime

class Utilities(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  #The change prefix command
  @commands.command(aliases = ["prefix"])
  @commands.has_permissions(administrator = True)
  async def changeprefix(self, ctx, prefix):
    with open("prefixes.json", "r") as f:
      prefixes = json.load(f)

    prefixes[f"{str(ctx.guild.name)}({str(ctx.guild.id)})"] = prefix

    with open("prefixes.json", "w") as f:
      json.dump(prefixes, f, indent = 4)
  
    await ctx.send(f'The prefix have been changed to ``{prefix}``')
  
  #The add role command
  @commands.command(pass_context = True)
  @commands.has_permissions(administrator = True)
  async def addrole(self, ctx, role: Role = None, user: Member = None):

    if role is  None:
      await ctx.reply(">addrole **<role>** <user>")
      # "Please select or mention a role to assign"
    
    elif user is None:
      await ctx.reply(">addrole <role> **<user>**")
      # Please mention or provide an id of a member
    
    elif role in user.roles:
      await ctx.send(f"{user.mention} already has the role {role.mention}")
    
    else:
      await user.add_roles(role)
      await ctx.send(f'Successfully added the {role.mention} role to {user.mention}')
  
  #The remove role command
  @commands.command(pass_context = True)
  @commands.has_permissions(administrator = True)
  async def removerole(self, ctx, role: Role, user: Member):

    if role in user.roles:
      await user.remove_roles(role)
      await ctx.send(f'Successfully removed the {role.mention} role from {user.mention}')

    else:
      await ctx.send(f'{user.mention} does not have the {role.mention} role')
  
  #The toggle command
  @commands.command(name = "toggle", description = "Enable or disable a command")
  @commands.is_owner()
  async def toggle(self, ctx, *, command):
    command = self.bot.get_command(command)
    
    if command is None:
      await ctx.reply("I can't find a command with that name")
    
    elif ctx.command == command:
      await ctx.reply("You cannot disable this command")
    
    else:
      command.enabled = not command.enabled
      ternary = "enabled" if command.enabled else "disabled"
      await ctx.send(f"I have {ternary} the {command.qualified_name} command for you! ♥")
  
  #The changename command
  @commands.command(name = "changename", description = "To edit the server's name")
  @commands.has_permissions(manage_guild = True)
  async def changename(self, ctx, *, name):
    await ctx.guild.edit(name=name)
    await ctx.send(f"I have changed the server's name to `{ctx.guild.name}`")
  
  #The whoadd command
  @commands.command()
  @commands.has_permissions(administrator = True)
  async def whoadd(self, ctx, *, user: User):
    guild = ctx.guild
    
    async for entries in guild.audit_logs(action=AuditLogAction.bot_add):
      if entries.target.id == user.id:
        entrisEmbed = Embed(
          title=f"{entries.target}",
          color=entries.target.color,
          timestamp=datetime.utcnow()
        )
        entrisEmbed.set_thumbnail(url=entries.target.avatar_url)
        entrisEmbed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
        
        entrisEmbed.add_field(name="Added by:", value=f"{entries.user.mention} (``{entries.user.id}``)", inline=False)
        entrisEmbed.add_field(name="Joined:", value=f"{entries.created_at.strftime('%A, %d %B %Y | %H:%M %p %Z')}", inline=True)
        
        await ctx.send(embed=entrisEmbed)

def setup(bot):
  bot.add_cog(Utilities(bot))