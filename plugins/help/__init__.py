from .help import AdvancedHelp

def setup(bot):
    """
    Setup when registering plugin
    """

    bot.add_cog(AdvancedHelp(bot))