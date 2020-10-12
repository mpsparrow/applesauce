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
            dateYearX = str(datetime.datetime.now().year)
            dateMonth = str(datetime.datetime.now().month)

            # Get current date/time
            if leaderboardDb is None or leaderboardDb[str(message.author.id)] is None:
                lastDateTime = currentDateTime - datetime.timedelta(seconds=1)
            else:
                lastDateTime = leaderboardDb[str(message.author.id)]["dateTime"]

            if currentDateTime > lastDateTime:
                points = random.randint(15, 25)
                # Update leaderboard score

                if leaderboardDb is None or leaderboardDb[str(message.author.id)] is None:
                    leaderboardData = { 
                                        str(message.author.id): { 
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
                                    }
                    leaderboardCol.update_one({ "_id": message.guild.id }, { "$set": leaderboardData }, upsert=True)
                else:
                    authorID = str(message.author.id)
                    monthData = {
                                    str(datetime.datetime.now().month): {
                                        "points": leaderboardDb[str(message.author.id)][str(datetime.datetime.now().year)][str(datetime.datetime.now().month)]["points"] + points,
                                        "messages": leaderboardDb[str(message.author.id)][str(datetime.datetime.now().year)][str(datetime.datetime.now().month)]["messages"] + 1,
                                        "total_messages": leaderboardDb[str(message.author.id)][str(datetime.datetime.now().year)][str(datetime.datetime.now().month)]["total_messages"] + 1
                                    }
                                }
                    leaderboardCol.update_one(  
                                                { "_id": message.guild.id }, 
                                                { "$set": {
                                                    authorID.dateYear: monthData,
                                                    authorID.dateTime: datetime.datetime.now(),
                                                    authorID.points: leaderboardDb[str(message.author.id)]["points"] + points,
                                                    authorID.messages: leaderboardDb[str(message.author.id)]["messages"] + 1,
                                                    authorID.total_messages: leaderboardDb[str(message.author.id)]["total_messages"] + 1
                                                }}
                                                , upsert=True)
            else:
                total_messages = "total_messages"
                leaderboardCol.update_one({ "_id": message.guild.id }, 
                                          { "$set": {
                                            str(message.author.id).dateYearX.dateMonth.total_messages: leaderboardDb[str(message.author.id)][str(datetime.datetime.now().year)][str(datetime.datetime.now().month)]["total_messages"] + 1, 
                                            str(message.author.id).total_messages: leaderboardDb[str(message.author.id)]["total_messages"] + 1 
                                          }})
        except Exception as error:
            print(error)