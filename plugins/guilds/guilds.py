import discord
from discord.ext import commands
from utils.database.actions import connect

class Guilds(commands.Cog):
    """
    Guild management commands
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(guild):
        # sends join message with getting started information
        await ctx.send(f"**Thanks for adding me!**\n**Prefix:** `!`\n**Help:** `!help`")

    @commands.Cog.listener()
    async def on_guild_remove(guild):
        return

    @commands.Cog.listener()
    async def on_guild_update(before, after):
        return