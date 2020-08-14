import discord
from discord.ext import commands
import time
import random
from utils.checks import is_guild_enabled
from .triviaAPI import topic_list, topics, difficulties, Quiz
import asyncio

default_topic = topic_list[0]
default_amount = 10
default_diff = difficulties[0]

max_questions = 20

time_in_seconds = 10.0

reaction_emotes = {
    "A": "🇦",
    "B": "🇧",
    "C": "🇨",
    "D": "🇩",
    "True": "✅",
    "False": "❌"
}

choices = ["a", "b", "c", "d"]

desc = ""
desc += f"• You have {time_in_seconds} seconds to answer each question\n"
desc += "• Whoever gives the correct answer first gets one point\n"
desc += "• There are two types of questions: Yes/No, and multiple choice\n"
desc += f"• Multiple choice questions can be answered by typing the correct answer, or by typing the correct enumerator ({', '.join(choices)})\n"
desc += f"• Answering with the WRONG choice will give you 0 points instantly. Don't even try spamming the answers\n"

rules = discord.Embed(
    title = "Rules",
    color = 0xc1c100,
    description=desc
)

class TriviaSession:
    def __init__(self, ctx, quiz, parent):
        self.quiz = quiz
        self.ctx = ctx
        self.owner = self.ctx.message.author
        self.parent = parent
        self.bot = self.parent.bot
        self.current_msg = None
        self.correct_choice = -1
        self.points = {}

        self.stop = False

    async def start(self):
        self.points = {}
        i = 0

        for question in self.quiz.questions:
            if self.stop:
                break

            wrong_users = []
            def check(message, wu = wrong_users, q = question):
                if message.channel != self.ctx.channel:
                    return False
                if message.author in wu:
                    return False
                if message.content.lower() == q.answer.lower() or message.content.lower() == choices[self.correct_choice]:
                    return True
                if (message.content.lower() in [x.lower() for x in q.wrong_answers]) or (message.content.lower() in choices and q.type != "boolean"):
                    wu.append(message.author)
                    return False
                
            def idle(message):
                return False

            i += 1
            await self.render_question(question, i)
            try:
                message = await self.bot.wait_for("message", check=check, timeout=time_in_seconds)
            except asyncio.TimeoutError:
                correct_answer_text = ""
                if question.type == "multiple":
                    correct_answer_text += f"{choices[self.correct_choice].upper()}. "
                correct_answer_text += question.answer
                await self.ctx.send(f"The correct answer is **{correct_answer_text}**. Nobody gets points.")
            else:
                await self.ctx.send(f"{message.author.name} is correct! 1 point to you.")
                if message.author.name not in self.points:
                    self.points[message.author.name] = 0
                self.points[message.author.name] += 1

            try:
                await self.bot.wait_for("message", check=idle, timeout=2.0)
            except asyncio.TimeoutError:
                continue
            else:
                # Wtf happened that it got here??
                continue

        sorted_scoreboard = sorted(self.points.items(), key=lambda x: x[1], reverse=True)
        scoreboard = "```Scoreboard: \n\n"
        i = 1
        for element in sorted_scoreboard:
            scoreboard += f"{i}. {element[0]}\t\t\t{element[1]}\n"
            i += 1
        scoreboard += "```"

        await self.ctx.send(scoreboard)
        self.parent.activeObjects.pop(self.ctx.guild.id, None)

    async def render_question(self, q, i):
        title = ""
        self.correct_choice = -1
        if q.type == "boolean":
            title += "True or False? "
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
                    embed.add_field(name = f"{choices[k].upper()}. {q.answer}", value="\u200b", inline=False)
                    self.correct_choice = k
                else:
                    embed.add_field(name = f"{choices[k].upper()}. {q.wrong_answers[j]}", value="\u200b", inline=False)
                    j += 1

        embed.set_footer(text=f"{q.category} | {q.difficulty}")

        self.current_msg = await self.ctx.send(embed=embed)


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
        self.activeObjects[ctx.guild.id] = session
        await session.start()

    @trivia.command(name="stop", description="Stop a game of trivia")
    @is_guild_enabled()
    async def stop(self, ctx):
        """
        Stops a game of trivia
        """
        if ctx.guild.id not in list(self.activeObjects.keys()):
            embed = discord.Embed(
                    title = "Trivia Error",
                    description = f"There's no trivia session running",
                    color = 0xf84722
                )
            await ctx.send(embed=embed)
            return

        activeSession = self.activeObjects[ctx.guild.id]

        # Allow people with specific guild permissions to end trivia
        if ctx.message.author != activeSession.owner:
            if not ctx.author.permissions_in(ctx.channel).administrator:
                embed = discord.Embed(
                        title = "Trivia Error",
                        description = f"Only {activeSession.owner.name} or an administrator can stop this trivia session",
                        color = 0xf84722
                    )
                await ctx.send(embed=embed)
                return

        activeSession.stop = True
        self.activeObjects.pop(ctx.guild.id)     

    @trivia.command(name="rules", description="Display trivia rules", aliases=["r"])
    @is_guild_enabled()
    async def rules(self, ctx):
        await ctx.send(embed=rules)