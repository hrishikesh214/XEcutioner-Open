from .setup import *

class Feedback(commands.Cog, name="Feedback"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="feedback")
    async def feedback(self, ctx, *, fb):
        author = ctx.message.author
        guild = ctx.guild
        fbchannel = self.bot.get_channel(config['feedback_channel'])
        embed = discord.Embed(title = "Feedback")
        embed.add_field(name="From", value=author.mention, inline=False)
        embed.add_field(name="Server", value=guild.name, inline=False)
        embed.add_field(name="Server Id", value=guild.id, inline=False)
        embed.add_field(name="Message", value=fb, inline=False)
        await fbchannel.send(embed=embed)
        await ctx.message.add_reaction('👍')
        await ctx.send(f"`Hey` {author.mention}, Thanks for giving your Feedback 😄")
    
    @feedback.error
    async def fb_error(self, ctx, err):
        if isinstance(err, commands.MissingRequiredArgument):
            await ctx.send("Please give a `Feedback Message`")
        
    @commands.command(name="report")
    async def report_bug(self, ctx, *, re):
        author = ctx.message.author
        guild = ctx.guild
        fbchannel = self.bot.get_channel(config['feedback_channel'])
        embed = discord.Embed(title = "Error Reported")
        embed.add_field(name=f"From", value=f"{author.mention}", inline=False)
        embed.add_field(name="Server", value=guild.name, inline=False)
        embed.add_field(name="Server Id", value=guild.id, inline=False)
        embed.add_field(name=f"Message", value=f"{re}", inline=False)
        await fbchannel.send(embed=embed)
        await ctx.message.add_reaction('👍')
        await ctx.send(f"`Hey` {author.mention}, Thanks for Reporting a Bug 😄 We will fix it ASAP")
    
    @report_bug.error
    async def re_error(self, ctx, err):
        if isinstance(err, commands.MissingRequiredArgument):
            await ctx.send("Please give a `Feedback Message`")

def setup(bot):
    bot.add_cog(Feedback(bot))