import discord
from discord.ext import commands
import time
import random
from utils.checks import is_guild_enabled
from .triviaAPI import topic_list, topics, difficulties, Quiz

default_topic = topic_list[0]
default_amount = 10
default_diff = difficulties[0]

max_questions = 20

reaction_emotes = {
    "A": "🇦",
    "B": "🇧",
    "C": "🇨",
    "D": "🇩",
    "True": "✅",
    "False": "❌"
}

class TriviaSession:
    def __init__(self, ctx, quiz, parent):
        self.quiz = quiz
        self.ctx = ctx
        self.parent = parent
        self.current_msg = None

    async def start(self):
        i = 0
        for question in self.quiz.questions:
            i += 1
            await self.render_question(question, i)
            time.sleep(5)
            print("jksjdksd")

        self.parent.activeObjects.pop(self.ctx.guild.id, None)

    async def render_question(self, q, i):
        title = ""
        if q.type == "boolean":
            title += "True or False?"
        title += q.question

        embed = discord.Embed(
                title = f"Question {i}",
                description = title,
                color = 0xc1c100
            )

        if q.type == "multiple":
            true_position = random.randint(0, 3)
            j = 0
            for k in range(0, 4):
                if k == true_position:
                    embed.add_field(name = f"{chr(65 + k)}. {q.answer}", value="\u200b", inline=False)
                else:
                    embed.add_field(name = f"{chr(65 + k)}. {q.wrong_answers[k]}", value="\u200b", inline=False)
                    k += 1

        embed.set_footer(text=f"{q.category} | {q.difficulty}")

        self.current_msg = await self.ctx.send(embed=embed)
        if q.type == "multiple":
            await self.current_msg.add_reaction(reaction_emotes["A"])
            await self.current_msg.add_reaction(reaction_emotes["B"])
            await self.current_msg.add_reaction(reaction_emotes["C"])
            await self.current_msg.add_reaction(reaction_emotes["D"])
        else:
            await self.current_msg.add_reaction(reaction_emotes["True"])
            await self.current_msg.add_reaction(reaction_emotes["False"])



class Trivia(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.activeObjects = {}

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
            description = f"`{', '.join(list(topics))}`",
            color = 0xc1c100
        )
        await ctx.send(embed=embed)

    @trivia.command(name="start", description="Start a game of trivia", usage="[topic] [questions] [difficulty]", aliases=["s"])
    @is_guild_enabled()
    async def start(self, ctx, 
        topic: str = None, 
        amount: int = default_amount, 
        difficulty: str = None):
        """
        Start a game of trivia
        """
        if ctx.guild.id in list(self.activeObjects.keys()):
            embed = discord.Embed(
                    title = "Trivia Error",
                    description = f"There's already a trivia session running",
                    color = 0xf84722
                )
            await ctx.send(embed=embed)
            return

        if topic is not None:
            if topic.lower() not in topic_list:
                embed = discord.Embed(
                    title = "Trivia Error",
                    description = f"Category `{topic}` doesn't exist. Use `trivia list` to see all categories.",
                    color = 0xf84722
                )
                await ctx.send(embed=embed)
                return

        if amount < 1 or amount > max_questions:
            embed = discord.Embed(
                title = "Trivia Error",
                description = f"Invalid amount of questions. Specify a number between 1 and {max_questions}",
                color = 0xf84722
            )
            await ctx.send(embed=embed)
            return

        if difficulty is not None:
            if difficulty.lower() not in difficulties:
                embed = discord.Embed(
                    title = "Trivia Error",
                    description = f"Difficulty `{difficulty}` doesn't exist. Choose `Easy`, `Medium`, `Hard`",
                    color = 0xf84722
                )
                await ctx.send(embed=embed)
                return
        
        quiz = Quiz(topic, amount, difficulty)
        session = TriviaSession(ctx, quiz, self)
        await session.start()
        self.activeObjects[ctx.guild.id] = session