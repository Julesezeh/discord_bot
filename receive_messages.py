import websocket
import json
from dotenv import load_dotenv
import os

load_dotenv()
token_ = os.getenv("TOKEN")


def send_json_request(ws, request):
    ws.send(json.dumps(request))


def receive_json_response(ws):
    response = ws.recv()
    if response:
        return json.loads(response)


ws = websocket.WebSocket()
ws.connect("wss://gateway.discord.gg/?v=9&encoding=json")
heartbeat_interval = receive_json_response(ws)["d"]
token = token_
payload = {
    "op": 2,
    "d": {
        "token": token,
        "intents": "513",
        "properties": {"$os": "Linux", "$browser": "chrome", "$device": "pc"},
    },
}

send_json_request(ws, payload)

# To get messages from the server
while True:
    event = receive_json_response(ws)
    try:
        # print(event)
        content = event["d"]["content"]
        author = event["d"]["author"]["username"]
        print(f"{author}: {content}")
    except:
        pass
