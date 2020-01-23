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

class wordsAPI(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # compiles URL and gets JSON
    def wordsRequest(self, word: str, ending: str):
        url = "https://wordsapiv1.p.rapidapi.com/words/" + word + "/" + ending

        conf = config.configLoad("cogconfig.json")
        headers = {
            'x-rapidapi-host': conf['wordsAPI']['key'],
            'x-rapidapi-key': conf['wordsAPI']['key']
            }

        return requests.request("GET", url, headers=headers)

    

def setup(bot):
    bot.add_cog(wordsAPI(bot))