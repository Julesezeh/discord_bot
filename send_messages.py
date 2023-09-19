import requests
import os
from dotenv import load_dotenv
import askai

# Fetches environment variables
load_dotenv()

# This sends messages to specified discord servers using python requests
channel_id = os.getenv("LE_SLIME_CHANNEL_ID")
server_url = f"https://discord.com/api/v9/channels/{channel_id}/messages"
auth_token = os.getenv("TOKEN")


# specifies the message to be sent of the request
payload = {"content": "Brodie"}
# specifies the main header attribute
header = {"Authorization": auth_token}

# req = requests.post(server_url, data=payload, headers=header)


def send_message(message):
    response = askai.ask(message)
    payload = {"content": response}
    header = {"Authorization": auth_token}
    channel_id = os.getenv("LE_SLIME_CHANNEL_ID")
    server_url = f"https://discord.com/api/v9/channels/{channel_id}/messages"
    if response:
        req = requests.post(server_url, data=payload, headers=header)
    else:
        req = requests.post(
            url=server_url, headers=header, data={"content": "Ungenerated response"}
        )
