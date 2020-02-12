'''
Name: Wikipedia
Description: Wikipedia command
Last Updated: February 11, 2020
Created: October 30, 2019
'''
import discord
from discord.ext import commands
from util import commandchecks
import wikipediaapi

class Wiki(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # wikipedia (command)
    @commands.check(commandchecks.isAllowed)
    @commands.command(name="wikipedia", description="Queries Wikipedia and returns summary and link to the page.", usage="wikipedia <query>", aliases=['wiki'])
    @commands.cooldown(1, 10, commands.BucketType.guild)
    async def wikipedia(self, ctx, *, lookup: str):
        loading = await ctx.send('Searching for article....') # loading message

        try:
            wiki = wikipediaapi.Wikipedia('en')
            wikipage = wiki.page(lookup)
            page = wiki.extracts(wikipage, exsentences=2)
            pageURL = wikipage.fullurl
            pageTitle = wikipage.title
        except:
            # if nothing is found
            page = 'No results found.'
            pageURL = '.'
            pageTitle = '.'

        # embed for results
        embed=discord.Embed(title='Wikipedia', description=f'{pageURL}', color=0xc1c100)
        embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/thumb/7/77/Wikipedia_svg_logo.svg/200px-Wikipedia_svg_logo.svg.png")
        embed.add_field(name=f'{pageTitle}', value=f'{page}', inline=False)
        await ctx.send(embed=embed)
        await loading.delete() # deletes loading message

def setup(bot):
    bot.add_cog(Wiki(bot))