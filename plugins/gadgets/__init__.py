from .rate import Rate
from .chance import Chance
from .eightball import EightBall
from .coinflip import Coinflip

def setup(bot):
    bot.add_cog(Rate(bot))
    bot.add_cog(Chance(bot))
    bot.add_cog(EightBall(bot))
    bot.add_cog(Coinflip(bot))