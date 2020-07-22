from fastapi import FastAPI
from telethon import TelegramClient, events
from telethon.sessions import StringSession
import asyncio
import json
import os
from dotenv import load_dotenv

load_dotenv('.env')

API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')
auth_key = os.getenv('AUTH')

loop = asyncio.get_event_loop()
app = FastAPI()

messages_list = []


class Telegrem:
    def __init__(self, bot_token, api_id, api_hash):
        self.bot_token = bot_token
        self.api_id = api_id
        self.api_hash = api_hash
        self.client = TelegramClient('bot', api_id, api_hash)

    async def receive_message(self, event):
        print(f'message is here {event.raw_text}')
        messages_list.append(event.raw_text)

    async def start_polling(self):
        await self.client.start(bot_token=self.bot_token)
        self.client.add_event_handler(self.receive_message, events.NewMessage)


async def background():
    telegrem = TelegramClient(StringSession(auth_key), API_ID, API_HASH)
    loop.create_task(telegrem.start_polling())


@app.route('/')
async def hello():
    return json.dumps(messages_list)

# loop.create_task(background())

