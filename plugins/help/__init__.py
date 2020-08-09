from .help import AdvancedHelp

### PLUGIN INFO ###
PLUGIN_NAME = "Help"
COG_NAMES = ["AdvancedHelp"]
VERSION = 0.1
AUTHOR = "Matthew Sparrow"
DESCRIPTION = "An advanced help command set"
LOAD_ON_START = True
REQUIRED = True
HIDDEN = False

def setup(bot):
    """
    Setup when registering plugin
    """

    # register cog
    bot.add_cog(AdvancedHelp(bot))