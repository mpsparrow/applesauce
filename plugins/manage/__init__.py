from .manage import Manage

def setup(bot):
    """
    Setup when registering plugin
    """

    bot.add_cog(Manage(bot))