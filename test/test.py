from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse

from telethon import TelegramClient, events, utils
from telethon.sessions import StringSession

api_id = 1060273
api_hash = 'd5b143b9482b385a081de9f8c39e30c1'
auth_key = '1BVtsOHEBu4icUCHuls4bDoQDQrtTwXuJLTg0zHz3GGswWhKd9HqS_rRZSOs2lGL_zF9MqOsDI28yf8ZNixNBZtuS_jqR961vJqAXJhYb9HTJ6_GU64ElzI5gSiMAyPv2RpbHOS1z2yxiUgxQsm8AO0KDegt-VjRIm5RrNURheljc2kEKlt9VtUFStFg2L9Yg4F87xavuCMH5sMMc-YOiusDNL_2AL1eTXFNm-tDEp7_llwUmlgl54Ue0ycLnqBBj3nSYA6CjDxIWvSZ9XSDqYyZEVImqj4p6Hb99IsirnhckG39hE_7Bk2zna52oWxXvNR1skj2MD6yXkONb0HNXLf6KSRf-zJs='


app = FastAPI()

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>Telegram Chat</h1>
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


@app.get("/")
async def get():
    return HTMLResponse(html)

# client = TelegramClient(StringSession(auth_key), api_id, api_hash).start()


# @client.on(events.NewMessage(outgoing=True))
# async def handler(event):
#     sender = await event.get_sender()
#     name = utils.get_display_name(sender)
#     print(name, 'said', event.text, '!')
#     return name

data = []


async def telegram_handler(event):
    sender = await event.get_sender()
    name = utils.get_display_name(sender)
    data.append(event.text)


async def live_message(websocket, client):
    await websocket.accept()
    while True:
        client.add_event_handler(
            telegram_handler, event=events.NewMessage(outgoing=True))
        await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    client = TelegramClient(StringSession(auth_key), api_id, api_hash)
    client = await client.start()
    await live_message(websocket, client)
# uvicorn test:app --reload
