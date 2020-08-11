import discord
from discord.ext import commands
from utils.database.actions import connect
from utils.logger import guildLog
from utils.config import readINI

emote_reactions = { 
    "failed": "❌",
    "success": "✅"
}

class Guilds(commands.Cog):
    """
    Guild management commands
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        guildLog.info(f"{guild.id}: Successfully joined!")

        # adds guild information into database
        try:
            guildCol = connect()[readINI("config.ini")["MongoDB"]["database"]]["guilds"]
            guildINFO = { "_id": guild.id,
                        "guild_name": guild.name,
                        "owner_id": guild.owner,
                        "region": guild.region,
                        "preferred_locale": guild.preferred_locale,
                        "icon_url": guild.icon_url,
                        "large": guild.large,
                        "member_count": guild.member_count,
                        "description": guild.description,
                        "created_at": guild.created_at,
                        "nitro_tier": guild.premium_tier,
                        "features": guild.features }
            guildCol.update_one({ "_id": guild.id }, { "$set": guildINFO }, upsert=True)
            guildLog.info(f"{guild.id}: Added information to database")
        except Exception as error:
            guildLog.info(f"{guild.id}: Failed to add information to database")

        # sends join message with getting started information
        try:
            guildData = guildCol.find_one({ "_id": guild.id })
            await ctx.send(f"**Thanks for adding me!**\n**Prefix:** `{guildData['prefix']}`\n**Help:** `{guildData['prefix']}help`")
        except Exception:
            await ctx.send(f"**Thanks for adding me!**\n**Prefix:** `{readINI("config.ini")['main']['defaultPrefix']}`\n**Help:** `{readINI("config.ini")['main']['defaultPrefix']}help`")
        else:
            await ctx.send(f"**Thanks for adding me!**")

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        try:
            guildCol = connect()[readINI("config.ini")["MongoDB"]["database"]]["guilds"]
            guildCol.delete_one({ "_id": guild.id })
            guildLog.info(f"{guild.id}: Removed information from database on_guild_remove")
        except Exception as error:
            guildLog.info(f"{guild.id}: Failed to remove information from database on_guild_remove")

    @commands.Cog.listener()
    async def on_guild_update(self, before, after):
        try:
            guildCol = connect()[readINI("config.ini")["MongoDB"]["database"]]["guilds"]
            guildINFO = { "_id": after.id,
                        "guild_name": after.name,
                        "owner_id": after.owner,
                        "region": after.region,
                        "preferred_locale": after.preferred_locale,
                        "icon_url": after.icon_url,
                        "large": after.large,
                        "member_count": after.member_count,
                        "description": after.description,
                        "created_at": after.created_at,
                        "nitro_tier": after.premium_tier,
                        "features": after.features }
            guildCol.update_one({ "_id": after.id }, { "$set": guildINFO }, upsert=True)
        except Exception as error:
            guildLog.error(f"{after.id}: Failed to update guild information")

    @commands.group(name="guild", description="Guild management", usage="<action>", aliases=["g"], invoked_subcommand=True)
    @commands.has_permissions(manage_guild=True)
    async def guild(self, ctx):
        """
        Command group for guild management
        :param ctx:
        """

    @guild.command(name="prefix", description="Change guild prefix", usage="<prefix>", aliases=["p"])
    @commands.has_permissions(manage_guild=True)
    async def prefix(self, ctx, prefix, *):
        """
        Change guild prefix
        :param ctx:
        :param prefix: prefix text
        """
        try:
            guildCol = connect()[readINI("config.ini")["MongoDB"]["database"]]["guilds"]
            guildINFO = { "_id": ctx.guild.id,
                          "prefix": str(prefix) }
            guildCol.update_one({ "_id": ctx.guild.id }, { "$set": guildINFO }, upsert=True)
            await ctx.message.add_reaction(emote_reactions["success"])
        except Exception as error:
            await ctx.message.add_reaction(emote_reactions["failed"])

    @guild.command(name="ignore", description="Make bot ignore a user", usage="<user>", aliases=["i"])
    @commands.has_permissions(manage_guild=True)
    async def ignore(self, ctx, *, user: discord.Member):
        """
        Make bot ignore a user
        :param ctx:
        :param user: discord.Member
        """
        try:
            guildCol = connect()[readINI("config.ini")["MongoDB"]["database"]]["guilds"]
            guildCol.update_one({ "_id": ctx.guild.id }, { "$set": { f"ignore.{str(user.id)}": True }}, upsert=True)
            await ctx.message.add_reaction(emote_reactions["success"])
        except Exception as error:
            await ctx.message.add_reaction(emote_reactions["failed"])

    @guild.command(name="unignore", description="Make bot unignore a user", usage="<user>", aliases=["uni", "ui"])
    @commands.has_permissions(manage_guild=True)
    async def unignore(self, ctx, *, user: discord.Member):
        """
        Make bot unignore a user
        :param ctx:
        :param user: discord.Member
        """
        try:
            guildCol = connect()[readINI("config.ini")["MongoDB"]["database"]]["guilds"]
            guildCol.update_one({ "_id": ctx.guild.id }, { "$set": { f"ignore.{str(user.id)}": False }}, upsert=True)
            await ctx.message.add_reaction(emote_reactions["success"])
        except Exception as error:
            await ctx.message.add_reaction(emote_reactions["failed"])