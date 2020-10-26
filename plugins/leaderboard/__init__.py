from .leaderboard import Leaderboard

def setup(bot):
    """
    Setup when registering plugin
    """

    bot.add_cog(Leaderboard(bot))