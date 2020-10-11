import discord
from discord.ext import commands
from utils.checks import is_guild_enabled
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
                print("bot")
                return

            leaderboardCol = connect()[readINI("config.ini")["MongoDB"]["database"]]["leaderboard"] # connect to DB
            leaderboardDb = leaderboardCol.find_one({ "_id": message.guild.id })

            print("1")
            print(message.author.id)
            print(leaderboardCol)
            print(leaderboardDb)
            # Get current date/time
            if leaderboardDb is None or leaderboardDb[str(message.author.id)] is None:
                currentDateTime = datetime.datetime.now() - datetime.timedelta(seconds=60)
            else:
                currentDateTime = datetime.datetime.now()

            lastDateTime = currentDateTime + datetime.timedelta(seconds=60)

            print("2")

            if currentDateTime < lastDateTime:
                points = random.randint(15, 25)
                # Update leaderboard score
                leaderboardData = { 
                                    str(message.author.id): { 
                                        "dateTime": currentDateTime,
                                        "points": points,
                                        "messages": 1,
                                        "total_messages": 1,
                                        str(currentDateTime.year): { 
                                            str(currentDateTime.month): {
                                                "points": points,
                                                "messages": 1,
                                                "total_messages": 1
                                            }
                                        }
                                    }
                                  }
                print(leaderboardData)

                leaderboardCol.update_one({ "_id": message.guild.id }, { "$set": leaderboardData }, upsert=True)
            else:
                leaderboardData = { 
                                    str(message.author.id): { 
                                        "total_messages": 1,
                                        str(currentDateTime.year): { 
                                            str(currentDateTime.month): {
                                                "points": points,
                                                "messages": 1,
                                                "total_messages": 1
                                            }
                                        }
                                    }
                                  }
                print(leaderboardData)

                leaderboardCol.update_one({ "_id": message.guild.id }, { "$set": leaderboardData }, upsert=True)
        except Exception as error:
            print(error)