from .plugins import Plugins

def setup(bot):
    """
    Setup when registering plugin
    """

    bot.add_cog(Plugins(bot))