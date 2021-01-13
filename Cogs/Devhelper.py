from .setup import *
import re

class Devhelper(commands.Cog, name="Devhelper"):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="request")
    async def request(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("help not ready...")
    
    @request.command(name="get")
    async def r_get(self, ctx, url):
        waitmsg = await ctx.send("`Please Wait...`")
        try:
            res = requests.get(url)
            await waitmsg.edit(content=f"`Loading...`")
            res = json.loads(res.text)
            res = json.dumps(res, indent=4)
            res = res.replace("```", "\`\`\`")
            now = datetime.datetime.now()
            embed = discord.Embed(title=f"GET Request to {url}", color=getEmbedColor())
            embed.add_field(name="Output", value=f"```json\n{res}\n```", inline=False)
            embed.set_footer(text=f"Requested by {ctx.author.name} | {now.strftime('%I:%M %p %x')}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
        except Exception as e:
            embed = discord.Embed(description="It seems that system has discovered an error\nDont worry it is reported to Dev and will be fixed shortly!", color=getEmbedColor())
            tc = await self.bot.fetch_channel(config['auto_trace_channel'])
            print(e)
            await tc.send(embed=embed)
        await waitmsg.delete()

def setup(bot):
    bot.add_cog(Devhelper(bot))