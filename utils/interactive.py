import discord
from discord.ext import commands
from abc import ABC, abstractmethod
import asyncio

class InteractiveEmbed(ABC):
    def __init__(self, bot, ctx, timeout):
        self.bot = bot
        self.ctx = ctx
        self.message = None
        self.timeout = timeout

    @abstractmethod
    async def on_reaction(self, reaction, user):
        pass

    @abstractmethod
    def make_embed(self):
        pass

    @abstractmethod
    async def add_navigation(self, message):
        pass

    def additional_checks(self, reaction, user):
        return True

    async def show_embed(self):
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
        except TimeoutError:
            await self.close_embed()

    async def close_embed(self):
        await self.message.clear_reactions()
