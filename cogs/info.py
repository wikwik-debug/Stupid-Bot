import discord
# from discord import Guild as guild
# from discord import PublicUserFlags
from discord.ext import commands
import requests
import json
import datetime
import phonenumbers
from phonenumbers import carrier, geocoder, timezone
import os


from main import configure
from weather import parse_data

class Info(commands.Cog):
  
  def __init__(self, bot):
    self.bot = bot

  #The help command
  @commands.command()
  async def help(self, ctx):
    embed = discord.Embed(title = "My list of commands", description = "Ping me if you don't know my prefix", colour = 0xffffff)
    embed.add_field(name = "Moderation Commands", value = "``ban`` ``unban`` ``kick`` ``slowmode`` ``nickname`` ``mute`` ``unmute`` ``purge`` ``lock`` ``unlock`` ``channelban``", inline = False)
    embed.add_field(name = "Info Commands", value = "``whois`` ``serverinfo`` ``botinfo`` ``covid`` ``emojiinfo`` ``numberinfo``", inline = False)
    embed.add_field(name = "Fun Commands", value = "``8ball`` ``avatar`` ``Konnichiwa`` ``meme`` ``emojify`` ``say`` ``catgif`` ``tweet``", inline = False)
    embed.add_field(name = "Utilities Commands", value = "``changeprefix`` ``addrole`` ``removerole`` ``toggle``", inline = False)
    embed.add_field(name = "Miscellaneous Commands", value = "``run``", inline = False)

    await ctx.send(embed = embed)
  
  #The covid command
  @commands.command()
  async def covid(self, ctx, *, countryName = None):
          try:
              if countryName is None:
                  embed=discord.Embed(title="This command is used like this: ```b!covid [country]```", colour=ctx.author.color)
                  await ctx.send(embed=embed)

              else:
                  url = f"https://coronavirus-19-api.herokuapp.com/countries/{countryName}"
                  stats = requests.get(url)
                  json_stats = stats.json()
                  country = json_stats["country"]
                  totalCases = json_stats["cases"]
                  todayCases = json_stats["todayCases"]
                  totalDeaths = json_stats["deaths"]
                  todayDeaths = json_stats["todayDeaths"]
                  recovered = json_stats["recovered"]
                  active = json_stats["active"]
                  critical = json_stats["critical"]
                  casesPerOneMillion = json_stats["casesPerOneMillion"]
                  deathsPerOneMillion = json_stats["deathsPerOneMillion"]
                  totalTests = json_stats["totalTests"]
                  testsPerOneMillion = json_stats["testsPerOneMillion"]

                  embed2 = discord.Embed(title=f"**COVID-19 Status Of {country}**!", description="This Information Isn't Live Always, Hence It May Not Be Accurate!", colour=ctx.author.color)
                  embed2.add_field(name="**Total Cases**", value=totalCases, inline=True)
                  embed2.add_field(name="**Today Cases**", value=todayCases, inline=True)
                  embed2.add_field(name="**Total Deaths**", value=totalDeaths, inline=True)
                  embed2.add_field(name="**Today Deaths**", value=todayDeaths, inline=True)
                  embed2.add_field(name="**Recovered**", value=recovered, inline=True)
                  embed2.add_field(name="**Active**", value=active, inline=True)
                  embed2.add_field(name="**Critical**", value=critical, inline=True)
                  embed2.add_field(name="**Cases Per One Million**", value=casesPerOneMillion, inline=True)
                  embed2.add_field(name="**Deaths Per One Million**", value=deathsPerOneMillion, inline=True)
                  embed2.add_field(name="**Total Tests**", value=totalTests, inline=True)
                  embed2.add_field(name="**Tests Per One Million**", value=testsPerOneMillion, inline=True)

                  embed2.set_thumbnail(url="https://cdn.discordapp.com/attachments/564520348821749766/701422183217365052/2Q.png")
                  await ctx.send(embed=embed2)

          except:
              embed3 = discord.Embed(title="Invalid Country Name Or API Error! Try Again..!", colour=ctx.author.color)
              embed3.set_author(name="Error!")
              await ctx.send(embed=embed3)
  
  #The serverinfo command
  @commands.command()
  async def serverinfo(self, ctx, guildID = None):
    guild = ctx.guild if guildID is None else await self.bot.fetch_guild(guildID)
    serverBosterRole = "``None``" if guild.premium_subscriber_role is None else guild.premium_subscriber_role
    
    embed = discord.Embed(
      title = "Server information",
      color = 0xffffff
    )
  
    embed.set_thumbnail(url=f'{guild.icon_url}')
    embed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)


    embed.add_field(name="Server Name", value=f'`{guild.name}`', inline=False)
    embed.add_field(name="Server ID", value=f'`{guild.id}`', inline=False)
    embed.add_field(name="Server Description", value=f'`{(guild.description)}`', inline=False)
    embed.add_field(name="Server Owner 👑", value=f'`{guild.owner}`', inline=False)
    embed.add_field(name="Verify Level", value=f'`{guild.verification_level}`', inline=False)
    embed.add_field(name="Server Boost Level", value=f'`{guild.premium_tier}`', inline=False)
    embed.add_field(name="Server Boost Role", value=f'{serverBosterRole}', inline=False)
    embed.add_field(name="Highest Role", value=f'{guild.roles[-1].mention}', inline=False)
    embed.add_field(name="Total Roles", value=f'`{len(guild.roles)}`', inline=False)
    # embed.add_field(name="Total Members", value=f'`{guild.member_count}`', inline=False)
    embed.add_field(name="Total Channels", value=f'`{len(guild.channels)}`', inline=False)
    embed.add_field(name="Total Categories", value=f'`{len(guild.categories)}`', inline=False)
    embed.add_field(name="The server was created at:", value=guild.created_at.strftime("``Date: %A, %d %B %Y``\n``Time: %H:%M %p %Z``"), inline=False)


    await ctx.send(embed=embed)
  
  #The whois command
  @commands.command()
  async def whois(self, ctx, member: discord.Member = None):

    member = ctx.author if not member else member
    
    roles = [role.mention for role in member.roles[::-1]]
    roles.pop()

    is_bot = "Yes" if member.bot else "No"

    embed = discord.Embed(colour = member.color, timestamp = ctx.message.created_at)

    embed.set_thumbnail(url=member.avatar_url)
    embed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
  
  
    embed.add_field(name="Username", value = f"``{member.name}#{member.discriminator}``", inline=False)
    embed.add_field(name="User's server nickname", value=f"``{member.nick}``", inline=False)
    
    embed.add_field(name="ID", value=f"``{member.id}``", inline=False)
    embed.add_field(name="User's status", value=f"``{member.status}``", inline=False)
    embed.add_field(name = "User's activity", value = f"``{member.activity}``", inline = False)

    embed.add_field(name="Created at:", value = f"``{member.created_at.strftime('%m/%d/%Y, %H:%M:%S')}``", inline=True)
    embed.add_field(name="Joined the server at:", value = f"``{member.joined_at.strftime('%m/%d/%Y, %H:%M:%S')}``", inline=False)

    embed.add_field(name=f'Roles ({len(member.roles[::-1])})', value =" ".join(roles), inline=False)

    embed.add_field(name="Is this user a bot?", value = f"``{is_bot}``", inline=False)


    await ctx.send(embed=embed)
  
  #The emojiinfo command
  @commands.command(name = "emojiinfo", aliases = ["ai"])
  async def emoji_info(self, ctx, emoji: discord.Emoji = None):
    if not emoji:
      return await ctx.invoke(self.bot.get_command("help"))
    
    try:
      emoji = await emoji.guild.fetch_emoji(emoji.id)
    
    except discord.NotFound:
      return await ctx.send("I could not find this emoji in the given guild")
    
    is_managed = "Yes" if emoji.managed else "No"
    is_animated = "Yes" if emoji.animated else "No"
    require_colons = "Yes" if emoji.require_colons else "No"
    creation_time = emoji.created_at.strftime("%m/%d/%Y, %H:%M:%S")
    can_use_emoji = "Everyone" if not emoji.roles else " ".join(role.name for role in emoji.roles[1:])

    description = f"""
    **General:**
    **- Name:** {emoji.name}
    **- ID:** {emoji.id}
    **- URL:** [Link To Emoji]({emoji.url})
    **- Author:** {emoji.user.mention}
    **- Time Created:** {creation_time}
    **- Usable by:** {can_use_emoji}

    **Other:**
    **- Animated:** {is_animated}
    **- Managed:** {is_managed}
    **- Require Colons:** {require_colons}
    **- Guild Name:** {emoji.guild.name}
    **- Guild ID:** {emoji.guild.id}
    """
    
    colour = discord.Colour
    
    emojiEmbed = discord.Embed(
      title = f"**Emoji Information for:** `{emoji.name}`",
      description=description,
      color = colour.random()
    )
    emojiEmbed.set_thumbnail(url = emoji.url)
    await ctx.send(embed = emojiEmbed)
  
  #The numberinfo command
  @commands.command(aliases = ["ni"])
  async def numberinfo(self, ctx, number):
    
    number = phonenumbers.parse(number)

    colour = discord.Colour

    valid_number = "Yes" if phonenumbers.is_valid_number(number) else "No"

    description = f"""
    **- The carrier's number:** ``{carrier.name_for_number(number, "en")}``
    **- The number's region:** ``{geocoder.description_for_number(number, "en")}``
    **- Number's timezone:** ``{timezone.time_zones_for_number(number)}``
    **- Valid phone number:** ``{valid_number}``
    """

    numEmbed = discord.Embed(
      title = f"Phone number information for: `{phonenumbers.format_number(number, phonenumbers.PhoneNumberFormat.NATIONAL)}`",
      description = description,
      color = colour.random()
    )

    numEmbed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/900644202453549076/908989593876054016/Goblok.png")

    await ctx.send(embed = numEmbed)
  
  #The weather command
  @commands.command()
  async def weather(ctx, *, location):

    url = f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={os.getenv('API_KEY')}&units=imperial"
    data = json.loads(requests.get(url).content)
    data = parse_data(data)
      
    aliases = {
      'temp': 'Temperature',
      'temp_max': "Maximum Temperature",
      "temp_min": "Minimum Temperature",
      "feels_like": "Feels like",
      "sea_level": "Sea level",
      "grnd_level": "Ground level"
    }
      
    colour = discord.Colour
      
    location = location.title()
          
    weatherEmbed = discord.Embed(
      title = f"{location} weather",
      description = f"Here is the data for {location}.",
      colour = colour.random()
    )

    for key in data:
      weatherEmbed.add_field(name = aliases[key], value = str(data[key]), inline = False)
          
    await ctx.send(embed = weatherEmbed)


def setup(bot):
  bot.add_cog(Info(bot))