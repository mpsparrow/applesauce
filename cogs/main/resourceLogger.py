'''
Name: Resource Logger
Description: Logs resource usage of server. Made to work with srLogger
Last Updated: February 7, 2020
Created: January 29, 2020
'''
import discord
from discord.ext import commands
import mysql.connector as mysql
from mysql.connector import errorcode
from utils import embed, config
import matplotlib.pyplot as plt
import numpy as np
import datetime
from datetime import date as dated
from datetime import timedelta

class resourceLogger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # resourceUsage (command)
    @commands.command(name="resourceUsage", description="Outputs resource usage of server for past 3 days.", usage="resources", aliases=['usage', 'ru', 'resources'])
    @commands.is_owner()
    async def resourceUsage(self, ctx):
        try:
            conf = config.configLoad('cogconfig.json')
            start_date = dated.today() - timedelta(days=3)
            end_date = dated.today() 

            # connects and gets database data
            cnx = mysql.connect(user=conf['srLogger']['user'], password=conf['srLogger']['password'], host=conf['srLogger']['host'], database=conf['srLogger']['database'])
            cursor = cnx.cursor()
            cursor.execute("SELECT cpu_percent_avg, vmemory_percent_avg, time, date FROM `usage` WHERE date BETWEEN %s AND %s", (start_date, end_date))
            data = np.array(cursor.fetchall())

            # parses database data into lists
            cpuPercent = np.array([item[0] for item in data])
            vmemoryPercent = np.array([item[1] for item in data])
            datetimeValue = []
            for item in data:
                datetimeValue.append(datetime.datetime.combine(item[3], (datetime.datetime.min + item[2]).time()))

            # plots data
            plt.plot(datetimeValue, cpuPercent, label="CPU Avg.")
            plt.plot(datetimeValue, vmemoryPercent, label="Virtual Mem Avg.")
            plt.ylabel("Usage 0-100%")
            plt.xlabel("Date/Time (MM-DD HH)")
            plt.yscale("log")
            plt.ylim(1e-1, 1e2)
            plt.legend(loc='best')
            plt.xticks(rotation=45)
            plt.grid()
            plt.tight_layout()
            plt.margins(0,0)
            plt.savefig("plot.png")
            plt.clf()
            cnx.close()
        except mysql.Error as err:
            print(err)
        data = embed.make_embed_image("Server Resource Usage", "plot.png")
        await ctx.send(embed=data[0], file=data[1])

def setup(bot):
    bot.add_cog(resourceLogger(bot))