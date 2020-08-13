import discord
from discord.ext import commands
from utils.checks import is_guild_enabled
from .wolframAPI import WolframResult
from abc import ABC, abstractmethod

class WolframObject(ABC):
    @abstractmethod
    async def on_react_callback(self, reaction, user):
        pass

    @abstractmethod
    async def show_embed(self):
        pass

class WolframDidYouMean(WolframObject):
    REACTIONS = {
        "yes": "✅",
        "no": "❌"
    }

    def __init__(self, parent, ctx, didyoumean):
        self.parent = parent
        self.ctx = ctx
        self.owner = self.ctx.author
        self.didyoumean = didyoumean
        
        self.message = None

    async def on_react_callback(self, reaction, user):
        if self.message is None:
            return

        if user.id != self.owner.id:
            return

        message = reaction.message
        if message.id != self.message.id:
            return

        if reaction.me:
            if reaction.emoji == WolframDidYouMean.REACTIONS["yes"]:
                await self.message.delete()
                await self.parent.query(self.ctx, self.didyoumean)
                return

            if reaction.emoji == WolframDidYouMean.REACTIONS["no"]:
                self.parent.activeObjects.pop(self.ctx.channel.id)
                return
        
    async def show_embed(self):
        embed = discord.Embed(
            title = "Wolfram|Alpha Error",
            description = f"Did you mean `{self.didyoumean}`",
            colour = 0xf84722
        )

        self.message = await self.ctx.send(embed=embed)
        await self.message.add_reaction(WolframDidYouMean.REACTIONS["yes"])
        await self.message.add_reaction(WolframDidYouMean.REACTIONS["no"])
        


class WolframAlpha(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.activeObjects = {}

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if user == self.bot.user:
            return

        channelid = reaction.message.channel.id
        if channelid not in self.activeObjects:
            return

        await self.activeObjects[channelid].on_react_callback(reaction, user)

    async def query(self, ctx, query):
        if query is None:
            embed = discord.Embed(
                title = "Wolfram|Alpha Error",
                description = "Please specify a search query: `wolf <query>`",
                colour = 0xf84722
            )
            await ctx.send(embed=embed)
            return

        result = WolframResult(query)
        if not result.success:
            if result.didyoumean is None:
                embed = discord.Embed(
                    title = "Wolfram|Alpha Error",
                    description = result.error,
                    colour = 0xf84722
                )
                await ctx.send(embed=embed)
            else:
                self.activeObjects[ctx.channel.id] = WolframDidYouMean(self, ctx, result.didyoumean)
                await self.activeObjects[ctx.channel.id].show_embed()
            
            return
        
        await ctx.send("Gucci Gang")

    @commands.command(name="wolf", description="Searches Wolfram|Alpha", usage="<query>", aliases=["w"])
    @is_guild_enabled()
    async def wolf(self, ctx, *, query: str = None):
        await self.query(ctx, query)
