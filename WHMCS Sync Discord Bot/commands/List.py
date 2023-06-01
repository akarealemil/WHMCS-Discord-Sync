import discord
from discord.ext import commands
from util import config, whmcs, other
from datetime import datetime

# List all the products of a specified email
# eg: -list test@gmail.com

class List(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    @commands.check(other.is_admin)
    async def list(self, ctx, email: str):
        # Sends original message
        message = await ctx.send(embed=other.warning_embed("Fetching Client Information"))
        # Get the details of the specified email
        details = whmcs.get_details_by_email(email)

        # If not successful, send error message
        if details['result'] != 'success':
            await message.edit(embed=other.error_embed(f"Unable to find a client with the email `{email}`"))
            return
        # If the client has no products send other error message
        if int(details['stats']['productsnumtotal']) < 1:
            await message.edit(embed=other.error_embed("That client has no products."))
            return
        # Use different api endpoint to get detailed information about products
        user_id = details['userid']
        embed = discord.Embed(
            color=other.color,
            title=f"{details['fullname']}'s Products",
            description=whmcs.get_products(user_id),
            timestamp=datetime.utcnow()
        )
        # Update original message with detailed information about other products
        await message.edit(embed=embed)

    @list.error
    async def list_error(self, ctx, error):
        # If the user fails the 'is_admin' check, send error message.
        if isinstance(error, commands.CheckFailure):
            await ctx.send(embed=other.error_embed("You do not have permission to complete this action"))
        # If the user doesn't specify an email address, send error message.
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(embed=other.error_embed(f"Invalid Syntax: `{config.get_prefix()}list (email)`"))
        # Used for debugging
        else:
            print(error)


def setup(bot):
    bot.add_cog(List(bot))
