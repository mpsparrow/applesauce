from .wolframalpha import WolframAlpha

def setup(bot):
    bot.add_cog(WolframAlpha(bot))