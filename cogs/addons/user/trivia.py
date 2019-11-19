import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
from cogs.utils import checks
import asyncio
import os
import random

class Quiz():
    def __init__(self, ctx, amount=5, delay=8):
        self.ctx = ctx
        self.questions = []
        self.question = ""
        self.amount = amount
        self.delay = delay

    def load_questions(self, file):
        path = os.path.abspath(f"./cogs/addons/user/trivia/{file}.txt")
        lines = open(path, encoding='utf-8').read().splitlines()
        for items in lines:
            self.questions.append(items.split('\t'))

    def ask_question(self):
        self.question = random.choice(self.questions)
        self.questions.remove(self.question)
        return self.question[0]

    def answer_question(self):
        return self.question[1]

    def quiz_amount(self):
        self.amount -= 1

    def is_quiz_over(self):
        if self.amount <= 0:
            return True
        return False

class Trivia(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # userinfo command
    @commands.check(checks.allowedGuild)
    @commands.command(name="trivia", description="select and play some trivia", usage="trivia type")
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def trivia(self, ctx, *, trivia=""):

        # reads all trivia txt files in trivia folder
        triviaList = []
        for required in os.listdir('./cogs/addons/user/trivia'):
            if required.endswith('.txt'): # if a .txt file is found
                triviaList.append(required[:-4])

        if len(triviaList) == 0:
            await ctx.send("no trivia loaded")
        elif trivia.lower() in triviaList:
            triv = Quiz(ctx)
            triv.load_questions(trivia)
            await ctx.send(triv.ask_question())
            await asyncio.sleep(triv.delay)
            await ctx.send(triv.answer_question())
        else:
            triviaText = ""
            for item in triviaList:
                triviaText += "`" + item + "` "
            embed=discord.Embed(title='Trivia', description='use: `trivia list` to start a trivia', color=0xc1c100)
            embed.add_field(name='Trivia List', value=f'{triviaText}', inline=False)
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Trivia(bot))
