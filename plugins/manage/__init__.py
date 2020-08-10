from .manage import Manage

### PLUGIN INFO ###
PLUGIN_NAME = "Plugin Management"
COG_NAMES = ["Manage"]
VERSION = 0.1
AUTHOR = "Matthew Sparrow"
DESCRIPTION = "Core plugin management commands"
LOAD_ON_START = True
REQUIRED = True
HIDDEN = False
ALWAYS_ALLOW = True

def setup(bot):
    """
    Setup when registering plugin
    """

    # register cog
    bot.add_cog(Manage(bot))