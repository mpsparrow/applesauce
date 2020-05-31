# Debug cog
# Debug related commands for owner
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
import sys
from util.log import log
from util import config


class Debug(commands.Cog):
    """
    Cog containing debugging commands.
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="log", help="Displays the startup log.", aliases=["startupLog"])
    @commands.is_owner()
    async def startupLog(self, ctx):
        """
        Command to display start log.
        """
        conf = config.readINI('mainConfig.ini')
        await ctx.send(f"```{log.read(conf['logs']['start'])}```")

    @commands.command(name="ping", help="Pings the bot.")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def ping(self, ctx):
        """
        Command to ping the bot.
        """
        await ctx.send('pong!')

    @commands.command(name="debug", help="Versions and other debug information.")
    @commands.is_owner()
    async def debug(self, ctx):
        """
        Command to display versions and other debug information.
        """
        embed=discord.Embed(title='Debug', color=0xc1c100)
        embed.add_field(name="discord.py", value=discord.__version__, inline=False)
        embed.add_field(name="python", value=sys.version, inline=False)
        embed.add_field(name="OS", value=sys.platform, inline=False)
        await ctx.send(embed=embed)

    # guildid (command)
    @commands.command(name="guildid", help="Gets guild ID.", usage="guildid")
    @commands.is_owner()
    async def guildid(self, ctx):
        """
        Command to display guild ID.
        """
        await ctx.send(f'Guild id: {ctx.guild.id}')

    # latency (command)
    @commands.command(name="latency", description="Gets latency to server.", usage="latency")
    @commands.is_owner()
    async def latency(self, ctx):
        """
        Command to display latency.
        """
        await ctx.send(str(round(self.bot.latency * 1000)) + 'ms')

    # close (command)
    @commands.command(name="close", description="Shuts down bot.", usage="close", aliases=['shutdown', 'restart', 'kill'])
    @commands.is_owner()
    async def close(self, ctx):
        """
        Command to shutdown bot.
        """
        await ctx.send("shutting down....")
        await self.bot.close()

    @commands.command(pass_context=True)
    @commands.has_permissions(add_reactions=True,embed_links=True)
    async def helpTest(self,ctx,*cog):
        """Gets all cogs and commands of mine."""
        try:
            if not cog:
                """Cog listing.  What more?"""
                halp=discord.Embed(title='Cog Listing and Uncatergorized Commands',
                                description='Use `!help *cog*` to find out more about them!\n(BTW, the Cog Name Must Be in Title Case, Just Like this Sentence.)')
                cogs_desc = ''
                for x in self.bot.cogs:
                    cogs_desc += ('{} - {}'.format(x,self.bot.cogs[x].__doc__)+'\n')
                halp.add_field(name='Cogs',value=cogs_desc[0:len(cogs_desc)-1],inline=False)
                cmds_desc = ''
                for y in self.bot.walk_commands():
                    if not y.cog_name and not y.hidden:
                        cmds_desc += ('{} - {}'.format(y.name,y.help)+'\n')
                halp.add_field(name='Uncatergorized Commands',value=cmds_desc[0:len(cmds_desc)-1],inline=False)
                await ctx.message.add_reaction(emoji='✉')
                await ctx.message.author.send('',embed=halp)
            else:
                """Helps me remind you if you pass too many args."""
                if len(cog) > 1:
                    halp = discord.Embed(title='Error!',description='That is way too many cogs!',color=discord.Color.red())
                    await ctx.message.author.send('',embed=halp)
                else:
                    """Command listing within a cog."""
                    found = False
                    for x in self.bot.cogs:
                        for y in cog:
                            if x == y:
                                halp=discord.Embed(title=cog[0]+' Command Listing',description=self.bot.cogs[cog[0]].__doc__)
                                for c in self.bot.get_cog(y).get_commands():
                                    if not c.hidden:
                                        halp.add_field(name=c.name,value=c.help,inline=False)
                                found = True
                    if not found:
                        """Reminds you if that cog doesn't exist."""
                        halp = discord.Embed(title='Error!',description='How do you even use "'+cog[0]+'"?',color=discord.Color.red())
                    else:
                        await ctx.message.add_reaction(emoji='✉')
                    await ctx.message.author.send('',embed=halp)
        except:
            await ctx.send("Excuse me, I can't send embeds.")

def setup(bot):
    bot.add_cog(Debug(bot))