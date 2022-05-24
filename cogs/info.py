from discord import Member, Colour, Embed, NotFound, Emoji
from discord.ext import commands
import requests
import json
import datetime
import phonenumbers
from phonenumbers import carrier, geocoder, timezone
import os
import time
import dateutil.parser as dt


from utils.weather import parse_data

class Info(commands.Cog):
  
  def __init__(self, bot):
    self.bot = bot

  #The help command
  @commands.command()
  async def help(self, ctx):
    embed = Embed(title = "My list of commands",  colour = 0xffffff)
    embed.add_field(name = "Moderation Commands", value = "``ban`` ``unban`` ``kick`` ``slowmode`` ``nickname`` ``mute`` ``unmute`` ``purge`` ``lock`` ``unlock`` ``channelban``", inline = False)
    embed.add_field(name = "Info Commands", value = "``whois`` ``serverinfo`` ``botinfo`` ``covid`` ``emojiinfo`` ``numberinfo``", inline = False)
    embed.add_field(name = "Fun Commands", value = "``8ball`` ``avatar`` ``Konnichiwa`` ``meme`` ``emojify`` ``say`` ``catgif`` ``tweet`` ``fact`` ``owoify``", inline = False)
    embed.add_field(name = "Utilities Commands", value = "``changeprefix`` ``addrole`` ``removerole`` ``toggle`` ``whoadd``", inline = False)
    embed.add_field(name = "Miscellaneous Commands", value = "``run``", inline = False)

    embed.set_footer(text="Ping me if you don't know my prefix")

    await ctx.send(embed = embed)
  
  #The covid command
  @commands.command()
  async def covid(self, ctx, *, countryName = None):
          try:
              if countryName is None:
                  embed=Embed(title="This command is used like this: ```b!covid [country]```", colour=ctx.author.color)
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

                  embed2 = Embed(title=f"**COVID-19 Status Of {country}**!", description="This Information Isn't Live Always, Hence It May Not Be Accurate!", colour=ctx.author.color)
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
              embed3 = Embed(title="Invalid Country Name Or API Error! Try Again..!", colour=ctx.author.color)
              embed3.set_author(name="Error!")
              await ctx.send(embed=embed3)
  
  #The serverinfo command
  @commands.command()
  async def serverinfo(self, ctx, guildID = None):
    guild = ctx.guild if guildID is None else await self.bot.fetch_guild(guildID)
    serverBosterRole = "``None``" if guild.premium_subscriber_role is None else guild.premium_subscriber_role
    
    embed = Embed(
      title = "Server information",
      color = 0xffffff
    )
  
    embed.set_thumbnail(url=f'{guild.icon_url}')
    embed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)


    embed.add_field(name="Server Name", value=f'`{guild.name}`', inline=False)
    embed.add_field(name="Server ID", value=f'`{guild.id}`', inline=False)
    embed.add_field(name="Server Description", value=f'`{(guild.description)}`', inline=False)
    embed.add_field(name="Server Owner", value=f'`{guild.owner}`', inline=False)
    embed.add_field(name="Verify Level", value=f'`{guild.verification_level}`', inline=False)
    embed.add_field(name="Server Boost Level", value=f'`{guild.premium_tier}`', inline=False)
    embed.add_field(name="Server Boost Role", value=f'{serverBosterRole}', inline=False)
    embed.add_field(name="Highest Role", value=f'{guild.roles[-1].mention}', inline=False)
    embed.add_field(name="Total Roles", value=f'`{len(guild.roles)}`', inline=False)
    embed.add_field(name="Total Members", value=f'`{guild.member_count}`', inline=False)
    embed.add_field(name="Total Channels", value=f'`{len(guild.channels)}`', inline=False)
    embed.add_field(name="Total Categories", value=f'`{len(guild.categories)}`', inline=False)
    embed.add_field(name="The server was created at:", value=guild.created_at.strftime("``Date: %A, %d %B %Y``\n``Time: %H:%M %p %Z``"), inline=False)


    await ctx.send(embed=embed)
  
  #The whois command
  @commands.command()
  async def whois(self, ctx, member: Member = None):

    member = ctx.author if not member else member
    guild = ctx.guild
    
    roles = [role.mention for role in member.roles[::-1]]
    roles.pop()

    is_bot = "Yes" if member.bot else "No"
    
    if guild.owner_id == member.id:
      is_guild_owner = "Yes"
    else:
      is_guild_owner = "No"
    
    if member.nick is None:
      nickname = member.name
    else:
      nickname = member.nick
    
    if member.raw_status == "online":
      memberStatus = "<:Online:909327079101837362>"
    elif member.raw_status == "dnd":
      memberStatus = "<:Do_not_disturb:909327092016095252>"
    elif member.raw_status == "idle":
      memberStatus = "<:Idle:909327106448699402>"
    elif member.raw_status == "offline":
      memberStatus = "<:Offline:909327118146617384>"
    # elif member.raw_status == "invisible":
    #   memberStatus = "<:Offline:909327118146617384>"

    embed = Embed(colour = member.color, timestamp = ctx.message.created_at)

    embed.set_thumbnail(url=member.avatar_url)
    embed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
  
  
    embed.add_field(name="Username", value = f"``{member.name}#{member.discriminator}``", inline=False)
    embed.add_field(name="User's server nickname", value=f"``{nickname}``", inline=False)
    embed.add_field(name="ID", value=f"``{member.id}``", inline=False)

    if member.bot == True:
      embed.add_field(name="User's status", value=f"{memberStatus}", inline=False)
    else:
      embed.add_field(name="User's status", value=f"{memberStatus}", inline=False)
      embed.add_field(name = "User's activity", value = f"``{member.activity}``", inline = False)

    embed.add_field(name="Created at:", value = f"``{member.created_at.strftime('%m/%d/%Y, %H:%M %p')}``", inline=True)
    embed.add_field(name="Joined the server at:", value = f"``{member.joined_at.strftime('%m/%d/%Y, %H:%M %p')}``", inline=False)
    
    embed.add_field(name=f'Roles ({len(roles)})', value="  ".join(roles), inline=False)

    if member.bot == True:
      embed.add_field(name="Is this user a bot?", value = f"``{is_bot}``", inline=False)
    else:
      embed.add_field(name="Is this user a bot?", value = f"``{is_bot}``", inline=False)
      embed.add_field(name="Is this user the server owner?", value = f"``{is_guild_owner}``", inline=False)



    await ctx.send(embed=embed)
  
  #The emojiinfo command
  @commands.command(name = "emojiinfo", aliases = ["ai"])
  async def emoji_info(self, ctx, emoji: Emoji = None):
    if not emoji:
      return await ctx.invoke(self.bot.get_command("help"))
    
    try:
      emoji = await emoji.guild.fetch_emoji(emoji.id)
    
    except NotFound:
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
    
    colour = Colour
    
    emojiEmbed = Embed(
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

    colour = Colour

    valid_number = "Yes" if phonenumbers.is_valid_number(number) else "No"

    description = f"""
    **- The carrier's number:** ``{carrier.name_for_number(number, "en")}``
    **- The number's region:** ``{geocoder.description_for_number(number, "en")}``
    **- Number's timezone:** ``{timezone.time_zones_for_number(number)}``
    **- Valid phone number:** ``{valid_number}``
    """

    numEmbed = Embed(
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
      
    colour = Colour
      
    location = location.title()
          
    weatherEmbed = Embed(
      title = f"{location} weather",
      description = f"Here is the data for {location}.",
      colour = colour.random()
    )

    for key in data:
      weatherEmbed.add_field(name = aliases[key], value = str(data[key]), inline = False)
          
    await ctx.send(embed = weatherEmbed)
  
  @commands.command()
  async def gameinfo(self, ctx, placeID:int):
    universeID = requests.get(f"https://api.roblox.com/universes/get-universe-containing-place?placeid={placeID}")
    universeID_data = universeID.json()
    
    gameInfo = requests.get(f"https://games.roblox.com/v1/games?universeIds={universeID_data['UniverseId']}")
    gameInfo_data = gameInfo.json()

    groupInfo = requests.get(f"https://groups.roblox.com/v1/groups/{gameInfo_data['data'][0]['creator']['id']}")
    groupInfo_data = groupInfo.json()

    thumbnail = requests.get(f"https://thumbnails.roblox.com/v1/games/icons?universeIds={universeID_data['UniverseId']}&size=512x512&format=jpeg&isCircular=false")
    thumbnail_data = thumbnail.json()

    gameUrl = f"https://www.roblox.com/games/{gameInfo_data['data'][0]['rootPlaceId']}"

    if gameInfo_data['data'][0]['creator']['type'] == "Group":
      creator = f"{groupInfo_data['owner']['username']} ({gameInfo_data['data'][0]['creator']['name']})"
      creatorUrl = f"https://www.roblox.com/groups/{groupInfo_data['id']}"
    else:
      creator = gameInfo_data['data'][0]['creator']['name']
      creatorUrl = f"https://www.roblox.com/users/{gameInfo_data['data'][0]['creator']['id']}"
    
    createdDateTimeString = gameInfo_data['data'][0]['created']
    createdDateTimeformatted = dt.parse(createdDateTimeString)
    createdUnixtime = time.mktime(createdDateTimeformatted.timetuple())

    updatedDateTimeString = gameInfo_data['data'][0]['updated']
    updatedDateTimeformatted = dt.parse(updatedDateTimeString)
    updatedUnixtime = time.mktime(updatedDateTimeformatted.timetuple())

    description = f"""
    **Name:**
    [``{gameInfo_data['data'][0]['sourceName']}``]({gameUrl})
    
    **Creator:**
    [``{creator}``]({creatorUrl})
    
    **Visits:**
    ``{format(gameInfo_data['data'][0]['visits'], ',')}``

    **Created At:**
    {createdDateTimeformatted.strftime('%A, %d %B %Y')}  (<t:{round(createdUnixtime)}:R>)

    **Updated At:**
    {updatedDateTimeformatted.strftime('%A, %d %B %Y')}  (<t:{round(updatedUnixtime)}:R>)
    """

    embed = Embed(
      title="Roblox Game Info",
      description=description,
      colour = Colour.random()
    )
    
    embed.set_thumbnail(url=thumbnail_data["data"][0]["imageUrl"])

    await ctx.send(embed = embed)

def setup(bot):
  bot.add_cog(Info(bot))