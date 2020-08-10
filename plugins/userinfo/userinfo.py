import discord
from discord.ext import commands
from utils.checks import is_guild_enabled

status_emotes = {
    discord.Status.online: "🟢",
    discord.Status.idle: "🟠",
    discord.Status.dnd: "🔴",
    discord.Status.offline: "⚫",
    discord.Status.invisible: "🕵️‍♂️"
}

class Userinfo(commands.Cog):
    """
    Displays user information
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="userinfo", description="Get information about discord users", usage="userinfo <user>", aliases=["player", "user"])
    @is_guild_enabled()
    async def userinfo(self, ctx: commands.Context, user: discord.Member = None):
        if user == None:
            user = ctx.author

        embed = discord.Embed(
            title=f"{user.display_name} {status_emotes[user.status]}",
            colour=user.colour,
            description=f"{user.name}#{user.discriminator}"
        )
        embed.set_thumbnail(url=user.avatar_url)
        embed.add_field(name='Guild member since', value=f'{user.joined_at.strftime("%B %d, %Y %H:%M:%S")}', inline=True)
        embed.add_field(name='Discord user since', value=f'{user.created_at.strftime("%B %d, %Y %H:%M:%S")}', inline=True)
        embed.set_footer(text=f'ID {user.id}')
        await ctx.send(embed=embed)