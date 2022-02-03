import discord
from discord.ext import commands
from util import config, whmcs, other, database
from datetime import datetime


# Show all the products of a linked user
# eg: -show @emil

class Show(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    @commands.check(other.is_admin)
    async def show(self, ctx, member: discord.Member):
        # Send original message
        message = await ctx.send(embed=other.warning_embed(f"Fetching **{str(member)}**'s Information"))
        # Check the database to see if the mentioned user is linked
        client_id = database.get_client_id(member.id)
        # If the user is not linked, send an error message
        if client_id < 0:
            await message.edit(
                embed=other.error_embed(f"{str(member)} hasn't connected their discord & whmcs accounts."))
            return
        # Use the fetched client_id from database to get information about the user
        details = whmcs.get_details_by_id(client_id)

        # If the api fails to get information send error message
        if details['result'] != 'success':
            await message.edit(embed=other.error_embed(f"Unable to get information about **{str(member)}**"))
            return

        # Create new embed to be sent
        embed = discord.Embed(
            color=other.color,
            timestamp=datetime.utcnow()
        )
        embed.set_author(
            name=f"{str(member)}'s Information",
            icon_url=member.avatar_url
        )
        # Get information about the user through the api
        embed.add_field(
            name="Name:",
            value=details['fullname'],
            inline=False
        )
        embed.add_field(
            name="Email:",
            value=details['email'],
            inline=False
        )
        embed.add_field(
            name="Amount Paid:",
            value=details['stats']['paidinvoicesamount'],
            inline=False
        )
        # Get the user's products
        products = whmcs.get_products(client_id)
        products_num = int(details['stats']['productsnumtotal'])
        # This is experimental, not sure if it'll work properly
        # But if the user has too many products to send in one embed, this attempts to break it down
        # into several embeds
        products_split = products.split("\n\n")
        if products is None or products_num == 0:
            embed.add_field(
                name="Products:",
                value="No Products",
                inline=False
            )
        elif products_num < 3:
            embed.add_field(
                name="Products:",
                value=products,
                inline=False
            )
        else:
            embed.add_field(
                name="Products",
                value="\n\n".join(products_split[0:3]),
                inline=False
            )
        # Edit original message
        await message.edit(embed=embed)
        # If surplus of products, send necessary embeds.
        if products_num > 3:
            for x in range(int(products_num / 3)):
                embed = discord.Embed(
                    color=other.color,
                    timestamp=datetime.utcnow()
                )
                embed.set_author(
                    name=f"{str(member)}'s Information | Page {x + 2}",
                    icon_url=member.avatar_url
                )
                index = (x + 1) * 3
                embed.add_field(
                    name="Products",
                    value="\n\n".join(products_split[index:index + 3]),
                    inline=False
                )
                await ctx.send(embed=embed)

    @show.error
    async def show_error(self, ctx, error):
        # If the user fails the 'is_admin' check send error message
        if isinstance(error, commands.CheckFailure):
            await ctx.send(embed=other.error_embed("You do not have permission to complete this action"))
        # if the user fails to mention a member
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(embed=other.error_embed(f"Invalid Syntax: `{config.get_prefix()}show (@user)`"))
        # If the user says something random instead of mentioning a member
        elif isinstance(error, commands.BadArgument):
            await ctx.send(embed=other.error_embed("Please mention a valid member."))
        # Used for debugging
        else:
            print(error)


def setup(bot):
    bot.add_cog(Show(bot))
