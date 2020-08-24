from ...models.dialog import UserBase


def get_info(dialog, client=None):
    if dialog.is_user or dialog.is_channel:
        entity = UserBase(
            peer_id=dialog.entity.id,
            access_hash=dialog.entity.access_hash,
        )

    elif dialog.is_group:
        entity = UserBase(
            peer_id=dialog.entity.id,
            access_hash=0,
        )
    else:
        entity = None

    return entity
