from discord.ext import commands

from util import other


# Manually syncs all members of the discord
# If they're connected and have one or more active products, they receive the client role
# Otherwise they lose it


class Sync(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    @commands.is_owner()
    async def sync(self, ctx):
        # Deletes original message
        await ctx.message.delete()
        # Sends information message
        message = await ctx.send(embed=other.warning_embed("Manually syncing all members. This may take a while..."))
        # Function to sync all members
        await other.total_rank_sync(ctx.author.guild, message)

    @sync.error
    async def show_error(self, ctx, error):
        # If user fails 'is_admin' check
        if isinstance(error, commands.CheckFailure):
            await ctx.send(embed=other.error_embed("You do not have permission to use this command."))


def setup(bot):
    bot.add_cog(Sync(bot))
