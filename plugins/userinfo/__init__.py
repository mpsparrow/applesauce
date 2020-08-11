from .userinfo import Userinfo

def setup(bot):
    """
    Setup when registering plugin
    """

    bot.add_cog(Userinfo(bot))