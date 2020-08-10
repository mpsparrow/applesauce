from .guilds import Guilds

def setup(bot):
    """
    Setup when registering plugin
    """

    bot.add_cog(Guilds(bot))