'''
Name: Archiving
Description: Archiving message system
Last Updated: February 6, 2020
Created: December 14, 2019
'''
import discord
from discord.ext import commands
import datetime
import time
from discord.ext.commands import has_permissions
from utils import config, commandchecks, embed, logger

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
                    channelID = conf[str(data["guild_id"])]["archiveChannel"]
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
    @commands.command(name="archiveChannel", description="Sets channel for pins archiving. Use `none` to disable.", usage="archiveChannel <channel-ID>")
    @commands.has_permissions(manage_guild=True)
    async def archiveChannel(self, ctx, channel):
        try:
            conf = config.configLoad("guildconfig.json")

            try:
                if str(channel) == "none":
                    del conf[str(ctx.guild.id)]["archiveChannel"]
                    config.configDump("guildconfig.json", conf)
                    await ctx.send(embed=embed.make_embed("Archiving", f"Channel removed."))
                    return
            except:
                pass

            conf[str(ctx.guild.id)]["archiveChannel"] = int(channel)
            config.configDump("guildconfig.json", conf)
            await ctx.send(embed=embed.make_embed("Archiving", f"Channel: <#{int(channel)}>"))
        except:
            await ctx.send(embed=embed.make_error_embed("Invalid channel ID"))

    @commands.command(name="archiveRole", description="Role given to anyone who gets their message archived. Use `none` to disable.", usage="archiveRole <role-ID>")
    @commands.has_permissions(manage_guild=True)
    async def archiveRole(self, ctx, role):
        try:
            conf = config.configLoad("guildconfig.json")

            try:
                if str(role) == "none":
                    del conf[str(ctx.guild.id)]["archiveRole"]
                    config.configDump("guildconfig.json", conf)
                    await ctx.send(embed=embed.make_embed("Archiving", f"Role removed."))
                    return
            except:
                pass

            conf[str(ctx.guild.id)]["archiveRole"] = int(role)
            config.configDump("guildconfig.json", conf)
            await ctx.send(embed=embed.make_embed("Archiving", f"Role: <@&{int(role)}>"))
        except:
            await ctx.send(embed=embed.make_error_embed("Invalid role ID"))

    # messageArchive (command)
    @commands.check(commandchecks.isAllowed)
    @commands.command(name="archive", description="Archives message in archiving channel", usage="a <message-ID>", aliases=['a'])
    @commands.has_permissions(manage_messages=True)
    @commands.cooldown(1, 10, commands.BucketType.default)
    async def archive(self, ctx, messageID):
        try:
            data = await ctx.fetch_message(messageID)
            conf = config.configLoad("guildconfig.json")
            current_date = datetime.datetime.utcfromtimestamp(int(time.time()))
            try:
                channelID = conf[str(data.guild.id)]["archiveChannel"]
                channel = self.bot.get_channel(channelID)
            except:
                await ctx.send(embed=embed.make_error_embed("No archiving channel set. Set one using `archiveChannel`"))

            # if message was an embed
            try:
                embed2 = data.embeds[0]
                embed2.timestamp = current_date
                embed2.set_footer(text=f'Embedded message sent in <#{self.bot.get_channel(int(data.channel.id))}>')
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

            try:
                roleID = conf[str(data.guild.id)]["archiveRole"]
                role = ctx.guild.get_role(roleID)
                member = ctx.guild.get_member(data.author.id)
                logger.infoLog(member)
                if member != self.bot.user:
                    await member.add_roles(role, atomic=True)
            except Exception as e:
                logger.errorLog(f'{e}')

            embed.set_footer(text=f'Sent in #{self.bot.get_channel(int(data.channel.id))}')
            embed.set_author(name=data.author.name, icon_url=f'https://cdn.discordapp.com/avatars/{data.author.id}/{data.author.avatar}.png', url=f'https://discordapp.com/channels/{data.guild.id}/{data.channel.id}/{data.id}')
            await channel.send(embed=embed)
        except:
            await ctx.send(embed=embed.make_error_embed("Error occured while trying to archive. Please try again."))

def setup(bot):
    bot.add_cog(pinArchive(bot))