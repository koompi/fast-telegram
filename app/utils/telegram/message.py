from fastapi import HTTPException
from telethon import TelegramClient
from telethon.sessions import StringSession

from .entitiy import get_entity
from ..extra.message import get_message_text
from ...core.config import api_id, api_hash


async def get_all_messages(auth_key, msg):
    client = TelegramClient(StringSession(auth_key), api_id, api_hash)
    try:
        await client.connect()
    except OSError:
        raise HTTPException(status_code=400, detail="Failed to connect")

    entity = await get_entity(msg.entity, msg.access_hash, client)
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
                from_user = f"{user.first_name} {user.last_name}"
            except TypeError:
                from_user = ""

            if message.is_reply:
                text = await get_message_text(message, client)
                msg_reply = await client.get_messages(
                    entity, ids=message.reply_to_msg_id
                )
                replys.append((msg_reply.id, from_user, text))
                text = ""
            else:
                text = await get_message_text(message, client)
            for reply in replys:
                if reply[0] == message.id:
                    inline = {
                        "from_user": reply[1],
                        "message": reply[2]
                    }
                    inline_replys.append(inline)
                    text = await get_message_text(message, client)
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


def get_file(message):
    if message.invoice:
        file = "invoice type (unsupport)"

    elif message.sticker:
        file = "sticker"
    elif message.gif:
        file = "GIF"
    elif message.photo:
        file = "photo"
    elif message.video_note or message.video:
        file = "video"
    elif message.voice:
        file = "voice message"
    elif message.audio:
        file = "audio"

    return file
