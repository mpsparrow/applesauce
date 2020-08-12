from .coinflip import Coinflip

def setup(bot):
    bot.add_cog(Coinflip(bot))