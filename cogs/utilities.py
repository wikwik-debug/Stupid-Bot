import discord
from discord.ext import commands

import json

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
  @commands.has_permissions(manage_roles = True)
  async def addrole(self, ctx, role: discord.Role = None, user: discord.Member = None):

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
  @commands.has_permissions(manage_roles = True)
  async def removerole(self, ctx, role: discord.Role, user: discord.Member):

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
  
  @commands.command(name = "createserver")
  async def create_guild(self, ctx, name, region):
    await self.bot.create_guild(name=name, region=region)
    await ctx.send(f"I have created a server called {name}")


def setup(bot):
  bot.add_cog(Utilities(bot))