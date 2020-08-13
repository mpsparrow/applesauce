from .trivia import Trivia

def setup(bot):
    bot.add_cog(Trivia(bot))