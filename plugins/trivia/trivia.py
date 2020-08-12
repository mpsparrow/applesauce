import discord
from discord.ext import commands
from utils.checks import is_guild_enabled
from .triviaAPI import Quiz

class Trivia(commands.Cog):
    default_topic = Quiz.topic_list[0]
    default_amount = 10
    default_diff = Quiz.difficulties[0]

    max_questions = 20

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
            description = f"`{', '.join(Quiz.topic_list)}`",
            color = 0xc1c100
        )
        await ctx.send(embed=embed)

    @trivia.command(name="start", description="Start a game of trivia", usage="[topic] [questions] [difficulty]", aliases=["s"])
    @is_guild_enabled()
    async def start(self, ctx, topic: str = default_topic, amount: str = default_amount, difficulty: str = default_diff):
        """
        Start a game of trivia
        """
        if topic not in Quiz.topic_list:
            await