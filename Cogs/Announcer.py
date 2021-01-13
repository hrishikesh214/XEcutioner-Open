from .setup import *

class Announcer(commands.Cog, name="Announcer"):

    def __init__(self, bot):
        self.bot = bot
    
    @commands.group(name="ue")
    # @commands.is_owner()
    async def update_embed(self, ctx):
        if ctx.invoked_subcommand is None:
            with open(utility_db, 'r', encoding='utf-8') as ur:
                u = json.load(ur)
            u = u['updatepost']
            author = await self.bot.fetch_user(config['authorid'])
            time = datetime.datetime.now()
            embed = discord.Embed(title=u['title'], description=u['description'], color=getEmbedColor())
            embed.set_footer(text=config['main_footer']+config['author']+f" | {time.strftime('%I:%M %p %x')}", icon_url=author.avatar_url)
            await ctx.send(embed=embed)
        
    @update_embed.command(name="title")
    async def ue_title(self, ctx, *, title):
        if title is None:
            title = ""
        with open(utility_db, 'r', encoding='utf-8') as ur:
            u = json.load(ur)
        u['updatepost']['title'] = title
        with open(utility_db, 'w', encoding='utf-8') as ur:
            json.dump(u, ur, indent=4)
        await ctx.message.add_reaction('👍')

    @update_embed.command(name="desc")
    async def ue_desc(self, ctx, *, desc):
        if desc is None:
            desc = ""
        with open(utility_db, 'r', encoding='utf-8') as ur:
            u = json.load(ur)
        u['updatepost']['description'] = desc
        with open(utility_db, 'w', encoding='utf-8') as ur:
            json.dump(u, ur, indent=4)
        await ctx.message.add_reaction('👍')
    
    @update_embed.command(name="announce")
    async def ue_announce(self, ctx):
        waitmsg = await ctx.send("`Getting Data...`")
        with open(utility_db, 'r', encoding='utf-8') as ur:
            u = json.load(ur)
        u = u['updatepost']
        time = datetime.datetime.now()
        author = await self.bot.fetch_user(config['authorid'])
        embed = discord.Embed(title=u['title'], description=u['description'], color=getEmbedColor())
        embed.set_footer(text=config['main_footer']+config['author']+f" | {time.strftime('%I:%M %p %x')}", icon_url=author.avatar_url)
        await waitmsg.edit(content="`Fetching channels...`")
        sql = f"SELECT `private_channel` FROM `{config['table']['guilds']}` WHERE `private_channel` != 0"
        mycur.execute(sql)
        xchans = mycur.fetchall()
        await waitmsg.edit(content="`Sending...`")
        count = 0
        notsend = 0
        for xchan in xchans:
            await waitmsg.edit(content=f"`Sending... {count} Done`")
            try:
                to = await self.bot.fetch_channel(xchan['private_channel'])
                await to.send(embed=embed)
                count += 1
            except Exception as e:
                notsend += 1
        await ctx.message.add_reaction('👍')
        await ctx.send(f"`{count}` Recieved While `{notsend}` got some error")
        await waitmsg.delete()
    
    @update_embed.error
    async def ue_tracer(self, ctx, err):
        embed = discord.Embed(description="It seems that system has discovered an error\nDont worry it is reported to Dev and will be fixed shortly!", color=getEmbedColor())
        tc = await self.bot.fetch_channel(config['auto_trace_channel'])
        await tc.send(embed=embed)

def setup(bot):
    bot.add_cog(Announcer(bot))