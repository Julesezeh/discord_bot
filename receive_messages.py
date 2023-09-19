import websocket, os, json, threading, time
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


def heartbeat(ws, heartbeat_):
    print("Heartbeat begins")
    while True:
        time.sleep(heartbeat_)
        heartbeat_payload = {"op": 1, "d": "null"}


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
        "properties": {"os": "Windows", "browser": "chrome", "device": "pc"},
    },
}

heartbeat_interval = receive_json_response(ws)["d"]["heartbeat_interval"]

send_json_request(ws, payload)

ws.ping()

while True:
    event = receive_json_response(ws)
    try:
        if event["t"] == "MESSAGE_CREATE":
            print(event)
            content = event["d"]["content"]
            author = event["d"]["author"]["username"]
            print(f"{author}: {content}")
            send_messages.send_message(content)
    except Exception as e:
        print(e)
# break
