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

class WolframEmbed(WolframObject):
    REACTIONS = {
        "next_pod": "➡️",
        "prev_pod": "⬅️",
        "next_sub": "⬇️",
        "prev_sub": "⬆️"
    }

    def __init__(self, parent, ctx, response):
        self.parent = parent
        self.ctx = ctx
        self.owner = self.ctx.author
        self.response = response
        
        self.message = None

        self.current_pod = 1
        self.current_subpod = 0

    def next_pod(self):
        self.current_pod += 1
        if self.current_pod >= self.response.num_pods:
            self.current_pod = 1
        self.current_subpod = 0

    def prev_pod(self):
        self.current_pod -= 1
        if self.current_pod < 1:
            self.current_pod = self.response.num_pods - 1
        self.current_subpod = 0


    def next_subopd(self):
        self.current_subpod += 1
        if self.current_subpod >= self.response.pods[self.current_pod].num_subpods:
            self.current_subpod = 0


    def prev_subpod(self):
        self.current_subpod -= 1
        if self.current_subpod < 0:
            self.current_subpod = self.response.pods[self.current_pod].num_subpods - 1

    async def on_react_callback(self, reaction, user):
        if self.message is None:
            return

        if user.id != self.owner.id:
            return

        message = reaction.message
        if message.id != self.message.id:
            return

        if reaction.me:
            if reaction.emoji == WolframEmbed.REACTIONS["prev_pod"]:
                self.prev_pod()
                await reaction.remove(user)

            if reaction.emoji == WolframEmbed.REACTIONS["next_pod"]:
                self.next_pod()
                await reaction.remove(user)

            if reaction.emoji == WolframEmbed.REACTIONS["prev_sub"]:
                self.prev_subpod()
                await reaction.remove(user)

            if reaction.emoji == WolframEmbed.REACTIONS["next_sub"]:
                self.next_subopd()
                await reaction.remove(user)

            await self.update_embed()

    async def show_embed(self):
        self.message = await self.ctx.send(embed=self.make_embed())

        await self.message.add_reaction(WolframEmbed.REACTIONS["prev_pod"])
        await self.message.add_reaction(WolframEmbed.REACTIONS["next_pod"])

        await self.message.add_reaction(WolframEmbed.REACTIONS["prev_sub"])
        await self.message.add_reaction(WolframEmbed.REACTIONS["next_sub"])

    async def update_embed(self):
        await self.message.edit(embed=self.make_embed())

    def make_embed(self):
        pod = self.response.pods[self.current_pod]
        subpod = pod.subpods[self.current_subpod]
        embed = discord.Embed(
            title = pod.title,
            description = subpod.plaintext,
            colour = 0xc1c100
        )

        embed.set_image(url = subpod.img_src)
        embed.set_thumbnail(url = self.response.pods[0].subpods[0].img_src)

        footer_text = f"Pod {self.current_pod}/{self.response.num_pods - 1}"
        if pod.num_subpods > 1:
            footer_text += f" [Subpod {self.current_subpod + 1}/{pod.num_subpods}]"
        embed.set_footer(text=footer_text)
        
        return embed

class WolframDidYouMeanEmbed(WolframObject):
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
            if reaction.emoji == WolframDidYouMeanEmbed.REACTIONS["yes"]:
                await self.message.delete()
                await self.parent.query(self.ctx, self.didyoumean)
                return

            if reaction.emoji == WolframDidYouMeanEmbed.REACTIONS["no"]:
                self.parent.activeObjects.pop(self.ctx.channel.id)
                return
        
    async def show_embed(self):
        embed = discord.Embed(
            title = "Wolfram|Alpha Error",
            description = f"Did you mean `{self.didyoumean}`",
            colour = 0xf84722
        )

        self.message = await self.ctx.send(embed=embed)
        await self.message.add_reaction(WolframDidYouMeanEmbed.REACTIONS["yes"])
        await self.message.add_reaction(WolframDidYouMeanEmbed.REACTIONS["no"])
        


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
                self.activeObjects[ctx.channel.id] = WolframDidYouMeanEmbed(self, ctx, result.didyoumean)
                await self.activeObjects[ctx.channel.id].show_embed()
            
            return

        self.activeObjects[ctx.channel.id] = WolframEmbed(self, ctx, result)
        await self.activeObjects[ctx.channel.id].show_embed()

    @commands.command(name="wolf", description="Searches Wolfram|Alpha", usage="<query>", aliases=["w"])
    @is_guild_enabled()
    async def wolf(self, ctx, *, query: str = None):
        await self.query(ctx, query)
