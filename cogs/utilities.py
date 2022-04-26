from pydoc import describe
from  discord import Role, Member, AuditLogAction, Embed
from discord.ext import commands
from discord.ext.commands import MemberConverter
from discord.ext.commands.errors import MemberNotFound

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
  async def addrole(self, ctx, user: Member = None, *roles: Role):
    if len(roles) == 0:
      await ctx.reply("Please select or mention a role to assign")
    elif user is None:
      await ctx.reply("Please mention or provide an id of a member")

    for role in roles:
      totalRoles = totalRoles + roles[role]
      
      if role in user.roles:
        errorAddRoleEmbed = Embed(
          description = f"<a:DeniedBox:882782174208749608> {user.mention} already has the role {role.mention}",
          color = 0xf04947
        )
        await ctx.send(embed = errorAddRoleEmbed)
      else:
        await user.add_roles(role)
        AddRoleEmbed = Embed(
          description = f"<a:ApprovedCheckBox:882777440609521724> {user.mention} has been added to the following role(s): {totalRoles.mention}",
          color = 0x44b582
        )
        await ctx.send(embed = AddRoleEmbed)
  
  #The remove role command
  @commands.command(pass_context = True)
  @commands.has_permissions(administrator = True)
  async def removerole(self, ctx, user: Member, *roles: Role):
    for role in roles:
      if role in user.roles:
        removeRoleEmbed = Embed(
          description = f"<a:ApprovedCheckBox:882777440609521724> Successfully removed the {role.mention} role from {user.mention}",
          color = 0x44b582
        )
        await user.remove_roles(role)
        await ctx.send(embed=removeRoleEmbed)
      else:
        errorRemoveRoleEmbed = Embed(
          description = f"<a:DeniedBox:882782174208749608> {user.mention} does not have the {role.mention} role",
          color = 0xf04947
        )
        await ctx.send(embed = errorRemoveRoleEmbed)
  
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
  async def whoadd(self, ctx, *, member: MemberConverter):
    async for entries in ctx.guild.audit_logs(action=AuditLogAction.bot_add):
      if entries.target.id == member.id:
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
        return

def setup(bot):
  bot.add_cog(Utilities(bot))