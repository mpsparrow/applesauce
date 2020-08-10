from .customcmd import CustomCMD

### PLUGIN INFO ###
PLUGIN_NAME = "Custom Commands"
COG_NAMES = ["CustomCMD"]
VERSION = 0.1
AUTHOR = "Matthew Sparrow"
DESCRIPTION = "Creation of custom commands"
LOAD_ON_START = True
REQUIRED = False
HIDDEN = False
ALWAYS_ALLOW = False

def setup(bot):
    """
    Setup when registering plugin
    """

    # register cog
    bot.add_cog(CustomCMD(bot))