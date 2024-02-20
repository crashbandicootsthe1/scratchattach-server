
import os

os.system("pip cache purge")
os.system("pip install -U scratchattach")

import scratchattach as scratch3
from app import keep_alive
import json

keep_alive()


session = scratch3.Session(
    os.environ["SESSION_ID"], username="crashbandicootsthe1")
conn = session.connect_cloud(968656181)
client = scratch3.CloudRequests(conn)


@client.request
def save_key(username: str, key_name: str, key_value, json_file: str = "storage-data.json"):
    try:
        with open(json_file, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        # If the file doesn't exist, create an empty dictionary
        data = {}

    # If the username doesn't exist in the data, create a new entry
    if username not in data:
        data[username] = {}

    # Add or update the key-value pair for the username
    data[username][key_name] = key_value

    # Write the updated data back to the JSON file
    with open(json_file, 'w') as file:
        json.dump(data, file, indent=4)
        return "Done"


@client.request
def load_keys(username=None):
    if username is None:
        username = session.get_linked_user()
    with open('storage-data.json', 'r') as file:
        data = json.load(file)
        user_data = data.get(username, {})
        key_value_pairs = [item for pair in user_data.items() for item in pair]
        return key_value_pairs


@client.request
def ping():
    return "pong"


@client.event
def on_ready():
    print("Request handler started.")


client.run(no_packet_loss=True)
