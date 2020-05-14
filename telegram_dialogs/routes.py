from typing import List
from datetime import datetime, date

from fastapi import APIRouter, Depends, HTTPException

from database.mongodb import db
from utils.get_telegram import _get_telegram_or_404

from .telegram_dialogs import get_all_dialogs, get_all_messages, \
    send_message, upload_file, edit_message

telegramDialogs_router = APIRouter()


@telegramDialogs_router.get("/get_all_dialogs")
async def getDialogs(id: str, limit: int = 10):
    auth = await _get_telegram_or_404(id)
    dialogs = await get_all_dialogs(auth['auth_key'], limit)
    return {'data': dialogs}


@telegramDialogs_router.get("/get_all_messages")
async def getMessages(
    id: str,
    chat_id: int,
    limit: int = 10,
    search: str = None,
    reverse: bool = False,
    offset_date: date = None,
    ids: int = None,
    from_user: int = None,
):
    auth = await _get_telegram_or_404(id)
    messages = await get_all_messages(
        auth['auth_key'],
        chat_id,
        limit,
        search,
        reverse,
        offset_date,
        ids,
        from_user
    )

    return {'data': messages}


@telegramDialogs_router.get("/send_messages")
async def sendMessages(
    chat_id: int,
    id: str,
    message: str,
    reply_to: int = None,
    parse_mode: str = None,
    link_preview: bool = True,
    clear_draft: bool = False,
    silent: bool = False,
    schedule: datetime = None,
):
    auth = await _get_telegram_or_404(id)

    messages = await send_message(
        auth['auth_key'],
        chat_id,
        message,
        reply_to,
        parse_mode,
        link_preview,
        clear_draft,
        silent,
        schedule,
    )

    return {'data': messages}


@telegramDialogs_router.post("/upload_file")
async def uploadFile(
    chat_id: int,
    id: str,
    file: List[str],
    caption: str = None,
    force_document: bool = False,
    clear_draft: bool = False,
    reply_to: int = None,
    thumb: str = None,
    voice_note: bool = False,
    video_note: bool = False,
    silent: bool = False,
    supports_streaming: bool = False,
    schedule: datetime = None,

):
    auth = await _get_telegram_or_404(id)

    file = await upload_file(
        auth['auth_key'],
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
        schedule
    )
    if file:
        return {'data': 'upload success'}

    return {'data': 'upload fail'}


@telegramDialogs_router.patch("/edit_message")
async def editMessage(
    chat_id: int,
    id: str,
    message_id: int,
    new_message: str,
    parse_mode: str = None,
    link_preview: bool = True,
    force_document: bool = False,
    schedule: datetime = None,
):
    auth = await _get_telegram_or_404(id)

    message = await edit_message(
        auth['auth_key'],
        chat_id,
        message_id=message_id,
        text=new_message,
        parse_mode=parse_mode,
        link_preview=link_preview,
        force_document=force_document,
        schedule=schedule
    )

    return {'new message': new_message}
