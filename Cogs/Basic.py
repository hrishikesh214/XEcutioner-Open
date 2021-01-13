from .setup import *
from math import floor

class Basic(commands.Cog, name="Basic"):
    def __init__(self, bot):
        self.bot = bot
        # self.mysql_recon.start()

    @tasks.loop(seconds=config['mysql']['loop_check'])
    async def mysql_recon(self):
        checkDBCon(db)
        checkDBCon(devdb)

    @mysql_recon.error
    async def mr_err(self, err):
        if isinstance(err, mysql.InterfaceError):
            print("Connection failed")

    @commands.command(help="About Bot")
    async def about(self, ctx):
        author = await self.bot.fetch_user(int(config['authorid']))
        embed = discord.Embed(title="About Me", description="", color=getEmbedColor())
        embed.add_field(name="Name", value=f"`{self.bot.user.name}`", inline=True)
        embed.add_field(name="Version", value=f"`{config['version']}`", inline=True)
        embed.add_field(name="Deployed", value=f"`{config['release']}`", inline=True)
        embed.add_field(name="Last Updated", value=f"`{config['last_update']}`", inline=True)
        embed.add_field(name="Used", value=f"`{config['language']}`", inline=True)
        embed.add_field(name="Latency", value=f"`{floor(self.bot.latency * 1000)} ms`", inline=True)
        embed.add_field(name="Watching", value=f"`{len(self.bot.guilds)} servers`", inline=True)
        embed.add_field(name="Support", value=f"[Invite]({config['bot_invite_link']}) | [Official Discord Server]({config['official_dlink']})", inline=False)
        embed.set_footer(text="Made with ❤️ By "+config['author'])
        embed.set_thumbnail(url=self.bot.user.avatar_url)
        # embed.set_author(name=author.name, icon_url=author.avatar_url)
        await ctx.message.channel.send(embed=embed)

    @commands.command(help="Bot says")
    async def say(self, ctx, *, msg):
        await ctx.message.delete()
        await ctx.message.channel.send(msg)

    @commands.command(help="Get your Roles") 
    async def myroles(self, ctx):
        await ctx.message.add_reaction('👍')
        user = ctx.message.author
        raw_roles = user.roles
        roles = []
        title = user.name
        title += " 's Role"
        myembed = discord.Embed(title=title, description=user.mention ,color=getEmbedColor())
        l = len(raw_roles)
        for x in reversed(range(1,l)):
            myembed.add_field(name=(l-x), value=raw_roles[x].name, inline=True)
        myembed.set_thumbnail(url=user.avatar_url)
        await ctx.send(embed=myembed)
    
    @commands.command(help="Quick Embed")
    @commands.has_permissions(manage_messages=True)
    async def qe(self, ctx, *, message):
        embed = discord.Embed(description=message, color=getEmbedColor())
        author = ctx.message.author
        embed.set_author(name=author.name, icon_url=author.avatar_url)
        await ctx.message.delete(delay=1)
        await ctx.send(embed=embed)
    
    @qe.error
    async def qe_error(self, ctx, err):
        if isinstance(err, commands.MissingRequiredArgument):
            await ctx.message.add_reaction('🙄')
            await ctx.send(f"Please write a Message!")
    
    @commands.command()
    async def timer(self, ctx, sec:int):
        if  not sec <= 0:
            if sec > 600:
                tempmsg = await ctx.send("Well I can't count above 600 seconds 😕")
                await tempmsg.delete(delay=5)
            else:
                tempsec = sec
                timermsg = await ctx.send(f"Timer : {tempsec} second/s")
                while(True):
                    tempsec -= 1
                    if tempsec == 0:
                        break
                    await timermsg.edit(content=f"Timer : {tempsec} second/s")
                    await asyncio.sleep(1)
                await timermsg.delete(delay=1)
                await ctx.send(f"{ctx.message.author.mention}, your timer is down 👍")
        else:
            tempmsg = await ctx.send("Well I can't count down negative 😕")
            await tempmsg.delete(delay=5)

    @commands.command(name="setup")
    async def x_set(self, ctx):
        edesc = f"This channel is for {self.bot.user.name}. Here all updates and issues related to the bot will be posted. While you can test bot and run commands here too\nThank You"
        embed = discord.Embed(color=getEmbedColor())
        author = await self.bot.fetch_user(int(config['authorid']))
        embed.set_author(name=author.name, icon_url=author.avatar_url)
        embed.add_field(name="About This Channel", value = edesc, inline=False)
        embed.set_footer(text=config['main_footer']+config['author'])

        rules = {
            ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            ctx.guild.me: discord.PermissionOverwrite(read_messages=True)
        }
        xtopic = config['guild_private_channel']['topic']
        try:
            xchannel = await ctx.guild.create_text_channel(config['guild_private_channel']['name'], overwrites=rules,topic=xtopic)
            if xchannel is not None:
                mc = xchannel.id
            else:
                mc = 0
        except Exception as e:
            await ctx.send("I lack Permissions")

        guild_data = getGuildSettings(ctx)
        guild_data['private_channel'] = mc
        process = updateGuildSettings(ctx, guild_data)
        if mc != 0:
            await xchannel.send(embed=embed)
            await ctx.message.add_reaction('👍')
        
    @commands.command()
    async def sh(self, ctx, mid:int):
        msg = await ctx.fetch_message(mid)
        print(msg.content)
        # await ctx.send(msg.embeds)
        for embed in msg.embeds:
            print(embed.to_dict())


def setup(bot):
    bot.add_cog(Basic(bot))