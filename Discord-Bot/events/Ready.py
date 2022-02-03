from discord.ext import commands
from util import database


class Ready(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        # Prints a message to console whenever the bot is started
        print('----------------------------')
        print('Bot Online!')
        print(f'Logged In As {self.bot.user.name})')
        print('----------------------------')
        # Creates necessary MySQL tables.
        database.create_tables()


def setup(bot):
    bot.add_cog(Ready(bot))
