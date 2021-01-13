from .setup import *    

class Settings(commands.Cog, name="Settings"):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_member_join(self, member):
        sql = f"SELECT * FROM `{config['table']['guilds']}` WHERE `guildid` = {member.guild.id}"
        mycur.execute(sql)
        guild_db = mycur.fetchone()
        if int(guild_db['join_status']):
            channel = self.bot.get_channel(int(guild_db['join_channel']))
            roles = []
            roles_name = guild_db['join_roles'].split(',')
            for x in roles_name:
                roles.append(discord.utils.get(member.guild.roles, name=str(x)))
            print(guild_db['join_roles'])
            embed = discord.Embed(title=guild_db['join_title'], description=member.mention, color=getEmbedColor(guild_db['join_color']))
            embed.set_image(url = member.avatar_url)
            embed.set_thumbnail(url=member.guild.icon_url)
            for role in roles:
                if role is not None:
                    await member.add_roles(role)
            await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        sql = f"SELECT * FROM `{config['table']['guilds']}` WHERE `guildid` = {member.guild.id}"
        mycur.execute(sql)
        guild_db = mycur.fetchone()
        if int(guild_db['leave_status']):
            settings = guild_db
            channel = self.bot.get_channel(int(settings['leave_channel']))
            embed = discord.Embed(title=settings['leave_title'], description=member.mention, color=getEmbedColor(guild_db['join_color']))
            embed.set_image(url = member.avatar_url)
            embed.set_thumbnail(url=member.guild.icon_url)
            await channel.send(embed=embed)

    @commands.command(help="Change Prefix")
    @commands.has_permissions(administrator=True)
    async def setprefix(self, ctx, *, pr):
        # await ctx.message.add_reaction('🙄')
        # embed1 = discord.Embed(description="Sorry Set Prefix is still not ready!")
        # await ctx.send(embed= embed1)
        # return
        new = getGuildSettings(ctx)
        new['prefix'] = str(pr)
        if updateGuildSettings(ctx, new):
            PREFIX = pr
            await ctx.message.add_reaction('👍')
            
    @commands.group(help="sets join")
    @commands.has_permissions(administrator=True)
    async def join(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send(f"Use `{PREFIX}help join`")

    @join.group(help="set join channel", name="channel")
    async def jchannel(self, ctx, ch:discord.TextChannel):
        new = getGuildSettings(ctx)
        new['join_channel'] = ch.id
        updateGuildSettings(ctx, new)
        embed = discord.Embed(description="Join Channel Updated 😄" , color=str_to_hex(config['default_embed_color']))
        await ctx.send(embed=embed)
        await ctx.message.add_reaction('👍')

    @join.group(help="set join welcome message", name="msg")
    async def jmsg(self, ctx, *, message):
        if message is None:
            message = ""
        new = getGuildSettings(ctx)
        new['join_title'] = str(message)
        updateGuildSettings(ctx, new)
        embed = discord.Embed(description="Join Message Updated 😄" , color=str_to_hex(config['default_embed_color']))
        await ctx.send(embed=embed)
        await ctx.message.add_reaction('👍')

    @join.group(help="set join welcome message", name="color")
    async def jcolor(self, ctx, color):
        if color is None:
            color = config['default_embed_color']
        new = getGuildSettings(ctx)
        new['join_color'] = str(color)
        updateGuildSettings(ctx, new)
        embed = discord.Embed(description="Join Color Updated 😄" , color=str_to_hex(config['default_embed_color']))
        await ctx.send(embed=embed)
        await ctx.message.add_reaction('👍')

    @join.group(help="Enable / Disable : 1 / 0", name="status")
    async def jstatus(self, ctx, *, st:int):
        new = getGuildSettings(ctx)
        if new['join_channel'] == 0:
            await ctx.send(f"Please set join channel first by `{PREFIX}join channel #channel`")
            return
        new['join_status'] = int(st)
        updateGuildSettings(ctx, new)
        embed = discord.Embed(description="Join Status Updated 😄" , color=str_to_hex(config['default_embed_color']))
        await ctx.send(embed=embed)
        await ctx.message.add_reaction('👍')
    
    @join.group(name="addrole")
    async def jar(self, ctx, *, st):
        new = getGuildSettings(ctx)
        oldroles = new['join_roles'].split(',')
        oldroles.append(st)
        newroles = ','.join(oldroles)
        new['join_roles'] = newroles
        updateGuildSettings(ctx, new)
        embed = discord.Embed(description="Join Autoroles Updated 😄" , color=str_to_hex(config['default_embed_color']))
        await ctx.send(embed=embed)
        await ctx.message.add_reaction('👍')

    @join.group(name="removerole")
    async def jrr(self, ctx, *, st):
        new = getGuildSettings(ctx)
        oldroles = new['join_roles'].split(',')
        oldroles.remove(st)
        newroles = ','.join(oldroles)
        new['join_roles'] = newroles
        updateGuildSettings(ctx, new)
        embed = discord.Embed(description="Join Autoroles Updated 😄" , color=str_to_hex(config['default_embed_color']))
        await ctx.send(embed=embed)
        await ctx.message.add_reaction('👍')


    @commands.group(help="sets leaves")
    @commands.has_permissions(administrator=True)
    async def leave(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send(f"Use `{PREFIX}help leave")

    @leave.group(help="set leave channel", name="channel")
    async def lchannel(self, ctx, ch:discord.TextChannel):
        new = getGuildSettings(ctx)
        new['leave_channel'] = ch.id
        updateGuildSettings(ctx, new)
        embed = discord.Embed(description="Leave Channel Updated 😄" , color=str_to_hex(config['default_embed_color']))
        await ctx.send(embed=embed)
        await ctx.message.add_reaction('👍')

    @leave.group(help="set leave welcome message", name="msg")
    async def lmsg(self, ctx, *, message):
        if message is None:
            message = ""
        new = getGuildSettings(ctx)
        new['leave_title'] = str(message)
        updateGuildSettings(ctx, new)
        embed = discord.Embed(description="Leave Message Updated 😄" , color=str_to_hex(config['default_embed_color']))
        await ctx.send(embed=embed)
        await ctx.message.add_reaction('👍')

    @leave.group(help="set leave welcome message", name="color")
    async def lcolor(self, ctx, color):
        if color is None:
            color = config['default_embed_color']
        new = getGuildSettings(ctx)
        new['leave_color'] = str(color)
        updateGuildSettings(ctx, new)
        embed = discord.Embed(description="Leave Color Updated 😄" , color=str_to_hex(config['default_embed_color']))
        await ctx.send(embed=embed)
        await ctx.message.add_reaction('👍')

    @leave.group(help="Enable / Disable : 1 / 0", name="status")
    async def lstatus(self, ctx, *, st:int):
        new = getGuildSettings(ctx)
        if new['leave_channel'] == 0:
            await ctx.send(f"Please set leave channel first by `{PREFIX}leave channel #channel`")
            return
        new['leave_status'] = int(st)
        updateGuildSettings(ctx, new)
        embed = discord.Embed(description="Leave Status Updated 😄" , color=str_to_hex(config['default_embed_color']))
        await ctx.send(embed=embed)
        await ctx.message.add_reaction('👍')

    @setprefix.error
    async def sp_error(self, ctx, err):
        if isinstance(err, commands.MissingPermissions):
            tempmsg = await ctx.send(f"You dont have permission to use this command")
            await tempmsg.delete(delay=5)
    
    @join.error
    async def j_error(self, ctx, err):
        if isinstance(err, commands.MissingPermissions):
            tempmsg = await ctx.send(f"You dont have permission to use this command")
            await tempmsg.delete(delay=5)
        
    @leave.error
    async def l_error(self, ctx, err):
        if isinstance(err, commands.MissingPermissions):
            tempmsg = await ctx.send(f"You dont have permission to use this command")
            await tempmsg.delete(delay=5)

    @jchannel.error
    async def jch_error(self, ctx, err):
        if isinstance(err, commands.MissingRequiredArgument):
            await ctx.send(f"Please mention a channel!")

    @jcolor.error
    async def jc_error(self, ctx, err):
        if isinstance(err, commands.MissingRequiredArgument):
            await ctx.send(f"Please mention a color in hex (e.g. 0xffffff)!")

    @jmsg.error
    async def jmsg_error(self, ctx, err):
        if isinstance(err, commands.MissingRequiredArgument):
            await ctx.send(f"Please Give a Message!")

    @jstatus.error
    async def js_error(self, ctx, err):
        if isinstance(err, commands.MissingRequiredArgument):
            await ctx.send(f"Please give status 1 for enable or 2 for disable the feature!")

    @jar.error
    async def jar_error(self, ctx, err):
        if isinstance(err, commands.MissingRequiredArgument):
            await ctx.send(f"Please give role name")

    @jrr.error
    async def jrr_error(self, ctx, err):
        if isinstance(err, commands.MissingRequiredArgument):
            await ctx.send(f"Please give role name")

    @lchannel.error
    async def lch_error(self, ctx, err):
        if isinstance(err, commands.MissingRequiredArgument):
            await ctx.send(f"Please mention a channel!")

    @lcolor.error
    async def lc_error(self, ctx, err):
        if isinstance(err, commands.MissingRequiredArgument):
            await ctx.send(f"Please mention a color in hex (e.g. 0xffffff)!")

    @lmsg.error
    async def lmsg_error(self, ctx, err):
        if isinstance(err, commands.MissingRequiredArgument):
            await ctx.send(f"Please Give a Message!")

    @lstatus.error
    async def ls_error(self, ctx, err):
        if isinstance(err, commands.MissingRequiredArgument):
            await ctx.send(f"Please give status 1 for enable or 2 for disable the feature!")

    @commands.command(help="Reload")
    async def refresh(self, ctx):
        await ctx.message.add_reaction('🙄')
        embed1 = discord.Embed(description="Sorry refresh is still not ready!")
        await ctx.send(embed= embed1)
        return
        PREFIX = xget_prefix(ctx)
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=PREFIX+"help"))

def setup(bot):
    bot.add_cog(Settings(bot))