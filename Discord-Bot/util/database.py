import json
from mysql.connector.pooling import MySQLConnectionPool
from mysql.connector import connect
# Read config file and get information for MySQL database
# This file contains all the functions related to the MySQL database
with open("./config.json", "r+") as config_file:
    config = json.load(config_file)

# pool = MySQLConnectionPool(pool_name='connection_pool',
#                            pool_size=3,
#                            **config['mysql'])


def get_connection():
    return connect(**config['mysql'])


def execute_update(sql: str, *args):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(sql, args)
    connection.commit()
    cursor.close()
    connection.close()


def execute_query(sql, *args):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(sql, args)
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    return result


def create_tables():
    # Create necessary MySQL tables
    execute_update("CREATE TABLE IF NOT EXISTS `whmcs_discord` ("
                   "`client_id` VARCHAR(255) UNIQUE NOT NULL,"
                   "`discord_id` VARCHAR(255) NOT NULL,"
                   "PRIMARY KEY (`client_id`))")


def is_connected_discord(discord_id):
    # Check if a member is connected based on their discord id
    result = execute_query("SELECT * FROM whmcs_discord WHERE discord_id = %s", discord_id)
    return result is not None


def is_connected_client(client_id):
    # Check if a client is connected based on their client_id
    result = execute_query("SELECT * FROM whmcs_discord WHERE client_id = %s", client_id)
    return result is not None


def get_client_id(discord_id):
    # Get a member's client id from their discord_id
    result = execute_query("SELECT client_id FROM whmcs_discord WHERE discord_id = %s", discord_id)
    # Since this function is supposed to return an int, I decided to return a negative value
    # If no client id was found
    if result is None:
        return -1
    # Otherwise convert the data into an int
    return int(result[0])


def get_discord_id(client_id):
    # Get a client's discord id using their client id
    result = execute_query("SELECT discord_id FROM whmcs_discord WHERE client_id = %s", client_id)
    if result is None:
        return None
    return result[0]


def add_client(discord_id, client_id):
    # Insert a linked user into the database
    execute_update("INSERT INTO whmcs_discord(client_id, discord_id) VALUES (%s, %s)", discord_id, client_id)


def remove_client(client_id):
    # Remove a linked user from the database
    # This is used when a client decides to unlink their accounts
    execute_update("DELETE FROM whmcs_discord WHERE client_id = %s", client_id)


def get_synced_members():
    # Get all the synced users in the database
    synced = dict()
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT discord_id, client_id FROM whmcs_discord")
    results = cursor.fetchall()
    # Iterate over them and add them to a dictionary to be used later
    for result in results:
        synced[int(result[0])] = int(result[1])
    cursor.close()
    connection.close()
    # Format is synced[discord_id] = client_id
    return synced
