from .setup import *

class Help(commands.Cog, name="Help"):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    @commands.is_owner()
    async def reload(self, ctx, ext):
        try:
            self.bot.unload_extension('Cogs.'+ext)
            self.bot.load_extension('Cogs.'+ext)
            await ctx.send(f"{ext} reloaded!")
        except Exception as e:
            print(f"Error while loading extention({ext}): {e}")
        
    @commands.group(name="help")
    async def help(self, ctx):
        if ctx.invoked_subcommand is None:
            PREFIX = getPStr(ctx)
            desc = f"You can easily setup bot for your server with commands. Just follow help 😆\nFollowing are commands and categories\nUse `{PREFIX}help <subcategory>` for detailed help!"
            embed = discord.Embed(title="Help Menu", description=desc, color=getEmbedColor())
            embed.add_field(name="Server Prefix", value=f"`{PREFIX}`", inline=False)
            embed.add_field(name="About", value=f"Use `{PREFIX}help about`", inline=True)
            embed.add_field(name="My Roles", value=f"Use `{PREFIX}help myroles`", inline=True)
            embed.add_field(name="Quick Embed", value=f"Use `{PREFIX}help qe`", inline=True)
            embed.add_field(name="Fun", value=f"Use `{PREFIX}help fun`", inline=True)
            embed.add_field(name="Meme", value=f"Use `{PREFIX}help meme`", inline=True)
            embed.add_field(name="Automeme", value=f"Use `{PREFIX}help automeme`", inline=True)
            embed.add_field(name="Moderation", value=f"Use `{PREFIX}help moderation`", inline=True)
            embed.add_field(name="Feedback", value=f"Use `{PREFIX}help feedback`", inline=True)
            embed.add_field(name="Report Bugs", value=f"Use `{PREFIX}help report`", inline=True)
            embed.add_field(name="Server Configs", value=f"Use `{PREFIX}help settings`", inline=True)
            embed.add_field(name="Todo Manager", value=f"Use `{PREFIX}help todo`", inline=True)
            embed.add_field(name="Pin Board", value=f"Use `{PREFIX}help pinboard`", inline=True)
            embed.set_footer(text=config['main_footer']+config['author'])
            await ctx.send(embed=embed)

    @help.group(name="about")
    async def help_about(self, ctx):
        embed = getStandardHelpEmbed(helps['about'], ctx)
        await ctx.send(embed=embed)
    
    @help.group(name="myroles")
    async def help_myroles(self, ctx):
        embed = getStandardHelpEmbed(helps['myroles'], ctx)
        await ctx.send(embed=embed)
    
    @help.group(name="qe")
    async def help_qe(self, ctx):
        embed = getStandardHelpEmbed(helps['qe'], ctx)
        await ctx.send(embed=embed)
    
    @help.group(name="feedback")
    async def help_feedback(self, ctx):
        embed = getStandardHelpEmbed(helps['feedback'], ctx)
        await ctx.send(embed=embed)

    @help.group(name="report")
    async def help_report(self, ctx):
        embed = getStandardHelpEmbed(helps['report'], ctx)
        await ctx.send(embed=embed)
    
    @help.group(name="fun")
    async def help_fun(self, ctx):
        if ctx.invoked_subcommand is None:
            root = helps['fun']
            PREFIX = getPStr(ctx)
            embed = discord.Embed(title=f"{root['name']} (help)", description=f"Following are sub commands", color=getEmbedColor())
            embed.add_field(name="Say", value=f"Use `{PREFIX}help fun say`", inline=True)
            embed.add_field(name="Ask", value=f"Use `{PREFIX}help fun ask`", inline=True)
            embed.add_field(name="Emoji", value=f"Use `{PREFIX}help fun emoji`", inline=True)
            embed.add_field(name="Timer", value=f"Use `{PREFIX}help fun timer`", inline=True)
            embed.set_footer(text=config['main_footer']+config['author'])
            await ctx.send(embed=embed)

    @help_fun.command(name="say")
    async def help_fun_say(self, ctx):
        embed = getStandardHelpEmbed(helps['fun']['say'], ctx)
        await ctx.send(embed=embed)

    @help_fun.command(name="ask")
    async def help_fun_ask(self, ctx):
        embed = getStandardHelpEmbed(helps['fun']['ask'], ctx)
        await ctx.send(embed=embed)
    
    @help_fun.command(name="emoji")
    async def help_fun_emoji(self, ctx):
        embed = getStandardHelpEmbed(helps['fun']['emoji'], ctx)
        await ctx.send(embed=embed)

    @help_fun.command(name="timer")
    async def help_fun_timer(self, ctx):
        embed = getStandardHelpEmbed(helps['fun']['timer'], ctx)
        await ctx.send(embed=embed)

    @help.group(name="meme")
    async def help_meme(self, ctx):
        if ctx.invoked_subcommand is None:
            root = helps['meme']
            PREFIX = getPStr(ctx)
            embed = discord.Embed(title=f"{root['name']} (help)", description=f"Following are sub commands", color=getEmbedColor())
            embed.add_field(name="Meme Embed Colour", value=f"Use `{PREFIX}help meme memecolor`", inline=True)
            embed.add_field(name="Requesting Meme", value=f"Use `{PREFIX}help meme meme`", inline=True)
            embed.set_footer(text=config['main_footer']+config['author'])
            await ctx.send(embed=embed)

    @help_meme.command(name="memecolor")
    async def help_meme_memecolor(self, ctx):
        embed = getStandardHelpEmbed(helps['meme']['memecolor'], ctx)
        await ctx.send(embed=embed)
    
    @help_meme.command(name="meme")
    async def help_meme_meme(self, ctx):
        embed = getStandardHelpEmbed(helps['meme']['meme'], ctx)
        await ctx.send(embed=embed)
    
    @help.group(name="automeme")
    async def help_automeme(self, ctx):
        if ctx.invoked_subcommand is None:
            root = helps['automeme']
            PREFIX = getPStr(ctx)
            embed = discord.Embed(title=f"{root['name']} (help)", description=f"{root['desc']}", color=getEmbedColor())
            embed.add_field(name="Automeme Channel", value=f"Use `{PREFIX}help automeme channel`", inline=True)
            embed.add_field(name="Automeme Status", value=f"Use `{PREFIX}help automeme status`", inline=True)
            embed.set_footer(text=config['main_footer']+config['author'])
            await ctx.send(embed=embed)

    @help_automeme.command(name="channel")
    async def help_automeme_channel(self, ctx):
        embed = getStandardHelpEmbed(helps['automeme']['channel'], ctx)
        await ctx.send(embed=embed)
    
    @help_automeme.command(name="status")
    async def help_automeme_status(self, ctx):
        embed = getStandardHelpEmbed(helps['automeme']['status'], ctx)
        await ctx.send(embed=embed)

    @help.group(name="moderation")
    async def help_moderation(self, ctx):
        if ctx.invoked_subcommand is None:
            root = helps['moderation']
            PREFIX = getPStr(ctx)
            embed = discord.Embed(title=f"{root['name']} (help)", description=f"Following are sub commands", color=getEmbedColor())
            embed.add_field(name="Clear Messages", value=f"Use `{PREFIX}help moderation clear`", inline=True)
            embed.add_field(name="Kick Member", value=f"Use `{PREFIX}help moderation kick`", inline=True)
            embed.add_field(name="Ban Member", value=f"Use `{PREFIX}help moderation ban`", inline=True)
            embed.add_field(name="Unban Member", value=f"Use `{PREFIX}help moderation unban`", inline=True)
            embed.add_field(name="Give Role to Member", value=f"Use `{PREFIX}help moderation gr`", inline=True)
            embed.add_field(name="Remove Role from Member", value=f"Use `{PREFIX}help moderation rr`", inline=True)
            embed.set_footer(text=config['main_footer']+config['author'])
            await ctx.send(embed=embed)

    @help_moderation.command(name="clear")
    async def help_moderation_clear(self, ctx):
        embed = getStandardHelpEmbed(helps['moderation']['clear'], ctx)
        await ctx.send(embed=embed)

    @help_moderation.command(name="kick")
    async def help_moderation_kick(self, ctx):
        embed = getStandardHelpEmbed(helps['moderation']['kick'], ctx)
        await ctx.send(embed=embed)

    @help_moderation.command(name="ban")
    async def help_moderation_ban(self, ctx):
        embed = getStandardHelpEmbed(helps['moderation']['ban'], ctx)
        await ctx.send(embed=embed)

    @help_moderation.command(name="unban")
    async def help_moderation_unban(self, ctx):
        embed = getStandardHelpEmbed(helps['moderation']['unban'], ctx)
        await ctx.send(embed=embed)

    @help_moderation.command(name="gr")
    async def help_moderation_gr(self, ctx):
        embed = getStandardHelpEmbed(helps['moderation']['giverole'], ctx)
        await ctx.send(embed=embed)

    @help_moderation.command(name="rr")
    async def help_moderation_rr(self, ctx):
        embed = getStandardHelpEmbed(helps['moderation']['removerole'], ctx)
        await ctx.send(embed=embed)
    
    @help.group(name="settings")
    async def help_settings(self, ctx):
        if ctx.invoked_subcommand is None:
            root = helps['settings']
            PREFIX = getPStr(ctx)
            embed = discord.Embed(title=f"{root['name']} (help)", color=getEmbedColor())
            embed.add_field(name="Prefix Settings", value=f"Use `{PREFIX}help settings prefix`", inline=True)
            embed.add_field(name="Join Settings", value=f"Use `{PREFIX}help settings join`", inline=True)
            embed.add_field(name="Leave Settings", value=f"Use `{PREFIX}help settings leave`", inline=True)
            embed.set_footer(text=config['main_footer']+config['author'])
            await ctx.send(embed=embed)
        
    @help_settings.command(name="prefix")
    async def help_settings_prefix(self, ctx):
        embed = getStandardHelpEmbed(helps['settings']['setprefix'], ctx)
        await ctx.send(embed=embed)
    
    @help_settings.command(name="join")
    async def help_settings_join(self, ctx, sub:str = None):
        root = helps['settings']['join']
        PREFIX = getPStr(ctx)
        jsc = ['channel', 'color', 'msg', 'status', 'addrole', 'removerole']
        if sub in jsc:
            embed = getStandardHelpEmbed(root[sub], ctx)
            await ctx.send(embed=embed)
        elif sub is None:
            embed = discord.Embed(title=f"{root['name']} (help)", description=f"{root['desc']}", color=getEmbedColor())
            embed.add_field(name="Join Channel", value=f"Use `{PREFIX}help settings join channel`", inline=True)
            embed.add_field(name="Join Embed Colour", value=f"Use `{PREFIX}help settings join color`", inline=True)
            embed.add_field(name="Join Message", value=f"Use `{PREFIX}help settings join msg`", inline=True)
            embed.add_field(name="Join Status", value=f"Use `{PREFIX}help settings join status`", inline=True)
            embed.add_field(name="Join Add Auto Role", value=f"Use `{PREFIX}help settings join addrole`", inline=True)
            embed.add_field(name="Join Remove Auto Role", value=f"Use `{PREFIX}help settings join removerole`", inline=True)
            embed.set_footer(text=config['main_footer']+config['author'])
            await ctx.send(embed=embed)
        else:
            tempmsg = await ctx.send("Invalid Help Command")
            await tempmsg.delete(delay=5)

    @help_settings.command(name="leave")
    async def help_settings_leave(self, ctx, sub:str = None):
        root = helps['settings']['leave']
        PREFIX = getPStr(ctx)
        jsc = ['channel', 'color', 'msg', 'status']
        if sub in jsc:
            embed = getStandardHelpEmbed(root[sub], ctx)
            await ctx.send(embed=embed)
        elif sub is None:
            embed = discord.Embed(title=f"{root['name']} (help)", description=f"{root['desc']}", color=getEmbedColor())
            embed.add_field(name="Leave Channel", value=f"Use `{PREFIX}help settings leave channel`", inline=True)
            embed.add_field(name="Leave Embed Colour", value=f"Use `{PREFIX}help settings leave color`", inline=True)
            embed.add_field(name="Leave Message", value=f"Use `{PREFIX}help settings leave msg`", inline=True)
            embed.add_field(name="Leave Status", value=f"Use `{PREFIX}help settings leave status`", inline=True)
            embed.set_footer(text=config['main_footer']+config['author'])
            await ctx.send(embed=embed)
        else:
            tempmsg = await ctx.send("Invalid Help Command")
            await tempmsg.delete(delay=5)

    @help.group(name="todo")
    async def help_todo(self, ctx, sub:str = None):
        root = helps['utility']['todo']
        PREFIX = getPStr(ctx)
        sc = ['add', 'remove', 'showall', 'show', 'doing', 'done', 'edit']
        if sub in sc:
            embed = getStandardHelpEmbed(root[sub], ctx)
            await ctx.send(embed=embed)
        elif sub is None:
            embed = discord.Embed(title=f"{root['name']} (help)", description=f"{root['desc']}", color=getEmbedColor())
            embed.add_field(name="Add", value=f"Use `{PREFIX}help todo add`", inline=True)
            embed.add_field(name="Remove", value=f"Use `{PREFIX}help todo remove`", inline=True)
            embed.add_field(name="Show All", value=f"Use `{PREFIX}help todo showall`", inline=True)
            embed.add_field(name="Show", value=f"Use `{PREFIX}help todo show`", inline=True)
            embed.add_field(name="Doing", value=f"Use `{PREFIX}help todo doing`", inline=True)
            embed.add_field(name="Done", value=f"Use `{PREFIX}help todo done`", inline=True)
            embed.add_field(name="Edit", value=f"Use `{PREFIX}help todo edit`", inline=True)
            embed.set_footer(text=config['main_footer']+config['author'])
            await ctx.send(embed=embed)
        else:
            tempmsg = await ctx.send("Invalid Help Command")
            await tempmsg.delete(delay=5)
        
    @help.group(name="todoedit")
    async def help_todoedit(self, ctx, sub:str = None):
        root = helps['utility']['todoedit']
        PREFIX = getPStr(ctx)
        sc = ['title', 'desc']
        if sub in sc:
            embed = getStandardHelpEmbed(root[sub], ctx)
            await ctx.send(embed=embed)
        elif sub is None:
            embed = discord.Embed(title=f"{root['name']} (help)", color=getEmbedColor())
            embed.add_field(name="Edit Title", value=f"Use `{PREFIX}help todoedit title`", inline=True)
            embed.add_field(name="Edit Description", value=f"Use `{PREFIX}help todoedit desc`", inline=True)
            embed.set_footer(text=config['main_footer']+config['author'])
            await ctx.send(embed=embed)
        else:
            tempmsg = await ctx.send("Invalid Help Command")
            await tempmsg.delete(delay=5)

    @help.group(name="pinboard")
    async def help_pinboard(self, ctx, sub:str = None):
        root = helps['utility']['pinboard']
        PREFIX = getPStr(ctx)
        sc = ['pin', 'pinchannel']
        if sub in sc:
            embed = getStandardHelpEmbed(root[sub], ctx)
            await ctx.send(embed=embed)
        elif sub is None:
            embed = discord.Embed(title=f"{root['name']} (help)", description=f"{root['desc']}", color=getEmbedColor())
            embed.add_field(name="Pin Message", value=f"Use `{PREFIX}help pinboard pin`", inline=True)
            embed.add_field(name="Set pinboard Channel", value=f"Use `{PREFIX}help pinboard pinchannel`", inline=True)
            embed.set_footer(text=config['main_footer']+config['author'])
            await ctx.send(embed=embed)
        else:
            tempmsg = await ctx.send("Invalid Help Command")
            await tempmsg.delete(delay=5)

def setup(bot):
    bot.add_cog(Help(bot))