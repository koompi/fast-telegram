import os

from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.errors import \
    MessageAuthorRequiredError, MessageNotModifiedError, MessageIdInvalidError


from utils.get_env import api_hash, api_id
from utils.get_message import get_lastest_message, get_all_message_data
from utils.dowload_file import download_profile_photo
from utils.get_entity import get_entity
from utils._file import create_new_dir
from utils.create_thumnail import create_thumbnail


async def get_all_dialogs(
        auth_key,
        limit
):
    try:
        client = TelegramClient(StringSession(auth_key), api_id, api_hash)
        await client.connect()
    except:
        return "client error"

    data = []

    async for dialog in client.iter_dialogs(limit=limit):
        try:
            entity = await get_entity(dialog.entity.id, client)
        except:
            return "entity error"

        filename = await download_profile_photo(entity, client, dialog.entity.id, dialog.name)

        user = dialog.message

        try:
            message = await get_lastest_message(dialog.message, client, entity)
        except:
            message = "can not get message"

        user = {
            "id": str(dialog.entity.id),
            "name": dialog.name,
            "photo": filename,
            "message": message,
        }
        data.append(user)

    return data


async def get_all_messages(
    auth_key,
    chat_id,
    limit,
    search,
    reverse,
    offset_date,
    ids,
    from_user
):

    try:
        client = TelegramClient(StringSession(auth_key), api_id, api_hash)
        await client.connect()
    except:
        return "client error"
    try:
        entity = await get_entity(chat_id, client)
    except:
        return "entity error"

    messages = []

    async for message in client.iter_messages(
            entity,
            limit=limit,
            search=search,
            reverse=reverse,
            offset_date=offset_date,
            ids=ids,
            from_user=from_user
    ):
        user = await client.get_entity(message.from_id)
        data = await get_all_message_data(message, client, entity, chat_id, user.username)
        messages.append(data)

    return messages


async def send_message(
    auth_key,
    chat_id,
    message,
    reply_to,
    parse_mode,
    link_preview,
    clear_draft,
    silent,
    schedule,
):
    try:
        client = TelegramClient(StringSession(auth_key), api_id, api_hash)
        await client.connect()
    except:
        return "client error"

    try:
        entity = await get_entity(chat_id, client)
    except:
        return "entity error"

    await client.send_message(
        entity,
        message=message,
        reply_to=reply_to,
        parse_mode=parse_mode,
        link_preview=link_preview,
        clear_draft=clear_draft,
        silent=silent,
        schedule=schedule
    )

    return message


async def edit_message(
    auth_key,
    chat_id,
    message_id,
    text,
    parse_mode,
    link_preview,
    force_document,
    schedule,
):
    try:
        client = TelegramClient(StringSession(auth_key), api_id, api_hash)
        await client.connect()
    except:
        return "client error"

    try:
        entity = await get_entity(chat_id, client)
    except:
        return "entity error"
    try:
        await client.edit_message(
            entity,
            message=message_id,
            text=text,
            parse_mode=parse_mode,
            link_preview=link_preview,
            force_document=force_document,
            schedule=schedule
        )
        return text
    except MessageAuthorRequiredError:
        return "you not have authorize"
    except MessageNotModifiedError:
        return "contents of the message were not modified"
    except MessageIdInvalidError:
        return "ID of the message is invalid or messages with a reply markup can`t edit"


async def upload_file(
    auth_key,
    chat_id,
    file,
    caption,
    force_document,
    clear_draft,
    reply_to,
    thumb,
    voice_note,
    video_note,
    silent,
    supports_streaming,
    schedule,
):
    try:
        client = TelegramClient(StringSession(auth_key), api_id, api_hash)
        await client.connect()
    except:
        return "client error"

    try:
        entity = await get_entity(chat_id, client)
    except:
        return "entity error"

    if thumb:
        thumb = create_thumbnail(thumb, (200, 200))

    try:
        await client.send_file(
            entity,
            file=file,
            caption=caption,
            force_document=force_document,
            clear_draft=clear_draft,
            reply_to=reply_to,
            thumb=thumb,
            voice_note=voice_note,
            video_note=video_note,
            silent=silent,
            supports_streaming=supports_streaming,
            schedule=schedule,
        )
        return True
    except:
        return False
