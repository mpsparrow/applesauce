'''
Name: Resource Logger
Description: Logs resource usage of server. Made to work with srLogger
Last Updated: January 29, 2020
Created: January 29, 2020
'''
import discord
from discord.ext import commands
import matplotlib.pyplot as plt

class resourceLogger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="resourceUsage", description="Outputs resource usage of server.", usage="resources <subcommand>", aliases=['usage', 'ru', 'resources'])
    @commands.is_owner()
    async def resourceUsage(self, ctx, subcmd):

    @resourceUsage.command(name="cpu", description="Shows CPU server usage stats", usage="resources cpu", aliases=['c'])
    async def cpu(self, ctx):

def setup(bot):
    bot.add_cog(resourceLogger(bot))