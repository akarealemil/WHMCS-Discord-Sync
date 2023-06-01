import json

# Read config file and get needed information
with open("./config.json", "r+") as config_file:
    config = json.load(config_file)


def get_url():
    url = config['api']['url']
    if not url.endswith("/"):
        url = url + "/"
    return url


def get_token():
    return config['bot']['token']


def get_prefix():
    return config['bot']['prefix']


def get_port():
    return int(config['bot']['port'])


def get_client_role():
    return int(config['variables']['client_role_id'])



