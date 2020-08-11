from .customcmd import CustomCMD

def setup(bot):
    """
    Setup when registering plugin
    """

    bot.add_cog(CustomCMD(bot))