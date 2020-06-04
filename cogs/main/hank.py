import discord
from discord.ext import commands
import random
import time
from util.db.query import queryChannel
from util.db.insert import insertChannel

class Hank(commands.Cog):
    """
    Hanks when you hank.
    """
    def __init__(self, bot):
        self.bot = bot
        self.hankTimer = 0
        self.randomVal = 0

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if ("<:hank:" in message.content):
            if queryChannel.status(message.channel.id, message.guild.id, "hank"):
                if ((time.time() - self.hankTimer) > self.randomVal)):
                    self.hankTimer = time.time()
                    self.randomVal = random.randint(240, 900)
                    channel = self.bot.get_channel(message.channel.id)
                    await channel.send("<:hank:461015208224358440>")
                    return

    @commands.check(command.isAllowed)
    @commands.has_permissions(manage_guild=true)
    @commands.command(name="hankEnable", description="Enable channel for hank reaction.", usage="hankEnable <channelID>")
    async def hankEnable(self, ctx):
        try:
            insertChannel.channel(ctx.channel.id, ctx.guild.id, "hank", True)
            await ctx.message.add_reaction("✅")
        except:
            await ctx.message.add_reaction("❌")

    @commands.check(command.isAllowed)
    @commands.has_permissions(manage_guild=true)
    @commands.command(name="hankDisable", description="Disable channel for hank reaction.", usage="hankDisable <channelID>")
    async def hankDisable(self, ctx):
        try:
            insertChannel.channel(ctx.channel.id, ctx.guild.id, "hank", True)
            await ctx.message.add_reaction("✅")
        except:
            await ctx.message.add_reaction("❌")
    
def setup(bot):
    bot.add_cog(Hank(bot))