from .userinfo import Userinfo

### PLUGIN INFO ###
PLUGIN_NAME = "Userinfo"
COG_NAMES = ["Userinfo"]
VERSION = 0.1
AUTHOR = "Lauchmelder"
DESCRIPTION = "A tool to provide discord user information"
LOAD_ON_START = True
REQUIRED = False
HIDDEN = False

def setup(bot):
    """
    Setup when registering plugin
    """

    # register cog
    bot.add_cog(Userinfo(bot))