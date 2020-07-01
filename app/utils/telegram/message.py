from fastapi import HTTPException

from telethon import TelegramClient
from telethon.sessions import StringSession

from ...core.config import api_id, api_hash
from .entitiy import get_entity


async def get_all_messages(auth_key, msg):
    client = TelegramClient(StringSession(auth_key), api_id, api_hash)
    try:
        await client.connect()
    except OSError:
        raise HTTPException(status_code=400, detail="Failed to connect")

    entity = await get_entity(msg.entity, client)
    res = []
    replys = []
    inline_replys = []
    async for message in client.iter_messages(
        entity=entity,
        limit=msg.limit,
        offset_date=msg.offset_date,
        min_id=msg.min_id,
        max_id=msg.max_id,
        reverse=msg.reverse,
        search=msg.search,
        from_user=msg.from_user,
        ids=msg.ids
    ):
        if message.text is not None:
            try:
                user = await client.get_entity(message.from_id)
                if user.first_name is None:
                    user.first_name = ""
                elif user.last_name is None:
                    user.last_name = ""
                from_user = f"{user.first_name} {user.last_name}"
            except TypeError:
                from_user = ""

            if message.is_reply:
                text = await get_message_text(message)
                msg_reply = await client.get_messages(
                    entity, ids=message.reply_to_msg_id
                )
                replys.append((msg_reply.id, from_user, text))
                text = ""
            else:
                text = await get_message_text(message)

            for reply in replys:
                if reply[0] == message.id:
                    inline = {
                        "from_user": reply[1],
                        "message": reply[2]
                    }
                    inline_replys.append(inline)
                    text = await get_message_text(message)
            if inline_replys or text != "":
                res_msg = {
                    "message_id": message.id,
                    "from_user": from_user,
                    "message": text,
                    "inline_replys": inline_replys
                }
                inline_replys = []
                res.append(res_msg)
    return res


async def get_message_text(message):
    try:
        if message.geo:
            text = "geo type (unsupport)"
        elif message.venue:
            text = "venue type (unsupport)"
        elif message.invoice:
            text = "invoice type (unsupport)"
        elif message.poll:
            text = "poll type (unsupport)"
        elif message.game:
            text = "game type (unsupport)"
        elif message.web_preview:
            text = message.message
        elif message.contact:
            phone_number = message.contact.phone_number
            first_name = message.contact.first_name
            last_name = message.contact.last_name
            vcard = message.contact.vcard
            user_id = message.contact.user_id

            text = {
                "message_id": user_id,
                "phone_number": phone_number,
                "name": f"{first_name} {last_name}",
                "vcard":  vcard
                }
        elif message.sticker:
            text = "sticker"
        elif message.gif:
            text = "GIF"
        elif message.photo:
            text = "photo"
        elif message.video_note or message.video:
            text = "video"
        elif message.voice:
            text = "voice message"
        elif message.audio:
            text = "audio"
        elif message.text or message.raw_text:
            text = message.text
    except Exception:
        raise HTTPException(status_code=400, detail="Get message Error")

    return text
