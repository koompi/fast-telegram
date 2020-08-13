from telethon.tl.types import InputPeerUser,  InputPeerChannel,  InputPeerChat

from fastapi import HTTPException


async def get_entity(peer_id, access_hash, client):
    try:
        try:
            entity = await client.get_entity(InputPeerUser(
                peer_id,
                access_hash=access_hash)
            )
        except Exception:
            try:
                entity = await client.get_entity(InputPeerChannel(
                    peer_id,
                    access_hash=access_hash)
                )
            except Exception:
                entity = await client.get_entity(InputPeerChat(
                    peer_id)
                )
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid Peer Id")
    return entity
