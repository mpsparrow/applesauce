from .manage import Manage

### PLUGIN INFO ###
PLUGIN_NAME = "Plugissn Management"
COG_NAMES = ["Manage"]
VERSION = 0.1
AUTHOR = "Matthew Sparrow"
DESCRIPTION = "Provides the basic per guild management features for enabling/disabling plugins."

def setup(bot):
    """
    Setup when registering plugin
    """

    # register cog
    bot.add_cog(Manage(bot))