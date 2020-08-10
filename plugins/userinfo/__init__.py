from .userinfo import Userinfo

def setup(bot):
    """
    Setup when registering plugin
    """

    # register cog
    bot.add_cog(Userinfo(bot))