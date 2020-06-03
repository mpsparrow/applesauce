import discord
from discord.ext import commands
from util import config
from util.checks import command
import random
import wolframalpha

class Wolfram(commands.Cog):
    """
    Wolfram Alpha querying command.
    """
    def __init__(self, bot):
        self.bot = bot

    # wolfram (command)
    @commands.check(command.isAllowed)
    @commands.command(name="wolfram", description="Queries Wolfram Alpha and returns the result.", usage="wolfram <query>", aliases=['wolf'])
    @commands.cooldown(1, 15, commands.BucketType.default)
    async def wolfram(self, ctx, *, question):
        """
        Command to query Wolfram Alpha and return article summary.
        :param ctx:
        :param str question:
        """
        await ctx.message.add_reaction("<a:loading:700208681685352479>") # loading message
        questionLink = 'https://www.wolframalpha.com/input/?i=' + question.strip().lower().replace(' ', '+') # builds wolfram URL (used just for link in results)

        conf = config.readINI('cogConfig.ini')
        wolframKey = conf['wolfram']['key'] # gets key list from config
        clientWolfram = wolframalpha.Client(wolframKey) # initialize API and chooses key from wolframKeys list
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

        await ctx.message.remove_reaction("<a:loading:700208681685352479>", self.bot.user) # deletes loading message
        for e in embeds:
            await ctx.send(embed=e) # sends embed

def setup(bot):
    bot.add_cog(Wolfram(bot))