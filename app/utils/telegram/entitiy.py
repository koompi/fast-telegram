from typing import List
# from telethon.tl.types import PeerUser, PeerChat, PeerChannel
from telethon.tl.types import InputPeerUser,  InputPeerChannel,  InputPeerChat
from telethon.errors.rpcerrorlist import PeerIdInvalidError
from telethon import TelegramClient

from fastapi import HTTPException


async def get_entity(
    peer_id,
    access_hash,
    client
):

    try:
        try:
            entity = await client.get_entity(InputPeerUser(
                int(peer_id),
                access_hash=access_hash)
            )
        except Exception:
            try:
                entity = await client.get_entity(InputPeerChannel(
                    int(peer_id),
                    access_hash=access_hash)
                )
            except Exception:
                entity = await client.get_entity(InputPeerChat(
                    int(peer_id),
                    access_hash=access_hash)
                )
    except Exception:
        try:
            entity = await client.get_entity(peer_id)
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid Peer Id")
    return entity


async def get_list_entity(
    peer_ids: List[str],
    client: TelegramClient,
    access_hash
):
    entitys = []
    for peer_id in peer_ids:
        try:
            try:
                entity = await client.get_entity(InputPeerUser(
                    int(peer_id),
                    access_hash=access_hash)
                )
            except Exception:
                entity = await client.get_entity(
                    InputPeerChannel(int(peer_id)))

        except Exception:
            try:
                entity = await client.get_entity(peer_id)
                entitys.append(entity)
            except PeerIdInvalidError:
                raise HTTPException(status_code=400, detail="Invalid Peer Id")
            except Exception:
                raise HTTPException(
                    status_code=400,
                    detail="something went wrong")
    return entitys
