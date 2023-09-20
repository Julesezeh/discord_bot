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


async def add_to_file(data):
    try:
        author = data["d"]["author"]["username"]
        id = data["d"]["author"]["id"]
        message = data["d"]["content"]
        date = data["d"]["timestamp"]
    except KeyError as e:
        return str(e)
    text = {
        "user": {"username": author, "id": id},
        "message": message,
        "timestamp": date,
    }
    with await open("history.txt", "w+") as file:
        file.append(text)
        file.close()


def heartbeat(ws, heartbeat_):
    print("Heartbeat begins")
    while True:
        time.sleep(heartbeat_)
        heartbeat_payload = {"op": 1, "d": "null"}
        send_json_request(ws, heartbeat_payload)
        print("heartbeat sent")


async def await_close(ws):
    await ws.wait_closed()


ws = websocket.WebSocket()

# To get messages from the server
ws.connect("wss://gateway.discord.gg/?encoding=json")

heartbeat_interval = receive_json_response(ws)["d"]["heartbeat_interval"] / 1000

hb = threading.Thread(target=heartbeat, args=(ws, heartbeat_interval))
hb.start()

token = token_

payload = {
    "op": 2,
    "d": {
        "token": token,
        "properties": {"os": "Windows", "browser": "chrome", "device": "pc"},
    },
}

send_json_request(ws, payload)


while True:
    event = receive_json_response(ws)
    try:
        if event["t"] == "MESSAGE_CREATE":
            print(event)
            content = event["d"]["content"]
            author = event["d"]["author"]["username"]
            print(f"{author}: {content}")
            add_to_file(event)
            if event["d"]["channel_id"] == "1076208583412297860":
                print("valid ID")
                send_messages.send_message(content)
            else:
                print(event["d"]["channel_id"])
                print("Invalid ID")
    except Exception as e:
        print(e)
# break
