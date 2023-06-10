import requests
import os
from dotenv import load_dotenv

# Fetches environment variables
load_dotenv()
# This sends messages to specified discord servers
channel_id = os.getenv("LE_SLIME_CHANNEL_ID")
server_url = f"https://discord.com/api/v9/channels/{channel_id}/messages"
print(server_url)
auth_token = os.getenv("TOKEN")

payload = {"content": "BRozay"}
header = {"Authorization": auth_token}

req = requests.post(server_url, data=payload, headers=header)
