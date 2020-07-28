from fastapi import FastAPI

from telethon import TelegramClient, events
from telethon.sessions import StringSession

import os
from dotenv import load_dotenv

load_dotenv('.env')

api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
auth_key = os.getenv('AUTH')


app = FastAPI()


async def handler(event):
    print(event.text)


async def tele_event():
    client = TelegramClient(StringSession(auth_key), api_id, api_hash)
    await client.connect()
    client.add_event_handler(handler, event=events.NewMessage)
    await client.run_until_disconnected()


@app.get("/")
async def read_root():
    await tele_event()

# uvicorn main:app --reload
