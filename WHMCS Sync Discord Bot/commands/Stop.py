import requests
from discord.ext import commands
from util import config


class Stop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def stop(self, ctx):
        # This is intended to be used only be the developers of the bot
        # I use this to stop the bot "correctly" rather than Ctrl C
        if ctx.author.id in [234255082345070592, 776169322178805797]:
            print('[Company] Stop Command Received!')
            # Sends stop request to web server
            requests.get(f'http://127.0.0.1:{config.get_port()}/h3h24j')
            # Deletes original message
            await ctx.message.delete()
            # Stop the bot
            await self.bot.logout()


def setup(bot):
    bot.add_cog(Stop(bot))
