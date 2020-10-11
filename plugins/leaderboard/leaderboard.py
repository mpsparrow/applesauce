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
                return

            leaderboardCol = connect()[readINI("config.ini")["MongoDB"]["database"]]["leaderboard"] # connect to DB
            leaderboardDb = leaderboardCol.find_one({ "_id": message.guild.id })

            # Get current date/time
            if leaderboardDb[message.author.id] is None:
                currentDateTime = datetime.datetime(2000, 4, 20, 0, 0)
            else:
                currentDateTime = datetime.datetime.now()

            lastDateTime = currentDateTime + datetime.timedelta(seconds=60)

            if currentDateTime < lastDateTime:
                points = random.randint(15, 25)
                # Update leaderboard score
                leaderboardData = { 
                                    message.author.id: { 
                                        "dateTime": currentDateTime,
                                        "points": points,
                                        "messages": 1,
                                        "total_messages": 1,
                                        currentDateTime.year: { 
                                            currentDateTime.month: {
                                                "points": points,
                                                "messages": 1,
                                                "total_messages": 1
                                            }
                                        }
                                    }
                                  }

                leaderboardCol.update_one({ "_id": message.guild.id }, { "$set": leaderboardData }, upsert=True)
            else:
                leaderboardData = { 
                                    message.author.id: { 
                                        "total_messages": 1,
                                        currentDateTime.year: { 
                                            currentDateTime.month: {
                                                "points": points,
                                                "messages": 1,
                                                "total_messages": 1
                                            }
                                        }
                                    }
                                  }

                leaderboardCol.update_one({ "_id": message.guild.id }, { "$set": leaderboardData }, upsert=True)
        except Exception as error:
            print(error)