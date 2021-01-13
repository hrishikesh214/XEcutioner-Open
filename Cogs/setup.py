import discord
import json
import asyncio
import random
import requests
import secrets
import datetime
import mysql.connector as mysql
from discord.ext import commands, tasks
from discord.utils import *

replies_db = "./db/replies.json"
todo_db = "./db/todo_db.json"
help_db = "./db/help_db.json"
utility_db = "./db/utility.json"
livepin_db = "./db/livepin_db.json"

with open("config.json", 'r',encoding="utf8") as raw_config:
    config = json.load(raw_config)
with open(help_db, 'r',encoding="utf8") as raw_help:
    helps = json.load(raw_help)
with open(replies_db, 'r', encoding="utf8") as raw_replies:
    replies = json.load(raw_replies)

db = mysql.connect(
    host=config['mysql']['host'], 
    user=config['mysql']['username'], 
    password=config['mysql']['password'],
    database=config['mysql']['database']
    )

devdb = mysql.connect(
    host=config['devsql']['host'], 
    user=config['devsql']['username'], 
    password=config['devsql']['password'],
    database=config['devsql']['database']
    )

if(db):
    mycur = db.cursor(dictionary=True)
else:
    print("Remote MySQL Connection Failed!")
    exit()

PREFIX = config['default_prefix']

def xget_prefix(ctx):
    return getPStr(ctx)

def str_to_hex(hex):
    hex_int = int(hex, 0)
    return hex_int

emojis = ['😀 ','😃',' 😄',' 😁',' 😆 ','😅',' 😂',' 🤣',' 😊',' 😇',' 🙂',' 🙃',' 😉',' 😌',' 😍',' 🥰',' 😘',' 😗',' 😙',' 😚',' 😋',' 😛',' 😝',' 😜',' 🤪',' 🤨',' 🧐',' 🤓',' 😎',' 🥸',' 🤩',' 🥳',' 😏',' 😒',' 😞',' 😔',' 😟',' 😕',' 🙁',' ☹️',' 😣',' 😖',' 😫',' 😩',' 🥺',' 😢',' 😭',' 😤',' 😠',' 🤗',' 🤔',' 🤭',' 🤫',' 🤥',' 😶',' 😐',' 😑',' 😬',' 🙄',' 😯',' 😦',' 😧',' 😮',' 😲',' 🥱',' 😴',' 🤤',' 😪',' 😵',' 🤐',' 🥴',' 🤢',' 🤮',' 🤧',' 😷',' 🤒',' 🤕',' 🤑',' 🤠',' 😈']

def getEmbedColor(color=None):
    if color == "" or color == '' or color is None:
        return str_to_hex(config['default_embed_color'])
    else:
        return str_to_hex(color)

def getStandardHelpEmbed(root, ctx):
    PREFIX = getPStr(ctx)
    embed = discord.Embed(title=f"{root['name']} (help)", color=getEmbedColor())
    embed.add_field(name="Description", value=f"{root['desc']}", inline=False)
    embed.add_field(name="Usage", value=f"`{PREFIX}{root['usage']}`", inline=False)
    embed.add_field(name="Permissions", value=f"{root['permissions']}", inline=False)
    embed.set_footer(text=config['main_footer']+config['author'])
    return embed

def getPStr(ctx):
    checkDBCon(db)
    res = getGuildSettings(ctx)
    if 'prefix' in res.keys():
        return res['prefix']
    else:
        return "_ERR_Reinvite_Me_"

def getGuildSettings(ctx):
    sql = f"SELECT * FROM `{config['table']['guilds']}` WHERE `guildid` = {ctx.guild.id}"
    mycur.execute(sql)
    res = mycur.fetchall()
    if not res:
        return False
    return res[0]

def updateGuildSettings(ctx, new):
    sql = f"UPDATE `guilds` SET `prefix`='{new['prefix']}',`join_status`={new['join_status']},`join_channel`={new['join_channel']},`join_title`='{new['join_title']}',`join_color`='{new['join_color']}',`join_roles`='{new['join_roles']}',`leave_status`={new['leave_status']},`leave_title`='{new['leave_title']}',`leave_channel`={new['leave_channel']},`leave_color`='{new['leave_color']}',`meme_color`='{new['meme_color']}',`automeme_channel`={new['automeme_channel']},`automeme_status`={new['automeme_status']},`pin_channel`={new['pin_channel']},`private_channel`={new['private_channel']} WHERE `guildid` = {new['guildid']}"
    mycur.execute(sql)
    db.commit()
    return mycur.rowcount

def getTodos(ctx, tid=None):
    if tid is not None:
        sql = f"SELECT * FROM `{config['table']['todos']}` WHERE `userid` = {ctx.message.author.id} AND `taskid` = {tid}"
    else:
        sql = f"SELECT * FROM `{config['table']['todos']}` WHERE `userid` = {ctx.message.author.id}"        
    mycur.execute(sql)
    res = mycur.fetchall()
    return res

def updateTodos(ctx, new):
    if ctx.message.author.id != new['userid']:
        return False
    sql = f"UPDATE `{config['table']['todos']}` SET `title`='{new['title']}',`description`='{new['description']}',`status`={new['status']} WHERE `taskid` = {new['taskid']}"
    mycur.execute(sql)
    db.commit()
    return mycur.rowcount

def insertTodos(ctx, new):
    sql = f"INSERT INTO `{config['table']['todos']}`(`userid`, `taskid`, `title`, `description`, `status`) VALUES ({new['userid']},null,'{new['title']}', '{new['description']}', {new['status']})"
    mycur.execute(sql)
    db.commit()
    return mycur.lastrowid

def insertLp(ctx, new):
    sql = f"INSERT INTO `{config['table']['livepins']}`(`channelid`, `messageid`, `status`) VALUES ({new['channelid']},{new['messageid']},{new['status']})"
    mycur.execute(sql)
    db.commit()
    return mycur.lastrowid

def updateLp(message, new):
    sql = f"UPDATE `{config['table']['livepins']}` SET `messageid`={new['messageid']},`status`={new['status']} WHERE `channelid`={message.channel.id}"
    mycur.execute(sql)
    db.commit()
    return mycur.rowcount

def getLp(message):
    sql = f"SELECT * FROM `{config['table']['livepins']}` WHERE `channelid`={message.channel.id}"
    mycur.execute(sql)
    res = mycur.fetchone()
    return res

def checkDBCon(db):
    db.ping(reconnect=True, delay=5, attempts=5)