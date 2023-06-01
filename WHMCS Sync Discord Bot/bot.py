import discord
from discord.ext import commands
import asyncio
from flask import Flask, request, Response, jsonify
import threading
from util import database, whmcs, other, config
from datetime import datetime

app = Flask(__name__)
loop = asyncio.get_event_loop()


@app.errorhandler(404)
def not_found_error(error):
    r = Response()
    r.headers.add('Location', "website")
    r.status_code = 301
    return r


def shutdown_server():
    # Stops the web server
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


@app.route('/h3h24j', methods=['GET'])
def shutdown():
    # Route to stop the web server
    shutdown_server()
    return 'Shutting Website'


async def rank_sync(client_id, discord_id):
    # Sync a newly linked user
    if client_id < 0:
        return
    guild = bot.get_guild(guildID)
    member = await guild.fetch_member(int(discord_id))
    if member is None:
        return
    client = discord.utils.get(member.guild.roles, id=int(config.get_client_role()))
    products = whmcs.get_products(client_id)
    if products is None:
        await member.remove_roles(client)
        return False
    await member.add_roles(client)
    return True


async def remove_rank(discord_id):
    # Remove the client role from someone who unlinks their account
    guild = bot.get_guild(guildID)
    member = await guild.fetch_member(int(discord_id))
    if member is None:
        return
    client = discord.utils.get(member.guild.roles, id=int(config.get_client_role()))
    await member.remove_roles(client)


@app.route('/client/add', methods=['POST'])
def client_add():
    # Route to add a new client
    client_id = request.form['client_id']
    discord_id = request.form['discord_id']

    if client_id is None or discord_id is None:
        return jsonify(result="failure")

    if database.is_connected_discord(discord_id):
        return jsonify(result="connected")

    database.add_client(client_id, discord_id)
    loop.create_task(rank_sync(int(client_id), discord_id))
    return jsonify(result="success")


@app.route('/client/remove', methods=['POST'])
def client_remove():
    # Route to remove a client
    client_id = request.form['client_id']

    if client_id is None:
        return jsonify(result="failure")
    discord_id = database.get_discord_id(client_id)
    if discord_id is None:
        return jsonify(result="unconnected")
    database.remove_client(client_id)
    loop.create_task(remove_rank(discord_id))
    return jsonify(result="success")


class Website(threading.Thread):
    def run(self):
        print('Website Starting')
        app.run(host='0.0.0.0', port=config.get_port(), threaded=True)


bot = commands.Bot(command_prefix=config.get_prefix(), command_not_found='', intents=discord.Intents.all())
bot.remove_command('help')

ext = ['commands.Stop', 'commands.List', 'commands.Show', 'commands.Sync',
       'events.Ready']


async def auto_sync():
    await bot.wait_until_ready()
    while bot.is_ready():
        print(f"[AtlasNode] Running Auto Client Sync at {datetime.utcnow()}")
        await other.total_rank_sync(bot.get_guild(777284420196630588), None)
        # How often the auto sync should run in seconds
        await asyncio.sleep(28800)

if __name__ == '__main__':
    # STart the web server
    Website().start()
    for ex in ext:
        try:
            # Load all the extensions(commands & events)
            bot.load_extension(ex)
        except Exception as error:
            print('{} cannot be loaded. [{}]'.format(ex, error))

# Interval auto syncs
bot.loop.create_task(auto_sync())
# Start the bot
bot.run(config.get_token(), reconnect=True)

