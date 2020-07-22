import os
from telethon import TelegramClient, events, utils
from telethon.sessions import StringSession
from dotenv import load_dotenv

load_dotenv('.env')

api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
auth_key = os.getenv('AUTH')


if __name__ == '__main__':

    async def handler(event):
        chat = await event.get_chat()
        name = utils.get_display_name(chat)
        print(name, 'said', event.text)
        return event.text

    with TelegramClient(StringSession(auth_key), api_id, api_hash) as client:
        name = client.add_event_handler(handler, event=events.NewMessage)
        print(name)
        client.run_until_disconnected()
