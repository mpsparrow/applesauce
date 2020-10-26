from discord.ext import commands
from discord.ext.commands import has_permissions
from utils.checks import is_guild_enabled
from utils.database.actions import connect
from utils.config import readINI
from utils.logger import startLog

class CustomCMD(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
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
                    comText = commandsCol.find_one({ "_id": ctx.guild.id })[str(name)]
                    comText = comText.replace("$(user)", f"{ctx.author}").replace("$(arg)", f"{arg}")
                    await ctx.send(comText)

                cmd.cog = self
                self.__cog_commands__ = self.__cog_commands__ + (cmd,)
                self.bot.add_command(cmd)
                loadedCounter += 1
            except Exception as err:
                startLog.debug(f"Error loading custom command {com} ERROR: {err}")
        
        startLog.info(f"{loadedCounter}/{len(commandSet)} custom commands loaded")

    @commands.command()
    @is_guild_enabled()
    @commands.has_permissions(manage_guild=True)
    async def add_command(self, ctx, name, *, output):
        commandsCol = connect()[readINI("config.ini")["MongoDB"]["database"]]["customCommands"] # connect to DB
        
        # First check if there's a custom command with that name already
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
            async def cmd(self, ctx, *, arg):
                comText = commandsCol.find_one({ "_id": ctx.guild.id })[str(name)]
                comText = comText.replace("$(user)", f"{ctx.author}").replace("$(arg)", f"{arg}")
                await ctx.send(comText)

            cmd.cog = self
            # And add it to the cog and the bot
            self.__cog_commands__ = self.__cog_commands__ + (cmd,)
            ctx.bot.add_command(cmd)
            # Now add it to our list of custom commands
            commandsCol.update_one({ "_id": ctx.guild.id }, { "$set": { f"{name}": output }}, upsert=True)
        await ctx.send(f"Added a command called {name}")

    @commands.command()
    @is_guild_enabled()
    @commands.has_permissions(manage_guild=True)
    async def remove_command(self, ctx, name):
        # Make sure it's actually a custom command, to avoid removing a real command
        commandsCol = connect()[readINI("config.ini")["MongoDB"]["database"]]["customCommands"] # connect to DB
        commandsObj = commandsCol.find_one({ "_id": ctx.guild.id })
        if str(name) not in commandsObj:
            return await ctx.send(f"There is no custom command called {name}")
        # All that technically has to be removed, is our guild from the dict for the command
        commandsCol.update({ "_id": ctx.guild.id }, { "$unset": { name: "" } })
        await ctx.send(f"Removed a command called {name}")