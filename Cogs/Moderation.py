from .setup import *

class Mod(commands.Cog, name="Moderation"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(help="Clear Messages")
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, n :int =0):
        await ctx.channel.purge(limit=n+1)
        embed=discord.Embed(description=f"Successfully deleted {n} Messages :smile:", color=getEmbedColor())
        msg = await ctx.send(embed=embed)
        await msg.delete(delay=3)

    @commands.command(help="Kick a Member")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member :discord.Member, *, reason=None):
        await member.kick(reason=reason)
        await ctx.channel.send(f"{member.name} was kicked for reason: {reason}")

    @kick.error
    async def kick_error(self, ctx, err):
        if isinstance(err, commands.MissingRequiredArgument):
            await ctx.send(f"Please mention user to be kicked!")
    
    @commands.command(help="Ban a Member")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member :discord.Member, *, reason=None):
        await member.ban(reason=reason)
        await ctx.send(f"{member.name} was banned for reason: {reason}")
    
    @ban.error
    async def ban_error(self, ctx, err):
        if isinstance(err, commands.MissingRequiredArgument):
            await ctx.send(f"Please mention user to be banned!")

    @commands.command(help="Unban a member")
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx,*, member_id):
        done = 0
        banned = await ctx.guild.bans()
        for banned_ele in banned:
            user = banned_ele.user
            if user.id == int(member_id):
                await ctx.guild.unban(user)
                await ctx.send(f"{user} was unbanned!")
                done = 1
                break
        if not done:
            await ctx.send(f"{member_id} Not found in banned list!")
        
    @unban.error
    async def unban_error(self, ctx, err):
        if isinstance(err, commands.MissingRequiredArgument):
            await ctx.send(f"Please mention user to be unbanned!")
    
    #User group manage permission
    @commands.group(name="user")    
    async def user(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("Help is not still ready...")

    @user.group(name="giverole")
    @commands.has_permissions(manage_roles=True)
    async def u_giverole(self, ctx, member:discord.Member, *, role):
        role = discord.utils.get(member.guild.roles, name=str(role))
        await member.add_roles(role)
        await ctx.message.add_reaction('👍')

    @user.group(name="removereole")
    @commands.has_permissions(manage_roles=True)
    async def u_removerole(self, ctx, member:discord.Member, *, role):
        role = discord.utils.get(member.guild.roles, name=str(role))
        await member.remove_roles(role)
        await ctx.message.add_reaction('👍')

    
def setup(bot):
    bot.add_cog(Mod(bot))