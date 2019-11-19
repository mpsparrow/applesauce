import discord
import asyncio
import os
import random
from discord.ext import commands
from discord.ext.commands import has_permissions
from cogs.utils import checks

class Quiz():
    def __init__(self, ctx, amount, delay):
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
            
        # # check if blank items are about to be appended
        # # should probably change this all to use ` as a separator instead
        # for items in lines:
        #     item = items.split('\t')
        #     if item != "":
        #         self.questions.append(items.split('\t'))

    def ask_question(self):
        self.question = random.choice(self.questions)
        self.questions.remove(self.question)
        return self.question[0]

    def answer_question(self):
        return self.question[1]

    def amount_questions(self):
        self.amount -= 1

    def is_over(self):
        if self.amount <= 0:
            return True
        return False

    def is_correct(self, answer):
        if any(self.question[1:] in answer.split() for answer in list_):
            return True
        return False

class Trivia(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # userinfo command
    @commands.check(checks.allowedGuild)
    @commands.command(name="trivia", description="Select a category and play some trivia. Default values: amountofquestions = 10, delay = 8", usage="trivia category amountofquestions timeforquestion")
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def trivia(self, ctx, trivia="", amount=10, delay=8):

        # reads all trivia txt files in trivia folder
        triviaList = []
        for required in os.listdir('./cogs/addons/user/trivia'):
            if required.endswith('.txt'): # if a .txt file is found
                triviaList.append(required[:-4])

        if len(triviaList) == 0:
            await ctx.send("no trivia loaded")
        elif trivia.lower() in triviaList:
            triv = Quiz(ctx, amount, delay)
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
