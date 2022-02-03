import json
import requests

with open("./config.json", "r+") as config_file:
    # Load all needed whmcs details from the config.json
    config = json.load(config_file)
    url = config['api']['url']
    if not url.endswith("/"):
        url = url + "/"
    # Set the endpoint for all whmcs requests
    api_url = f"{config['api']['url']}includes/api.php"
    identifier = config['api']['identifier']
    secret = config['api']['secret']
    access_key = config['api']['access_key']


def get_details_by_email(email: str):
    # Get a client's details through their email
    payload_tuples = [
        ('identifier', identifier),
        ('secret', secret),
        ('accesskey', access_key),
        ('email', email),
        ('stats', True),
        ('action', 'GetClientsDetails'),
        ('responsetype', 'json')]
    response = requests.post(api_url, data=payload_tuples)
    return response.json()


def get_details_by_id(client_id):
    # Get a client's details through their client_id
    payload_tuples = [
        ('identifier', identifier),
        ('secret', secret),
        ('accesskey', access_key),
        ('clientid', int(client_id)),
        ('stats', True),
        ('action', 'GetClientsDetails'),
        ('responsetype', 'json')]
    response = requests.post(api_url, data=payload_tuples)
    return response.json()


def get_products(client_id):
    # Get a client's products
    payload_tuples = [
        ('identifier', identifier),
        ('secret', secret),
        ('accesskey', access_key),
        ('clientid', int(client_id)),
        ('action', 'GetClientsProducts'),
        ('responsetype', 'json')]
    response = requests.post(api_url, data=payload_tuples)
    data = response.json()
    if data is None:
        return None
    if data['result'] != 'success':
        return None
    if int(data['totalresults']) < 0:
        return None
    products = ""
    for product in data['products']['product']:
        # Remove this if statement if you want all products to be shown
        if product['status'] == 'Active':
            products += f":white_medium_small_square: {product['translated_name']}\n"
            products += f"  :white_small_square: Status: {product['status']}\n"
            if product['groupname'] == 'Web Hosting':
                products += f"  :white_small_square: Domain: {product['domain']}\n"
            elif product['groupname'] == 'Minecraft Hosting':
                products += f"  :white_small_square: Server IP: {product['serverip']}\n"
            products += f"  :white_small_square: Due Date: {product['nextduedate']}\n"
            products += f"  :white_small_square: Payment Method: {product['paymentmethodname']}\n"
            products += "\n"
    if products == "":
        return None
    return products
