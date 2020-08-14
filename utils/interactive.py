import discord
from discord.ext import commands
from abc import ABC, abstractmethod
import asyncio

class InteractiveEmbed(ABC):
    """
    This abstract base class can be used to create interactive embeds
    """
    def __init__(self, bot, ctx, timeout):
        """
        Sets up the embed with needed parameters
        bot: The bot hosting this embed
        ctx: The context that caused this embed
        timeuout: The time until the embed times out (in seconds)
        """
        self.bot = bot
        self.ctx = ctx
        self.message = None
        self.timeout = timeout

    @abstractmethod
    async def on_reaction(self, reaction, user):
        """
        Gets called when the user interacted with the embed
        """
        pass

    @abstractmethod
    def make_embed(self):
        """
        Creates and returns a new embed
        """
        pass

    @abstractmethod
    async def add_navigation(self, message):
        """
        Adds the navigational emotes to the embed
        """
        pass

    async def on_close(self):
        """
        Can be overridden. Gets called when the embed is closed
        """
        pass

    def additional_checks(self, reaction, user):
        """
        Can be overridden. Additional checks to do before calling on_reaction()
        """
        return True

    async def show_embed(self):
        """
        Displays an embed / Creates an embed
        """
        if self.message is None:
            self.message = await self.ctx.send(embed=self.make_embed())
            await self.add_navigation(self.message)

        else:
            await self.message.edit(embed=self.make_embed())

        def check(reaction, user):
            if self.message is None:
                return False

            if user.id != self.ctx.author.id:
                return False

            if reaction.message.id != self.message.id:
                return False

            if not reaction.me:
                return False

            return self.additional_checks(reaction, user)

        try:
            reaction, user = await self.bot.wait_for("reaction_add", check=check, timeout=self.timeout)
            await self.on_reaction(reaction, user)
            await self.show_embed()
        except asyncio.TimeoutError:
            await self.close_embed()

    async def close_embed(self):
        """
        Close this embed
        """
        await self.message.clear_reactions()
        await self.on_close()
