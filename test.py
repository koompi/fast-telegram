import os
from telethon import TelegramClient, events, utils
from telethon.sessions import StringSession
from telethon.utils import get_display_name

from dotenv import load_dotenv

load_dotenv('.env')

api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
auth_key = os.getenv('AUTH')


if __name__ == '__main__':

    # @events.register(events.NewMessage(outgoing=True))
    async def handler(event):
        sender = await event.get_sender()
        name = utils.get_display_name(sender)
        print(name, 'said', event.text, '!')
        

    with TelegramClient(StringSession(auth_key), api_id, api_hash) as client:
        client.add_event_handler(handler, event=events.NewMessage)
        client.run_until_disconnected()

