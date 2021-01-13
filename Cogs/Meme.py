from .setup import *

class Meme(commands.Cog, name="Meme"):
    def __init__(self, bot):
        self.bot = bot
        self.automeme_task.start()
    
    @commands.command(name="meme")
    async def getmeme(self, ctx):
        waitmsg = await ctx.send("```Please wait...```")
        guild_db = getGuildSettings(ctx)
        res = requests.get(config['api']['meme']['url'])
        res = json.loads(res.text)
        embed = discord.Embed(title=res['title'], color=getEmbedColor(guild_db['meme_color']))
        embed.set_image(url=res['image'])
        embed.set_author(name=res['author'])
        embed.set_footer(text=f"{res['ups']} 👍 | {res['downs']} 👎")
        await waitmsg.delete()
        await ctx.send(embed=embed)
    
    @commands.command(name="memecolor")
    async def meme_color(self, ctx, color):
        new = getGuildSettings(ctx)
        new['meme_color'] = str(color)
        updateGuildSettings(ctx, new)
        await ctx.message.add_reaction('👍')

    @meme_color.error
    async def mc_error(self, ctx, err):
        if isinstance(err, commands.MissingRequiredArgument):
            await ctx.send("Please Specify a hex color!(e.g. `0x000000`)")

    @commands.group()
    async def automeme(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send(f"Use `{PREFIX}help automeme`")
    
    @automeme.group(name="channel")
    async def aset_channel(self, ctx, ch:discord.TextChannel):
        new = getGuildSettings(ctx)
        new['automeme_channel'] = ch.id
        updateGuildSettings(ctx, new)
        await ctx.message.add_reaction('👍')

    @aset_channel.error
    async def asc_error(self, ctx, err):
        if isinstance(err, commands.MissingRequiredArgument):
            await ctx.send("Please mention a `channel`")


    @automeme.group(name="status")
    async def aset_status(self, ctx, status):
        status = status.lower()
        if status == "on":
            status = 1
        elif status == "off":
            status = 0
        else:
            await ctx.send(content="Allowed values are: `on` and `off`")
            return
        new = getGuildSettings(ctx)
        new['automeme_status'] = int(status)
        updateGuildSettings(ctx, new)
        embed = discord.Embed(description="Automeme Status Updated 😄" , color=getEmbedColor(config['default_embed_color']))
        await ctx.send(embed=embed)
        await ctx.message.add_reaction('👍')

    @aset_status.error
    async def ass_error(self, ctx, err):
        await ctx.message.add_reaction(config['err_emoji'])
        if isinstance(err, commands.MissingRequiredArgument):
            await ctx.send("Please state `on` or `off`")
        else:
            embed = discord.Embed(description="It seems that system has discovered an error\nDont worry it is reported to Dev and will be fixed shortly!", color=getEmbedColor())
            tc = await self.bot.fetch_channel(config['auto_auto_trace_channel'])
            await tc.send(embed=embed)

    
    @tasks.loop(seconds=config['automeme_cooldown'])
    async def automeme_task(self):
        sql = f"SELECT `automeme_channel` FROM `{config['table']['guilds']}` WHERE `automeme_status` = 1"
        mycur.execute(sql)
        res = mycur.fetchall()
        achannels = []
        for x in res:
            achannels.append(await self.bot.fetch_channel(x['automeme_channel']))
        for achannel in achannels:
            res = requests.get(config['api']['meme']['url'])
            res = json.loads(res.text)
            embed = discord.Embed(title=res['title'], color=getEmbedColor())
            embed.set_image(url=res['image'])
            embed.set_author(name=res['author'])
            embed.set_footer(text=f"{res['ups']} 👍 | {res['downs']} 👎")
            await achannel.send(embed=embed)

def setup(bot):
    bot.add_cog(Meme(bot))