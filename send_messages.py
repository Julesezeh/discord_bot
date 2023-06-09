import requests
import os
from dotenv import load_dotenv

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

req = requests.post(server_url, data=payload, headers=header)
