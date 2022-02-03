import discord
from util import whmcs, config, database

color = 0x00ff04


def is_admin(ctx):
    # Check if a user can use the admin commands
    # Namely list, show & sync
    # Basically all the commands are admin commands
    management = discord.utils.get(ctx.guild.roles, id=guildID)
    developer = discord.utils.get(ctx.guild.roles, id=guildID)
    return management in ctx.author.roles or developer in ctx.author.roles


def error_embed(description):
    # Generic error message
    return discord.Embed(
        color=0xff0000,
        title='An Error Occurred',
        description=description
    )


def normal_embed(description):
    # Generic normal embed message
    return discord.Embed(
        color=color,
        description=description
    )


def warning_embed(description):
    # Generic warning message
    # Basically just sends an embed with a yellow colour
    return discord.Embed(
        color=0xf6ff00,
        description=description
    )


async def total_rank_sync(guild, message):
    # Get the client role
    client = discord.utils.get(guild.roles, id=int(config.get_client_role()))
    # Get the members in the guild
    members = await guild.chunk()
    amount = len(members)
    # Get the synced members from the database
    synced = database.get_synced_members()
    # Iterate through all the members in the guild
    current = 0
    for member in members:
        current = current + 1
        if message is not None:
            # Update the message to keep you informed.
            await message.edit(embed=warning_embed(f"Updating member {current} / {amount}."))
        # If the member is not linked, remove their client role
        if member.id not in synced:
            await member.remove_roles(client)
            continue

        # If the member is synced check if they have 1 or more active products
        client_id = synced[member.id]
        products = whmcs.get_products(client_id)
        # If they don't remove their client role
        if products is None:
            await member.remove_roles(client)
            continue
        # Otherwise, add their client role
        await member.add_roles(client)

    if message is not None:
        # If this function was called by the sync command, update the message that was sent
        await message.edit(embed=normal_embed(f"Successfully synced {len(members)} members."))
