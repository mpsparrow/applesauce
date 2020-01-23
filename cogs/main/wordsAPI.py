'''
Name: Words API
Description: Links up with WordsAPI to provide dictionary and word lookup commands
Last Updated: January 23, 2020
Created: January 23, 2020
'''
import discord
from discord.ext import commands
from utils import commandchecks, embed, config
import requests
import json

class wordsAPI(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # compiles URL and gets JSON
    def wordsRequest(self, word, ending):
        url = f"https://wordsapiv1.p.rapidapi.com/words/{word}/{ending}"
        conf = config.configLoad("cogconfig.json")
        headers = conf['wordsAPI']
        response = requests.request("GET", url, headers=headers)
        return response.text

    # words group command
    @commands.check(commandchecks.isAllowed)
    @commands.group(name="words", description="Gets information and definition of words.", usage="words <subcommand> <word>", aliases=['w', 'word'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def words(self, ctx):
        pass

    # definition subcommand
    @words.command(name="define", description="Returns a definition of the word provided.", usage="words define <word>", aliases=['d'])
    async def define(self, ctx, word):
        data = json.loads(self.wordsRequest(str(word), "definitions"))
        definitions = ""

        for i in range(0, 3):
            try:
                definitions += f"**{i+1}.** {data['definitions'][i]['definition']}\n"
            except:
                pass
        
        if len(definitions) == 0:
            definitions = "No definitions found."
            embedDef = embed.make_embed(word, definitions)
        else:
            embedDef = embed.make_embed(data['word'], definitions)

        await ctx.send(embed=embedDef)

def setup(bot):
    bot.add_cog(wordsAPI(bot))