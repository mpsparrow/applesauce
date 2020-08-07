from .manage import Manage
from .manage2 import Manage2

### PLUGIN INFO ###
PLUGIN_NAME = "Plugin Management"
COG_NAMES = ["Manage", "Manage2"]
VERSION = 0.1
AUTHOR = "Matthew Sparrow"
DESCRIPTION = "Provides the basic per guild management features for enabling/disabling plugins."

def setup(bot):
    """
    Setup when registering plugin
    """

    # register cog
    bot.add_cog(Manage(bot))
    bot.add_cog(Manage23(bot))