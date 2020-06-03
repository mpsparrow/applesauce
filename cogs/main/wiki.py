import aiohttp
import asyncio
import discord
from discord.ext import commands
from util.checks import command

class Wiki(commands.Cog):
    """
    Wikipedia querying command.
    """
    def __init__(self, bot):
        self.bot = bot

    # wikipedia (command)
    @commands.check(command.isAllowed)
    @commands.command(name="wikipedia", description="Queries Wikipedia and returns summary.", usage="wikipedia <query>", aliases=['wiki'])
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def wikipedia(self, ctx, *, lookup: str):
        """
        Command to query Wikipedia and return article summary.
        :param ctx:
        :param str lookup:
        """
        await ctx.message.add_reaction("<a:loading:700208681685352479>") # loading message
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{lookup}"

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as r:
                if r.status == 200:
                    js = await r.json()

                    embed=discord.Embed(title='Wikipedia', description=f"{js['content_urls']['desktop']['page']}", color=0xc1c100)
                    embed.add_field(name=f"{js['displaytitle']}", value=f"{js['extract']}", inline=False)
                    await ctx.send(embed=embed)
                else:
                    await ctx.message.add_reaction("⚠️")

        await ctx.message.remove_reaction("<a:loading:700208681685352479>", self.bot.user) # deletes loading message

def setup(bot):
    bot.add_cog(Wiki(bot))