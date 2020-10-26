import discord
from discord.ext import commands
from utils.checks import is_guild_enabled
import json
import inspect
import functools
import re

class CustomCommandEntry:
    __slots__ = ['name', 'content', 'guild_id']

    def __init__(self, **kwargs):
        self.name = kwargs.pop('name', None)
        self.content = kwargs.pop('content', None)
        self.guild_id = kwargs.pop('guild_id', None)

    def __repr__(self):
        return '<CustomCommandEntry name={0.name} content={0.content} guild_id={0.guild_id}>'.format(self)

class CustomCommandEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, CustomCommandEntry):
            payload = { '__command__': True }
            for val in obj.__slots__:
                payload[val] = getattr(obj, val)
            return payload
        return super().default(obj)

def custom_command_decoder(obj):
    if '__command__' in obj:
        return CustomCommandEntry(**obj)
    return obj

# the actual 'functional' parts

# this is the actual 'callback' that executes the custom command registered
# for 'sanity' sakes, custom commands cannot have arguments. Maybe I will
# modify it so they can in the future, but for now they don't.

async def custom_command_callback(entry, ctx, *args : str):
    # in the entry content you can have ${user} and ${mention}
    author = ctx.message.author
    fixed = entry.content.replace('${user}', author.name).replace('${mention}', author.mention)

    # find all ${N} and replace it with args[N]
    def getter(obj):
        try:
            return args[int(obj.group(1))]
        except Exception:
            return ''

    fixed = re.sub(r'\${(\d+)}', getter, fixed)
    await ctx.send(fixed)

class CustomCommand(commands.Command):
    def __init__(self, **kwargs):
        self._entries = {}
        super().__init__(**kwargs)

    async def invoke(self, ctx):
        server = ctx.message.server
        if server is not None:
            entry = self._entries.get(server.id)
            if entry is None:
                return

            # update the callback called
            self.callback = functools.partial(custom_command_callback, entry)
            self.params = inspect.signature(self.callback).parameters

        await super().invoke(ctx)

# that ends the 'functionality'

class CustomCMD(commands.Cog):
    """
    Custom commands
    """
    def __init__(self, bot):
        self.bot = bot

    async def register_custom_command(self, entry):
        """Registers a custom command to the bot."""
        command = self.bot.get_command(entry.name)
        if command is None:
            # the command is not registered so we can add it
            # for the first time using this entry as its first entry.
            command = self.bot.command(name=entry.name, cls=CustomCommand,
                                pass_context=True, hidden=True)(custom_command_callback)

        if not isinstance(command, CustomCommand):
            raise RuntimeError('This is an already registered non-custom command.')

        if entry.guild_id in command._entries:
            # you can do some permission checking here, but this is outside the example's scope.
            raise RuntimeError('This is already registered as a custom command.')

        command._entries[entry.guild_id] = entry

    async def load_custom_commands(self):
        try:
            with open('custom_commands.json') as f:
                entries = json.load(f, object_hook=custom_command_decoder)
                for entry in entries:
                    await self.register_custom_command(entry)
        except FileNotFoundError:
            pass

    async def save_custom_commands(self):
        entries = []
        for name, command in self.bot.commands.items():
            if isinstance(command, CustomCommand):
                entries.extend(command._entries.values())

        with open('custom_commands.json', 'w') as f:
            json.dump(entries, f, ensure_ascii=True, cls=CustomCommandEncoder)

    @commands.Cog.listener()
    async def on_ready(self):
        await self.load_custom_commands()
        print('loaded custom commands')

    @commands.command(name="create", description="Custom command")
    @is_guild_enabled()
    async def create(self, ctx, name, *, content):
        """Creates a custom command for your server.

        The following placeholders are available:

        - ${user} : replaces the user's name
        - ${mention} : replaced with a mention of the user

        Custom commands are forced to be lower case.
        """
        entry = CustomCommandEntry(name=name.lower(), content=content, guild_id=ctx.message.server.id)
        try:
            await self.register_custom_command(entry)
        except RuntimeError as e:
            await ctx.send('Error: ' + str(e))
        else:
            await self.save_custom_commands()
            await ctx.send(f'Successfully registered command')