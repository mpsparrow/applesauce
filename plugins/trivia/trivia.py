import discord
from discord.ext import commands
from utils.checks import is_guild_enabled
from .triviaAPI import Quiz

class Trivia(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="trivia", description="Play a game of trivia!", usage="<subcommand>", aliases=["t"], invoked_subcommand=True)
    @is_guild_enabled()
    async def trivia(self, ctx):
        """
        
        """

    @trivia.command(name="list", description="List all the categories", usage="", aliases=["l"])
    @is_guild_enabled()
    async def list(self, ctx):
        """
        List all trivia categories
        """
        embed = discord.Embed(
            title = "Trivia categories",
            description = f"`{', '.join(list(Quiz.topics.keys()))}`",
            color = 0xc1c100
        )
        await ctx.send(embed=embed)
