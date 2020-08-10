from .debugger import Debugger

def setup(bot):
    """
    Setup when registering plugin
    """

    bot.add_cog(Debugger(bot))