import time
from telethon import TelegramClient, events, utils
from telethon.sessions import StringSession

api_id = 1060273
api_hash = 'd5b143b9482b385a081de9f8c39e30c1'
auth_key = '1BVtsOHEBu4icUCHuls4bDoQDQrtTwXuJLTg0zHz3GGswWhKd9HqS_rRZSOs2lGL_zF9MqOsDI28yf8ZNixNBZtuS_jqR961vJqAXJhYb9HTJ6_GU64ElzI5gSiMAyPv2RpbHOS1z2yxiUgxQsm8AO0KDegt-VjRIm5RrNURheljc2kEKlt9VtUFStFg2L9Yg4F87xavuCMH5sMMc-YOiusDNL_2AL1eTXFNm-tDEp7_llwUmlgl54Ue0ycLnqBBj3nSYA6CjDxIWvSZ9XSDqYyZEVImqj4p6Hb99IsirnhckG39hE_7Bk2zna52oWxXvNR1skj2MD6yXkONb0HNXLf6KSRf-zJs='


if __name__ == '__main__':

    @events.register(events.NewMessage(outgoing=True))
    async def handler(event):
        # client = event.client
        sender = await event.get_sender()
        name = utils.get_display_name(sender)
        print(name, 'said', event.text, '!')

    with TelegramClient(StringSession(auth_key), api_id, api_hash) as client:
        client.add_event_handler(handler)
        client.run_until_disconnected()
