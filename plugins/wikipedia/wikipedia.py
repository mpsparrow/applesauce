import discord
import requests
import json
from urllib.parse import quote_plus, quote
from discord.ext import commands
from utils.checks import is_guild_enabled

class Wikipedia(commands.Cog):
    TEMPLATE_URL = "https://en.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exintro&explaintext&redirects=1&titles={0}"
    BASE_URL = "https://www.wikiwand.com/en/{0}"

    def __init__(self, bot):
        self.bot = bot

    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.command(name="wiki", description="Quotes Wikipedia", usage="<query>")
    @is_guild_enabled()
    async def wiki(self, ctx, *, query: str = None):
        if query is None:
            return

        r = requests.get(Wikipedia.TEMPLATE_URL.format(quote(query)))
        if r.status_code != 200:
            embed = discord.Embed(
                title = "Wikipedia Error",
                description = f"Couldn't reach Wikipedia API: {r.status_code}",
                colour = 0xf84722
            )
            await ctx.send(embed=embed)
            return

        data = json.loads(r.text)
        try:
            pageid = list(data["query"]["pages"].keys())[0]
            title = data["query"]["pages"][pageid]["title"]
            extract = data["query"]["pages"][pageid]["extract"].split("\n")[0]

            embed = discord.Embed(
                title = title,
                url = Wikipedia.BASE_URL.format(quote_plus(title).replace("+", "_")),
                description = extract,
                colour = 0xc1c100
            )

        except KeyError:
            embed = discord.Embed(
                title = "Wikipedia Error",
                description = "There is no article with that name",
                colour = 0xf84722
            )

        except Exception:
            embed = discord.Embed(
                title = "Wikipedia Error",
                description = "If you see this then something went horribly wrong",
                colour = 0xf84722
            )

        await ctx.send(embed=embed)
