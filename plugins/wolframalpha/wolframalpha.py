import discord
from discord.ext import commands
from utils.checks import is_guild_enabled

class WolframAlpha(commands.Cog):
    def __init__(self, bot):
        self.bot = bot