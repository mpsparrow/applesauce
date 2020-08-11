from .eightball import EightBall

def setup(bot):
    bot.add_cog(EightBall(bot))