'''
Name: Resource Logger
Description: Logs resource usage of server. Made to work with srLogger
Last Updated: January 31, 2020
Created: January 29, 2020
'''
import discord
from discord.ext import commands
import mysql.connector as mysql
from mysql.connector import errorcode
import matplotlib.pyplot as plt
from utils import embed, config
import datetime
from datetime import date as dated
from datetime import timedelta

class resourceLogger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="resourceUsage", description="Outputs resource usage of server for past 3 days.", usage="resources", aliases=['usage', 'ru', 'resources'])
    @commands.is_owner()
    async def resourceUsage(self, ctx):
        try:
            conf = config.configLoad('cogconfig.json')
            start_date = dated.today() - timedelta(days=3)
            end_date = dated.today() 
            cnx = mysql.connect(user=conf['srLogger']['user'], password=conf['srLogger']['password'], host=conf['srLogger']['host'], database=conf['srLogger']['database'])
            cursor = cnx.cursor()
            cursor.execute("SELECT cpu_percent_avg, vmemory_percent_avg, smemory_percent_avg, time, date FROM `usage` WHERE date BETWEEN %s AND %s", (start_date, end_date))
            cpuPercent = []
            timeValue = []
            dateValue = []
            vmemoryPercent = []
            smemoryPercent = []
            newLegend = []
            for (cpu_percent_avg, vmemory_percent_avg, smemory_percent_avg, time, date) in cursor:
                cpuPercent.append(cpu_percent_avg)
                timeValue.append(str(time))
                dateValue.append(str(date))
                vmemoryPercent.append(vmemory_percent_avg)
                smemoryPercent.append(smemory_percent_avg)
            '''
            plt.plot(timeValue, cpuPercent, label="CPU Avg.")
            plt.plot(timeValue, cpuMin, label="CPU Min")
            plt.plot(timeValue, cpuMax, label="CPU Max")
            '''
            plt.stackplot(timeValue, cpuPercent, vmemoryPercent, smemoryPercent, labels=["CPU", "Virtual Memory", "Swap Memory"])
            plt.ylabel("Usage 0-100%")
            plt.ylim(0, 100)
            for i in range(len(dateValue)):
                if i % 15 == 0:
                    newLegend.append(dateValue[i] + "\n" + timeValue[i][:-3])
                else:
                    newLegend.append(" ")
            plt.xticks(timeValue, newLegend, fontsize=8, rotation=80)
            plt.legend(loc='best')
            plt.tight_layout()
            plt.savefig("plot.png")
            plt.clf()
            cnx.close()
        except mysql.Error as err:
            print(err)
        data = embed.make_embed_image("Server Resource Usage", "plot.png")
        await ctx.send(embed=data[0], file=data[1])

def setup(bot):
    bot.add_cog(resourceLogger(bot))