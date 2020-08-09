from .debugger import Debugger

### PLUGIN INFO ###
PLUGIN_NAME = "Debugger"
COG_NAMES = ["Debugger"]
VERSION = 0.1
AUTHOR = "Matthew Sparrow"
DESCRIPTION = "Debugging tools for owners"
LOAD_ON_START = False
REQUIRED = False
HIDDEN = True

def setup(bot):
    """
    Setup when registering plugin
    """

    # register cog
    bot.add_cog(Debugger(bot))