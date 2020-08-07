from .customcmd import CustomCMD

### PLUGIN INFO ###
PLUGIN_NAME = "Custom Commandss"
COG_NAMES = ["CustomCMD"]
VERSION = 0.1
AUTHOR = "Matthew Sparrow"
DESCRIPTION = "Creation of custom commands."

def setup(bot):
    """
    Setup when registering plugin
    """

    # register cog
    bot.add_cog(CustomCMD(bot))