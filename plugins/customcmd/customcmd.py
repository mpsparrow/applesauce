from discord.ext import commands
from discord.ext.commands import has_permissions
from utils.checks import is_guild_enabled
from utils.database.actions import connect
from utils.config import readINI
from utils.logger import startLog, pluginLog

class CustomCMD(commands.Cog):
    """
    Custom Commands
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        startLog.info("Loading Custom Commands")

        commandsCol = connect()[readINI("config.ini")["MongoDB"]["database"]]["customCommands"] # connect to DB
        commandSet = set()
        loadedCounter = 0

        for document in commandsCol.find():
            for item in document:
                if not(item == "_id"):
                    commandSet.add(item)

        for com in commandSet:
            try:
                @commands.command(name=com, help=f"Custom command", description=f"Custom command")
                async def cmd(self, ctx):
                    comText = commandsCol.find_one({ "_id": ctx.guild.id })[str(com)]
                    comText = comText.replace("$(user)", f"{ctx.author.name}")
                    await ctx.send(comText)

                cmd.cog = self
                self.__cog_commands__ = self.__cog_commands__ + (cmd,)
                self.bot.add_command(cmd)
                loadedCounter += 1
            except Exception as err:
                pluginLog.error(f"Error loading custom command {com} ERROR: {err}")
        
        startLog.info(f"{loadedCounter}/{len(commandSet)} custom commands loaded")

    @commands.command()
    @is_guild_enabled()
    @commands.has_permissions(manage_guild=True)
    async def addcommand(self, ctx, name, *, output):
        commandsCol = connect()[readINI("config.ini")["MongoDB"]["database"]]["customCommands"] # connect to DB
        commandsObj = commandsCol.find_one({ "_id": ctx.guild.id })

        # Check if there's a built in command, we don't want to override that
        if (commandsObj is None or str(name) in commandsObj) and ctx.bot.get_command(name)  :
            return await ctx.send(f"A built in command with the name {name} is already registered")

        # Now, if the command already exists then we just need to add/override the message for this guild
        if commandsObj is not None and str(name) not in commandsObj:
            commandsCol.update_one({ "_id": ctx.guild.id }, { "$set": { f"{name}": output }}, upsert=True)

        # Otherwise, we need to create the command object
        else:
            @commands.command(name=name, help=f"Custom command", description=f"Custom command")
            async def cmd(self, ctx):
                comText = commandsCol.find_one({ "_id": ctx.guild.id })[str(name)]
                comText = comText.replace("$(user)", f"{ctx.author.name}")
                await ctx.send(comText)

            cmd.cog = self

            self.__cog_commands__ = self.__cog_commands__ + (cmd,)
            ctx.bot.add_command(cmd)

            commandsCol.update_one({ "_id": ctx.guild.id }, { "$set": { f"{name}": output }}, upsert=True)
        await ctx.send(f"Added a command called {name}")

    @commands.command()
    @is_guild_enabled()
    @commands.has_permissions(manage_guild=True)
    async def removecommand(self, ctx, name):
        commandsCol = connect()[readINI("config.ini")["MongoDB"]["database"]]["customCommands"] # connect to DB
        commandsObj = commandsCol.find_one({ "_id": ctx.guild.id })

        if str(name) not in commandsObj:
            return await ctx.send(f"There is no custom command called {name}")

        commandsCol.update({ "_id": ctx.guild.id }, { "$unset": { name: "" } })
        await ctx.send(f"Removed a command called {name}")