'''
Name: Wikipedia
Description: Wikipedia command
'''

import aiohttp
import asyncio
import discord
from discord.ext import commands
from util import commandchecks


class Wiki(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # wikipedia (command)
    @commands.check(commandchecks.isAllowed)
    @commands.command(name="wikipedia", description="Queries Wikipedia and returns summary and link to the page.", usage="wikipedia <query>", aliases=['wiki'])
    @commands.cooldown(1, 10, commands.BucketType.guild)
    async def wikipedia(self, ctx, *, lookup: str):
        loading = await ctx.send('Searching for article....') # loading message
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{lookup}"

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as r:
                if r.status == 200:
                    js = await r.json()

                    embed=discord.Embed(title='Wikipedia', description=f"{js['content_urls']['desktop']['page']}", color=0xc1c100)
                    embed.add_field(name=f"{js['displaytitle']}", value=f"{js['extract']}", inline=False)
                    await ctx.send(embed=embed)
                else:
                    await ctx.send("no result found")

        await loading.delete() # deletes loading message

def setup(bot):
    bot.add_cog(Wiki(bot))