import discord
from discord.ext import commands
from . import configloader
import random
import wolframalpha
import wikipedia
import json

class API(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # wikipedia command
    @commands.command(aliases=['wikipedia'])
    @commands.cooldown(1, 10, commands.BucketType.default)
    async def wiki(self, ctx, *, lookup):
        loading = await ctx.send('loading....') # loading message

        try:
            page = wikipedia.summary(lookup, sentences=1) # gets pages first sentence
            wikiPage = wikipedia.page(lookup)
            pageURL = wikiPage.url # gets pages URL
            pageTitle = wikiPage.title
        except:
            # if nothing is found
            page = 'No results found.'
            pageURL = '....'
            pageTitle = '....'

        # embed for results
        embed=discord.Embed(title='Wikipedia', description=f'{pageURL}', color=0xc1c100)
        embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/en/thumb/8/80/Wikipedia-logo-v2.svg/1200px-Wikipedia-logo-v2.svg.png")
        # embed.add_field(name='Lookup', value=f'{lookup}', inline=False)
        embed.add_field(name=f'{pageTitle}', value=f'{page}', inline=False)
        await ctx.send(embed=embed)

        await loading.delete() # deletes loading message

    # wolfram command
    @commands.command(aliases=['wolf'])
    @commands.cooldown(1, 20, commands.BucketType.default)
    async def wolfram(self, ctx, *, question):
        loading = await ctx.send('loading....') # loading message
        questionLink = 'https://www.wolframalpha.com/input/?i=' + question.strip().lower().replace(' ', '+') # builds wolfram URL (used just for link in results)

        wolframKeys = json.loads(configloader.config.get("api","keys")) # gets key list from config
        clientWolfram = wolframalpha.Client(wolframKeys[random.randint(0,len(wolframKeys)-1)]) # initialize API and choose key from wolframKeys list
        res = clientWolfram.query(question) # sends a query with the question

        embeds = []

        # builds embed for results
        embed=discord.Embed(title='Wolfram Alpha', description=f'{questionLink}', color=0xc1c100)
        embed.set_thumbnail(url="https://images-na.ssl-images-amazon.com/images/I/41kS+WGH8TL.png")
        # embed.add_field(name='Question', value=f'{question}', inline=False)
        embeds.append(embed)

        MAX_PODS = 3
        try:
            count = 1
            for r in res.pods:
                e=discord.Embed(title=r['@title'], color=0xc1c100)
                for sub in r.subpods:
                    for img in sub.img:
                        e.set_image(url=img['@src'])
                        embeds.append(e)
                        break;
                    break;

                if count == MAX_PODS:
                    break
                count += 1

            embeds = embeds[:3]
        except:
            e=discord.Embed(title='Result', description='No results found.', color=0xc1c100)
            embeds.append(e)

        await loading.delete() # deletes loading message
        for e in embeds:
            await ctx.send(embed=e) # sends embed

def setup(bot):
    bot.add_cog(API(bot))
