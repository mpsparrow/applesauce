import discord
from discord.ext import commands
from util import embed, config
from util.checks import command
import requests
import json

class wordsAPI(commands.Cog):
    """
    Word related querying command.
    """
    def __init__(self, bot):
        self.bot = bot

    # compiles URL, gets JSON result
    def wordsRequest(self, word, ending):
        url = f"https://wordsapiv1.p.rapidapi.com/words/{word}/{ending}"
        conf = config.readINI("cogConfig.ini")
        headers = conf['wordsAPI']
        response = requests.request("GET", url, headers=headers)
        return response.text

    @commands.check(command.isAllowed)
    @commands.group(name="words", description="Gets information and definition of words.", usage="words <subcommand> <word>", aliases=['w', 'word'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def words(self, ctx):
        pass

    @words.command(name="define", description="Returns a definition of the word provided.", usage="words define <word>", aliases=['d'])
    async def define(self, ctx, *, word):
        data = json.loads(self.wordsRequest(str(word), "definitions"))
        definitions = ""

        # attempts to retrieve first 3 definitions
        for i in range(0, 3):
            try:
                definitions += f"**{i+1}.** {data['definitions'][i]['definition']}\n"
            except:
                pass
        
        # if no definitions found
        if len(definitions) == 0:
            definitions = "No definitions found."
            embedDef = embed.make_embed(word, definitions)
        else:
            embedDef = embed.make_embed(data['word'], definitions)

        await ctx.send(embed=embedDef)

def setup(bot):
    bot.add_cog(wordsAPI(bot))