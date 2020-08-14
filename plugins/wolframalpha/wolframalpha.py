import discord
from discord.ext import commands
from utils.checks import is_guild_enabled
from .wolframAPI import WolframResult
from abc import ABCMeta, abstractmethod
from utils.interactive import InteractiveEmbed

class WolframEmbed(InteractiveEmbed):
    REACTIONS = {
        "next_pod": "➡️",
        "prev_pod": "⬅️",
        "next_sub": "⬇️",
        "prev_sub": "⬆️"
    }

    def __init__(self, parent, ctx, response):
        super(WolframEmbed, self).__init__(parent.bot, ctx, 60.0)
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

    async def on_reaction(self, reaction, user):
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

    async def add_navigation(self, message):
        await message.add_reaction(WolframEmbed.REACTIONS["prev_pod"])
        await message.add_reaction(WolframEmbed.REACTIONS["next_pod"])

        await message.add_reaction(WolframEmbed.REACTIONS["prev_sub"])
        await message.add_reaction(WolframEmbed.REACTIONS["next_sub"])

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

    async def on_close(self):
        self.parent.activeObjects.pop(self.ctx.guild.id)

class WolframDidYouMeanEmbed(InteractiveEmbed):
    REACTIONS = {
        "yes": "✅",
        "no": "❌"
    }

    def __init__(self, parent, ctx, didyoumean):
        super(WolframDidYouMeanEmbed, self).__init__(parent.bot, ctx, 60.0)
        self.parent = parent
        self.ctx = ctx
        self.owner = self.ctx.author
        self.didyoumean = didyoumean
        
        self.message = None

    async def on_reaction(self, reaction, user):
        if reaction.emoji == WolframDidYouMeanEmbed.REACTIONS["yes"]:
            await self.close_embed()
            await self.parent.query(self.ctx, self.didyoumean)
            return

        if reaction.emoji == WolframDidYouMeanEmbed.REACTIONS["no"]:
            await self.close_embed()
            self.parent.activeObjects.pop(self.ctx.channel.id)
            return
        
    def make_embed(self):
        embed = discord.Embed(
            title = "Wolfram|Alpha Error",
            description = f"Did you mean `{self.didyoumean}`",
            colour = 0xf84722
        )
        return embed

    async def add_navigation(self, message):
        await message.add_reaction(WolframDidYouMeanEmbed.REACTIONS["yes"])
        await message.add_reaction(WolframDidYouMeanEmbed.REACTIONS["no"])

    async def on_close(self):
        self.parent.activeObjects.pop(self.ctx.guild.id)
        await self.message.delete()
        

class WolframAlpha(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.activeObjects = {}

    async def query(self, ctx, query):
        if query is None:
            embed = discord.Embed(
                title = "Wolfram|Alpha Error",
                description = "Please specify a search query: `wolf <query>`",
                colour = 0xf84722
            )
            await ctx.send(embed=embed)
            return

        embed = discord.Embed(
            title = "Wolfram|Alpha",
            description = "Querying Wolfram|Alpha... Hold on",
            colour = 0xc1c100
        )
        load_msg = await ctx.send(embed=embed)
        result = WolframResult(query)
        await load_msg.delete()

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
