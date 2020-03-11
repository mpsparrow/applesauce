'''
Name: Archiving
Description: Archiving message system
'''

import discord
from discord.ext import commands
import datetime
import time
from discord.ext.commands import has_permissions
from util import commandchecks, embed, dbQuery, dbInsert


class pinArchive(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # pin archiving
    @commands.Cog.listener()
    async def on_raw_message_edit(self, payload):
        data = payload.data
        try:
            conf = dbQuery.archive(data["guild_id"])
            if (data['pinned'] == True) and (conf[3]) and (conf[4]): 
                try:
                    channelID = conf[1]
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

                    try:
                        roleID = conf[2]
                        role = self.bot.get_guild(int(data["guild_id"])).get_role(roleID)
                        member = self.bot.get_guild(int(data["guild_id"])).get_member(int(data["author"]["id"]))
                        if member != self.bot.user:
                            await member.add_roles(role, atomic=True)
                    except:
                        pass

                    embed.set_author(name=data["author"]["username"], icon_url=f'https://cdn.discordapp.com/avatars/{data["author"]["id"]}/{data["author"]["avatar"]}.png', url=f'https://discordapp.com/channels/{data["guild_id"]}/{data["channel_id"]}/{data["id"]}')
                    embed.set_footer(text=f'Pinned in #{self.bot.get_channel(int(data["channel_id"]))}')
                    await channel.send(embed=embed)
                    return
                except:
                    pass
        except:
            pass

    # archiveSetup (command)
    @commands.group(name="archiveSetup", description="Help menu and commands for configuring archiving.", usage="archiveSetup", aliases=['as'], invoke_without_command=True)
    @commands.has_permissions(manage_guild=True)
    async def archiveSetup(self, ctx):
        prefix = dbQuery.prefix(ctx.guild.id)
        embed2 = embed.make_embed_fields_ninl("Archiving Setup", "commands for configuring archiving", 
            (f"{prefix}a <message-ID>", "Archives given message in archiving channel."),
            (f"{prefix}as t <true/false>", "Override toggle on/off for archiving. `true` is enabled."),
            (f"{prefix}as p <true/false>", "`true` will enable archiving of pinned messages."),
            (f"{prefix}as c <channel-ID>", "Sets channel for archiving."), 
            (f"{prefix}as r <role-ID>", f"Role given to anyone who gets their message archived (either through pins or `{prefix}a`). Use `0` to disable."))
        await ctx.send(embed=embed2)

    # archiveToggle (subcommand)
    @archiveSetup.command(aliases=['t'])
    @commands.has_permissions(manage_guild=True)
    async def archiveToggle(self, ctx, value: bool):
        try:
            dbInsert.archiveToggle(ctx.guild.id, value)
            await ctx.send(embed=embed.make_embed("Archiving", f"Archiving set to {value}"))
        except:
            await ctx.send(embed=embed.make_error_embed("Error toggling. Please try again."))

    # archivePins (subcommand)
    @archiveSetup.command(aliases=['p'])
    @commands.has_permissions(manage_guild=True)
    async def archivePins(self, ctx, value: bool):
        try:
            dbInsert.archivePins(ctx.guild.id, value)
            await ctx.send(embed=embed.make_embed("Archiving", f"Archiving pins set to {value}"))
        except:
            await ctx.send(embed=embed.make_error_embed("Error. Please try again."))

    # archiveChannel (subcommand)
    @archiveSetup.command(aliases=['c'])
    @commands.has_permissions(manage_guild=True)
    async def archiveChannel(self, ctx, channel):
        try:
            dbInsert.archiveChannel(ctx.guild.id, channel)
            await ctx.send(embed=embed.make_embed("Archiving", f"Channel: <#{int(channel)}>"))
        except:
            await ctx.send(embed=embed.make_error_embed("Invalid channel ID"))

    # archiveRole (subcommand)
    @archiveSetup.command(aliases=['r'])
    @commands.has_permissions(manage_guild=True)
    async def archiveRole(self, ctx, role):
        try:
            dbInsert.archiveRole(ctx.guild.id, role)
            await ctx.send(embed=embed.make_embed("Archiving", f"Role: <@&{int(role)}>"))
        except:
            await ctx.send(embed=embed.make_error_embed("Invalid role ID"))

    # archive (command)
    @commands.check(commandchecks.isAllowed)
    @commands.command(name="archive", description="Archives given message in defined archiving channel.", usage="a <message-ID>", aliases=['a'])
    @commands.has_permissions(manage_messages=True)
    @commands.cooldown(1, 10, commands.BucketType.default)
    async def archive(self, ctx, messageID):
        conf = dbQuery.archive(ctx.guild.id)
        if conf[4] == True:
            try:
                data = await ctx.fetch_message(messageID)
                current_date = datetime.datetime.utcfromtimestamp(int(time.time()))
                try:
                    channelID = conf[1]
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
                    roleID = conf[2]
                    role = ctx.guild.get_role(roleID)
                    member = ctx.guild.get_member(data.author.id)
                    if member != self.bot.user:
                        await member.add_roles(role, atomic=True)
                except:
                    pass

                embed.set_footer(text=f'Sent in #{self.bot.get_channel(int(data.channel.id))}')
                embed.set_author(name=data.author.name, icon_url=f'https://cdn.discordapp.com/avatars/{data.author.id}/{data.author.avatar}.png', url=f'https://discordapp.com/channels/{data.guild.id}/{data.channel.id}/{data.id}')
                await channel.send(embed=embed)
                await ctx.message.add_reaction("📌")
            except:
                await ctx.send(embed=embed.make_error_embed("Error occured while trying to archive. Please try again."))

def setup(bot):
    bot.add_cog(pinArchive(bot))