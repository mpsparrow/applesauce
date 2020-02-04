'''
Name: Pin Archive
Description: Pin archiving system
Last Updated: January 20, 2020
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
                try:
                    conf = config.configLoad("guildconfig.json")
                    channelID = conf[str(data["guild_id"])]["archive"]
                    channel = self.bot.get_channel(channelID)
                    current_date = datetime.datetime.utcfromtimestamp(int(time.time()))

                    # if message was an embed
                    try:
                        embed2 = data['embeds'][0]
                        embed3 = discord.Embed(description=f"{embed2['description']}", color=0xc1c100, timestamp=current_date)
                        try:
                            attachmentURL = embed2["image"]["proxy_url"]
                            embed3.set_image(url=attachmentURL)
                        except:
                            pass
                        embed3.set_author(name=data["author"]["username"], icon_url=f'https://cdn.discordapp.com/avatars/{data["author"]["id"]}/{data["author"]["avatar"]}.png', url=f'https://discordapp.com/channels/{data["guild_id"]}/{data["channel_id"]}/{data["id"]}')
                        embed3.set_footer(text=f'Embedded message sent in #{self.bot.get_channel(int(data["channel_id"]))}')
                        await channel.send(embed=embed3)
                        return
                    except:
                        pass

                    # if message isn't an embed
                    embed = discord.Embed(description=f"{data['content']}", color=0xc1c100, timestamp=current_date)
                    try:
                        attachmentURL = data["attachments"][0]["proxy_url"]
                        embed.set_image(url=attachmentURL)
                    except:
                        pass

                    embed.set_author(name=data["author"]["username"], icon_url=f'https://cdn.discordapp.com/avatars/{data["author"]["id"]}/{data["author"]["avatar"]}.png', url=f'https://discordapp.com/channels/{data["guild_id"]}/{data["channel_id"]}/{data["id"]}')
                    embed.set_footer(text=f'Sent in #{self.bot.get_channel(int(data["channel_id"]))}')
                    await channel.send(embed=embed)
                    return
                except:
                    pass
        except:
            pass

    # setArchive (command)
    @commands.command(name="setArchive", description="Sets channel for pins archiving.", usage="setArchive <channel-ID>", aliases=['setChannelArchive'])
    @commands.has_permissions(manage_guild=True)
    async def setArchive(self, ctx, channel):
        try:
            conf = config.configLoad("guildconfig.json")
            conf[str(ctx.guild.id)]["archive"] = int(channel)
            config.configDump("guildconfig.json", conf)
            await ctx.send("channel id set")
        except:
            await ctx.send("invalid or enable to set")

    # messageArchive (command)
    @commands.check(commandchecks.isAllowed)
    @commands.command(name="messageArchive", description="Archives message", usage="a <message-ID>", aliases=['a'])
    @commands.has_permissions(manage_guild=True)
    @commands.cooldown(1, 10, commands.BucketType.default)
    async def messageArchive(self, ctx, messageID):
        try:
            data = await ctx.fetch_message(messageID)

            try:
                conf = config.configLoad("guildconfig.json")
                channelID = conf[str(data.guild.id)]["archive"]
                channel = self.bot.get_channel(channelID)
                current_date = datetime.datetime.utcfromtimestamp(int(time.time()))

                # if message was an embed
                try:
                    embed2 = data.embeds[0]
                    embed2.timestamp = current_date
                    embed2.set_footer(text=f'Embedded message sent in #{self.bot.get_channel(int(data.channel.id))}')
                    await channel.send(embed=embed2)
                    return
                except:
                    pass

                # if message isn't an embed
                embed = discord.Embed(description=f"{data.content}", color=0xc1c100, timestamp=current_date)
                try:
                    attachmentURL = data.attachments[0].url
                    embed.set_image(url=attachmentURL)
                except:
                    pass

                embed.set_footer(text=f'Sent in #{self.bot.get_channel(int(data.channel.id))}')
                embed.set_author(name=data.author.name, icon_url=f'https://cdn.discordapp.com/avatars/{data.author.id}/{data.author.avatar}.png', url=f'https://discordapp.com/channels/{data.guild.id}/{data.channel.id}/{data.id}')
                await channel.send(embed=embed)
                return
            except:
                pass
        except:
            pass

def setup(bot):
    bot.add_cog(pinArchive(bot))