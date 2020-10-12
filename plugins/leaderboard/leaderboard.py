import discord
import random
import datetime
import pymongo
from discord.ext import commands
from utils.checks import is_guild_enabled
from utils.config import readINI
from utils.database.actions import connect

class Leaderboard(commands.Cog):
    """
    Leaderboard system
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        try:
            # Ignore bot users
            if (message.author == self.bot.user) or message.author.bot:
                return

            leaderboardCol = connect()[readINI("config.ini")["MongoDB"]["database"]]["leaderboard"] # connect to DB
            leaderboardDb = leaderboardCol.find_one({ "_id": message.guild.id })

            currentDateTime = datetime.datetime.now() - datetime.timedelta(seconds=60)
            dateYear = datetime.datetime.now().year
            dateMonth = datetime.datetime.now().month
            authorID = message.author.id

            # Get current date/time
            if leaderboardDb is None or leaderboardDb[str(message.author.id)] is None:
                lastDateTime = currentDateTime - datetime.timedelta(seconds=1)
            else:
                lastDateTime = leaderboardDb[str(authorID)]["dateTime"]

            if currentDateTime > lastDateTime:
                points = random.randint(15, 25)
                # Update leaderboard score

                if leaderboardDb is None or leaderboardDb[str(authorID)] is None:
                    leaderboardData = { 
                                        "dateTime": datetime.datetime.now(),
                                        "points": points,
                                        "messages": 1,
                                        "total_messages": 1,
                                        str(datetime.datetime.now().year): {
                                            str(datetime.datetime.now().month): {
                                                "points": points,
                                                "messages": 1,
                                                "total_messages": 1
                                            }
                                        }
                                      }
                    leaderboardCol.update_one({ "_id": message.guild.id }, { "$set": { f"{authorID}": leaderboardData }}, upsert=True)
                else:
                    if leaderboardDb[str(authorID)][str(dateYear)][str(dateMonth)] is None:
                        monthData = {
                                        str(dateMonth): {
                                            "points": points,
                                            "messages": 1,
                                            "total_messages": 1
                                        }
                                    }
                    else:
                        monthData = {
                                        str(dateMonth): {
                                            "points": leaderboardDb[str(authorID)][str(dateYear)][str(dateMonth)]["points"] + points,
                                            "messages": leaderboardDb[str(authorID)][str(dateYear)][str(dateMonth)]["messages"] + 1,
                                            "total_messages": leaderboardDb[str(authorID)][str(dateYear)][dateMonth]["total_messages"] + 1
                                        }
                                    }

                    leaderboardCol.update_one(  
                                                { "_id": message.guild.id }, 
                                                { "$set": {
                                                    f"{authorID}.{dateYear}": monthData,
                                                    f"{authorID}.dateTime": datetime.datetime.now(),
                                                    f"{authorID}.points": leaderboardDb[str(authorID)]["points"] + points,
                                                    f"{authorID}.messages": leaderboardDb[str(authorID)]["messages"] + 1,
                                                    f"{authorID}.total_messages": leaderboardDb[str(authorID)]["total_messages"] + 1
                                                }}
                                                , upsert=True)
            else:
                if leaderboardDb[str(authorID)][str(dateYear)][str(dateMonth)]["total_messages"] is None:
                    leaderboardCol.update_one({ "_id": message.guild.id }, 
                                            { "$set": {
                                                f"{authorID}.{dateYear}.{dateMonth}.total_messages": leaderboardDb[str(authorID)][str(dateYear)][str(dateMonth)]["total_messages"] + 1, 
                                                f"{authorID}.total_messages": leaderboardDb[str(authorID)]["total_messages"] + 1 
                                            }})
                else:
                    leaderboardCol.update_one({ "_id": message.guild.id }, 
                                            { "$set": {
                                                f"{authorID}.{dateYear}.{dateMonth}.total_messages": 1, 
                                                f"{authorID}.total_messages": leaderboardDb[str(authorID)]["total_messages"] + 1 
                                            }})    
        except Exception as error:
            print(error)

    @commands.command(name="rank", description="Gives current rank on the server")
    @is_guild_enabled()
    async def rank(self, ctx):
        await ctx.send(f"my rank")

    @commands.command(name="leaderboard", description="Tells you your chances of success", aliases=["levels"])
    @is_guild_enabled()
    async def leaderboard(self, ctx):
        await ctx.send(f"leaderboard")