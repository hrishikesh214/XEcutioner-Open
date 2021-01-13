import discord
import json
import sys
import os
import mysql.connector as mysql
from discord.ext import commands
from Cogs.setup import getEmbedColor, str_to_hex, checkDBCon

replies_db = "./db/replies.json"

with open("config.json", 'r',encoding="utf8") as raw_config:
    config = json.load(raw_config)

with open(replies_db, 'r') as raw_replies:
    replies = json.load(raw_replies)

db = mysql.connect(
    host=config['mysql']['host'], 
    user=config['mysql']['username'], 
    password=config['mysql']['password'],
    database=config['mysql']['database']
    )

if(db):
    db.autocommit = config['mysql']['autocommit']
    mycur = db.cursor(dictionary=True)
    print("MySQL Connected...")
else:
    print("Remote MySQL Connection Failed!")
    exit()

async def get_prefix(bot, message):
    sql = "SELECT `prefix` FROM `" + config['table']['guilds'] +"` WHERE `guildid` = " + str(message.guild.id)
    res = None
    checkDBCon(db)
    try:
        mycur.execute(sql)
        res = mycur.fetchall()
    except Exception as err:
        if isinstance(err, mysql.errors.OperationalError):
            db.reconnect(attempts=5, delay=5)
        if isinstance(err, mysql.errors.InterfaceError):
            print("Interface Error: Refused")
        else:
            print(err)
            db.reconnect(attempts=1, delay=0)
    if res is None:
        em = await message.channel.send("```css\nIt seems there is some [error]\nWait for some time or try Reinviting Me to the .Server!```")
        await em.delete(delay=7)
        return commands.when_mentioned(bot, message)
    pr = res[0]['prefix']
    return commands.when_mentioned_or(pr)(bot, message)
   

TOKEN = config['token']
intents = discord.Intents.default()
intents.members=True
bot = commands.Bot(command_prefix=get_prefix, case_insensitive=True, intents=intents, help_command=None)

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=config['default_prefix']+"help"))
    print('I am Ready!')

@bot.event
async def on_guild_join(guild):
    edesc = f"This channel is for {bot.user.name}. Here all updates and issues related to the bot will be posted. While you can test bot and run commands here too\nThank You"
    embed = discord.Embed(color=getEmbedColor())
    author = await bot.fetch_user(int(config['authorid']))
    embed.set_author(name=author.name, icon_url=author.avatar_url)
    embed.add_field(name="About This Channel", value = edesc, inline=False)
    embed.set_footer(text=config['main_footer']+config['author'])

    rules = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        guild.me: discord.PermissionOverwrite(read_messages=True)
    }
    xtopic = config['guild_private_channel']['topic']
    mc = 0
    try:
        xchannel = await guild.create_text_channel(config['guild_private_channel']['name'], overwrites=rules,topic=xtopic)
        if xchannel is not None:
            mc = xchannel.id
    except Exception as e:
        pass
        
    new = {
        "guildid":guild.id,
        "prefix": str(config['default_prefix']),
        "join": {
            "status":0,
            "title":"",
            "channel":0,
            "color":"",
            "roles":""
        },
        "leave": {
            "status":0,
            "title":"",
            "channel":0,
            "color":""
        },
        "meme":{
            "color":"",
            "automeme":{
                "channel":0,
                "status":0
            }
        },
        "pin_channel":0,
        "private_channel":mc
    }
    sql = f"INSERT INTO `{config['table']['guilds']}`(`guildid`, `prefix`, `join_status`, `join_channel`, `join_title`, `join_color`, `join_roles`, `leave_status`, `leave_title`, `leave_channel`, `leave_color`, `meme_color`, `automeme_channel`, `automeme_status`, `pin_channel`, `private_channel`) VALUES({new['guildid']}, '{new['prefix']}', {new['join']['status']}, {new['join']['channel']}, '{new['join']['title']}', '{new['join']['color']}', '{new['join']['roles']}', {new['leave']['status']}, '{new['leave']['title']}', {new['leave']['channel']}, '{new['leave']['color']}', '{new['meme']['color']}', {new['meme']['automeme']['channel']}, {new['meme']['automeme']['status']}, {new['pin_channel']}, {new['private_channel']})"
    
    mycur.execute(sql)
    db.commit()
    if mc != 0:
        await xchannel.send(embed=embed)
    
@bot.event
async def on_guild_remove(guild):
    sql = f"DELETE FROM `{config['table']['guilds']}` WHERE `guildid` = {guild.id}" 
    mycur.execute(sql)
    db.commit()

# @bot.event
# async def on_message(message):
#     if message.author == bot.user:
#         return
#     await bot.process_commands(message)   


extentions = config['extentions']

if __name__ == "__main__":
    for extention in extentions.keys():
        if int(extentions[extention]):
            try:
                bot.load_extension(extention)
                x = extention.split('.')
                print(f"{x[1]} is loaded...") if len(x) == 2 else print(f"{x[0]} is loaded...")
            except Exception as e:
                print(f"Error while loading extention({extention}): {e}")

bot.run(TOKEN)