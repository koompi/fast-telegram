from fastapi import HTTPException
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.utils import get_display_name

from .entitiy import get_entity
from ..extra.message import get_message_text
from ...core.config import api_id, api_hash
from ...models.message import MessageInResponse, InlineMessage

from ..extra.is_exit import is_not_exit
from ...core.config import (
    audio_dir, audio_type,
    video_dir, video_type
)


async def get_all_messages(auth_key, msg, filter):
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
        filter=filter,
        offset_date=msg.offset_date,
        min_id=msg.min_id,
        max_id=msg.max_id,
        reverse=msg.reverse,
        search=msg.search,
        from_user=msg.from_user,
        ids=msg.ids
    ):
        if message.text is not None:
            from_user = get_display_name(message.sender)
            if message.is_reply:
                text = await get_message_text(message, client)
                msg_reply = await client.get_messages(
                    entity, ids=message.reply_to_msg_id
                )
                replys.append((
                    msg_reply.id,
                    from_user,
                    text,
                    message.id,
                    message.date
                    ))
                text = ""
            else:
                text = await get_message_text(message, client)
            for reply in replys:
                if reply[0] == message.id:
                    inline = InlineMessage(
                        id=reply[3],
                        from_user=reply[1],
                        message=reply[2],
                        date=reply[4]
                    )
                    inline_replys.append(inline)
                    text = await get_message_text(message, client)
            if inline_replys or text != "":
                res_msg = MessageInResponse(
                    id=message.id,
                    from_user=from_user,
                    message=text,
                    date=message.date,
                    reply=inline_replys
                )
                inline_replys = []
                res.append(res_msg)
    return res


async def get_file(auth_key, file):
    client = TelegramClient(StringSession(auth_key), api_id, api_hash)
    try:
        await client.connect()
    except OSError:
        raise HTTPException(status_code=400, detail="Failed to connect")

    entity = await get_entity(file.entity, file.access_hash, client)

    async for message in client.iter_messages(
        entity=entity,
        ids=file.ids
    ):
        if message.video:
            id = message.message.video
            video = f"{video_dir}{id}.{video_type}"
            if is_not_exit(video_dir, video, video_type):
                with open(video, 'wb') as fd:
                    async for chunk in client.iter_download(message.video):
                        fd.write(chunk)
                return 'download success'
        elif message.audio:
            id = message.audio.id
            audio = f"{audio_dir}{id}.{audio_type}"
            if is_not_exit(audio_dir, audio, audio_type):
                with open(audio, 'wb') as fd:
                    async for chunk in client.iter_download(message.audio):
                        fd.write(chunk)
                return 'download success'
        else:
            return 'can not download'

        return 'file already exit'


async def edit_message(auth_key, msg):
    client = TelegramClient(StringSession(auth_key), api_id, api_hash)
    try:
        await client.connect()
    except OSError:
        raise HTTPException(status_code=400, detail="Failed to connect")

    entity = await get_entity(msg.entity, msg.access_hash, client)
    try:
        await client.edit_message(
            entity=entity,
            message=msg.message,
            text=msg.text,
            link_preview=msg.link_preview,
            file=msg.file,
            force_document=msg.force_document
            )
    except Exception:
        raise HTTPException(status_code=400, detail="something went wrong")


async def delete_message(auth_key, msg):
    client = TelegramClient(StringSession(auth_key), api_id, api_hash)
    try:
        await client.connect()
    except OSError:
        raise HTTPException(status_code=400, detail="Failed to connect")

    entity = await get_entity(msg.entity, msg.access_hash, client)

    try:
        await client.delete_messages(
            entity=entity,
            message_ids=msg.message_ids,
            revoke=msg.revoke
            )
    except Exception:
        raise HTTPException(status_code=400, detail="something went wrong")
