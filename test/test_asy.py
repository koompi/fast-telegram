from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse

# ---------------------------------------------
from telethon import TelegramClient, events
from telethon.sessions import StringSession
import os
from dotenv import load_dotenv

load_dotenv('.env')

api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
auth_key = os.getenv('AUTH')

# --------------------------------------------------

app = FastAPI()

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost:8000/ws");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


async def handler(event):
    print(event.text)


async def tele_event():
    client = TelegramClient(StringSession(auth_key), api_id, api_hash)
    await client.connect()
    print("start telegram")
    client.add_event_handler(handler, event=events.NewMessage)
    await client.run_until_disconnected()


@app.get("/")
async def get():
    return HTMLResponse(html)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        await tele_event()
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")

# uvicorn main:app --reload
