from telethon.tl.types import PeerUser, PeerChat, PeerChannel
from telethon.errors.rpcerrorlist import PeerIdInvalidError
from telethon import TelegramClient

from fastapi import HTTPException


async def get_entity(
    peer_id: int,
    client: TelegramClient
):
    try:
        try:
            entity = await client.get_entity(PeerUser(peer_id))
        except Exception:
            try:
                entity = await client.get_entity(PeerChannel(peer_id))
            except Exception:
                entity = await client.get_entity(PeerChat(peer_id))
    except PeerIdInvalidError:
        raise HTTPException(
                status_code=400,
                detail="Invalid Peer Id")

    return entity
