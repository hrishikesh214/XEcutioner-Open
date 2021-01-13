from .setup import *

class Fun(commands.Cog, name="Fun"):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def emoji(self, ctx):
        await ctx.message.add_reaction('😄')
        await ctx.channel.send(random.choice(emojis))

    @commands.command(help="Answers if found in Database")
    async def ask(self, ctx, * , question):
        for reply in replies:
            if str(reply).lower() in str(question).lower():
                await ctx.message.add_reaction('😄')
                await ctx.send(replies[reply])
                return
        await ctx.send("Sorry I dont have any reply in my Database 😔")

def setup(bot):
    bot.add_cog(Fun(bot))