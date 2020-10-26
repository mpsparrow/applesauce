from discord.ext import commands
from discord.ext.commands import has_permissions
from utils.checks import is_guild_enabled
from utils.database.actions import connect
from utils.config import readINI

# The check to ensure this is the guild used where the command was made
def guild_check(commandsCol):
    async def predicate(ctx):
        return commandsCol.find({ f"{ctx.guild.id}.{ctx.command.qualified_name}": { "$exists": True } })
    return commands.check(predicate)

class CustomCMD(commands.Cog):
    @commands.command()
    @is_guild_enabled()
    @commands.has_permissions(manage_guild=True)
    async def add_command(self, ctx, name, *, output):
        try:
            commandsCol = connect()[readINI("config.ini")["MongoDB"]["database"]]["customCommands"] # connect to DB
            
            # First check if there's a custom command with that name already
            existing_command = commandsCol.find({ f"{ctx.guild.id}.{name}": { "$exists": True } })
            # Check if there's a built in command, we don't want to override that
            if existing_command is False and ctx.bot.get_command(name):
                return await ctx.send(f"A built in command with the name {name} is already registered")

            # Now, if the command already exists then we just need to add/override the message for this guild
            if existing_command:
                commandsCol.update_one({ "_id": ctx.guild.id }, { "$set": { f"{name}": output }}, upsert=True)

            # Otherwise, we need to create the command object
            else:
                @commands.command(name=name, help=f"Custom command: Outputs your custom provided output")
                @guild_check(commandsCol)
                async def cmd(self, ctx):
                    await ctx.send(commandsCol.find_one({ "_id": ctx.guild.id }[ctx.invoked_with]))
                cmd.cog = self
                # And add it to the cog and the bot
                self.__cog_commands__ = self.__cog_commands__ + (cmd,)
                ctx.bot.add_command(cmd)
                # Now add it to our list of custom commands
                commandsCol.update_one({ "_id": ctx.guild.id }, { "$set": { f"{name}": output }}, upsert=True)
            await ctx.send(f"Added a command called {name}")
        except Exception as err:
            print(err)

    @commands.command()
    @is_guild_enabled()
    @commands.has_permissions(manage_guild=True)
    async def remove_command(self, ctx, name):
        # Make sure it's actually a custom command, to avoid removing a real command
        commandsCol = connect()[readINI("config.ini")["MongoDB"]["database"]]["customCommands"] # connect to DB
        if not(commandsCol.find({ f"{ctx.guild.id}.{name}": { "$exists": True } })):
            return await ctx.send(f"There is no custom command called {name}")
        # All that technically has to be removed, is our guild from the dict for the command
        commandsCol[ctx.guild.id].remove( { "$pull": name } )
        await ctx.send(f"Removed a command called {name}")