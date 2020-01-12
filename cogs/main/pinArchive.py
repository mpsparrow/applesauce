'''
Name: Pin Archive
Description: Pin archiving system
Last Updated: January 11, 2020
Created: December 14, 2019
'''
import discord
from discord.ext import commands
import datetime
import time
from discord.ext.commands import has_permissions
from utils import config, commandchecks

class pinArchive(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # pin archiving
    @commands.Cog.listener()
    async def on_raw_message_edit(self, payload):
        data = payload.data
        try:
            if data['pinned'] == True: 
                conf = config.configLoad("guildconfig.json")
                channelID = conf[str(data["guild_id"])]["archive"]
                channel = self.bot.get_channel(channelID)                
                current_date = datetime.datetime.utcfromtimestamp(int(time.time()))
                embed = discord.Embed(description=f"{data['content']}", color=0xc1c100, timestamp=current_date)
                try:
                    attach = data["attachments"]
                    img_url = attach[0]['proxy_url']
                    embed.set_image(url=img_url)
                except:
                    pass
                embed.set_author(name=data["author"]["username"], icon_url=f'https://cdn.discordapp.com/avatars/{data["author"]["id"]}/{data["author"]["avatar"]}.png', url=f'https://discordapp.com/channels/{data["guild_id"]}/{data["channel_id"]}/{data["id"]}')
                embed.set_footer(text=f'Sent in #{self.bot.get_channel(int(data["channel_id"]))}')
                await channel.send(embed=embed)
        except:
            pass

    # clear/purge command
    @commands.command(name="setArchive", description="Sets channel for pins archiving.", usage="setArchive <channel-ID>", aliases=['setChannelArchive'])
    @commands.has_permissions(manage_messages=True)
    async def setArchive(self, ctx, channel):
        try:
            conf = config.configLoad("guildconfig.json")
            conf[str(ctx.guild.id)]["archive"] = int(channel)
            config.configDump("guildconfig.json", conf)
            await ctx.send("channel id set")
        except:
            await ctx.send("invalid or enable to set")

def setup(bot):
    bot.add_cog(pinArchive(bot))