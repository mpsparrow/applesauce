'''
Name: Emoji Commands
Description: Pile of commands to display emojis
'''

import discord
from discord.ext import commands
from util.checks import command
import random


class Emoji(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # emoji (group)
    @commands.check(command.isAllowed)
    @commands.group(name="emoji", description="Makes the bot print emojis.", usage="emoji <emoji-name>", aliases=['e'])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def emoji(self, ctx):
        pass

    # hank (subcommand)
    @emoji.command(name="hank", description="<:hank:651284638958092301>", usage="emoji hank", aliases=['h'])
    async def hank(self, ctx):
        await ctx.send('<:hank:651284638958092301>')

    # mushroom (subcommand)
    @emoji.command(name="mushroom", description="<a:mushroomDance:659932848035463198>", usage="emoji mushroom", aliases=['ms', 'shroom'])
    async def mushroom(self, ctx):
        await ctx.send('<a:mushroomDance:659932848035463198>')

    # saber (subcommand)
    @emoji.command(name="saber", description="<a:pepelightsaber:663496095065964585>", usage="emoji saber", aliases=['sb'])
    async def saber(self, ctx):
        await ctx.send('<a:pepelightsaber:663496095065964585>') 

    # thonks (subcommand)
    @emoji.command(name="thonk", description="<:thowonking:605504425083011102>", usage="emoji thonk", aliases=['t', 'think'])
    async def thonk(self, ctx):
        thonks = [
            '<:thowonking:605504425083011102>',
            '<:thonkshock:609621801412198410>',
            '<:thunk:568294885258428416>',
            '<:thonkosis:649902777925107712>',
            '<:thonkong:638800699345469451>',
            '<a:ThonkmegaSpin:638800592977920010>',
            '<:thonkLUL:649902693137252352>',
            '<:thonkfold:649902869008351256>',
            '<:nerdthink:649117561543458816>',
            '<:LennyThink:638801336284086276>',
            '<:thinkfoil:649117139667648535>',
            '<:thinkdrops:649117385818898452>',
            '<:thinkception:649117474356199424>',
            '<:eggplantThink:639570203105296394>',
            '<:OofThinking:638801365057011721>'
            ]
        await ctx.send(random.choice(thonks))

def setup(bot):
    bot.add_cog(Emoji(bot))