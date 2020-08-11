from .rate import Rate

def setup(bot):
    bot.add_cog(Rate(bot))