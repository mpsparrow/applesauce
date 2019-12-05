import discord
import asyncio
import os
import random
import time
from discord.ext import commands
from discord.ext.commands import has_permissions
from cogs.utils import commandchecks

# main class for trivia
class Quiz():
    def __init__(self, ctx, amount, delay):
        self.ctx = ctx
        self.questions = []
        self.question = ""
        self.answers = ""

        if round(abs(amount)) > 15:
            self.amount = 15
        elif round(abs(amount)) == 0:
            self.amount = 1
        else:
            self.amount = round(abs(amount))

        if round(abs(delay)) > 20:
            self.delay = 20
        elif round(abs(delay)) < 2:
            self.delay = 2
        else:
            self.delay = round(abs(delay))

    # loads trivia file
    def load_questions(self, file):
        path = os.path.abspath(f"./cogs/main/assets/trivia/{file}.txt")
        lines = open(path, encoding='utf-8').read().splitlines()
        for items in lines:
            tmp = items.split('\t')
            for i in tmp:
                if i == "":
                    tmp.remove(i)
            self.questions.append(tmp)

    # picks random question from trivia file
    def ask_question(self):
        self.question = random.choice(self.questions)
        self.questions.remove(self.question)
        self.answers = self.question[1:]
        return self.question[0]

    # correct answer for question
    def answer_question(self):
        return self.question[1]

    # amount of questions for travia instance
    def amount_questions(self):
        self.amount -= 1

    # checks if trivia is done
    def is_over(self):
        if self.amount <= 0:
            return True
        return False

    # ends trivia
    def end_now(self):
        self.amount = 0

# Cog for trivia commands
class Trivia(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # main trivia command
    @commands.check(commandchecks.isAllowed)
    @commands.command(name="trivia", description="Select a category and play some trivia. Use `trivia` for a list of categories.", usage="trivia <category> <#questions> <timelimit>")
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def trivia(self, ctx, trivia="", amount=10, delay=10):

        # reads all trivia txt files in trivia folder
        triviaList = []
        for required in os.listdir('./cogs/main/assets/trivia'):
            if required.endswith('.txt'): # if a .txt file is found
                triviaList.append(required[:-4])

        if len(triviaList) == 0:
            await ctx.send("no trivia loaded")
        elif trivia.lower() in triviaList:
            await self.trivia_runner(ctx, trivia, amount, delay) # starts trivia
        else:
            triviaText = ""
            for item in triviaList:
                triviaText += "`" + item + "` "
            embed=discord.Embed(title='Trivia', description='use: `trivia list` to start a trivia', color=0xc1c100)
            embed.add_field(name='Trivia List', value=f'{triviaText}', inline=False)
            await ctx.send(embed=embed)

    # function to run through trivia questions
    async def trivia_runner(self, ctx, trivia, amount, delay):
        triv = Quiz(ctx, amount, delay)
        triv.load_questions(trivia)
        correctans = 0
        await asyncio.sleep(1)
        while triv.is_over() == False:
            await ctx.send(triv.ask_question())
            triv.amount -= 1
            def pred(m):
                answers=[]
                for i in triv.answers:
                    answers.append(i.lower())
                return any(ele in m.content.lower() for ele in answers) and m.channel == ctx.channel
            try:
                msg = await self.bot.wait_for('message', timeout=triv.delay, check=pred)
                correctans += 1
                await ctx.send("Correct!")
            except asyncio.TimeoutError:
                await ctx.send(f'Answer: {triv.answer_question()}')
            await asyncio.sleep(2)
        await ctx.send(f'All Done :)   Correct Answers: {correctans}')

def setup(bot):
    bot.add_cog(Trivia(bot))