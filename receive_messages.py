import websocket, os, json
from dotenv import load_dotenv
import send_messages

load_dotenv()
token_ = os.getenv("TOKEN")
print("token", token_)


def send_json_request(ws, request):
    ws.send(json.dumps(request))


def receive_json_response(ws):
    response = ws.recv()
    if response:
        return json.loads(response)


async def await_close(ws):
    await ws.wait_closed()


ws = websocket.WebSocket()

# To get messages from the server
ws.connect("wss://gateway.discord.gg/?encoding=json")

token = token_

payload = {
    "op": 2,
    "d": {
        "token": token,
        "intents": "513",
        "properties": {"os": "Windows", "browser": "chrome", "device": "pc"},
    },
}

heartbeat_interval = receive_json_response(ws)["d"]["heartbeat_interval"]

send_json_request(ws, payload)

ws.ping()

while True:
    event = receive_json_response(ws)
    try:
        content = event["d"]["content"]
        author = event["d"]["author"]["username"]
        print(f"{author}: {content}")
        send_messages.send_message(content)
    except Exception as e:
        print(str(e))
# break
