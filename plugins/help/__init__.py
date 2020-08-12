from .help import Help

def setup(bot):
    """
    Setup when registering plugin
    """

    bot.add_cog(Help(bot))