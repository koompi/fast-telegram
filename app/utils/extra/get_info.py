from ...models.dialog import (
    UserBase,
    ChannelBase,
    ChatBase,
)


def get_info(dialog, client=None):
    if dialog.is_user:
        entity = UserBase(
            peer_id=dialog.entity.id,
            access_hash=dialog.entity.access_hash,
            first_name=dialog.entity.first_name,
            last_name=dialog.entity.last_name,
            username=dialog.entity.username,
            scam=dialog.entity.scam
        )

    elif dialog.is_channel:
        entity = ChannelBase(
            peer_id=dialog.entity.id,
            access_hash=dialog.entity.access_hash,
            username=dialog.entity.username,
            title=dialog.entity.title,
            participants_count=dialog.entity.participants_count,
            scam=dialog.entity.scam
        )
    elif dialog.is_group:
        entity = ChatBase(
            peer_id=dialog.entity.id,
            title=dialog.entity.title,
            participants_count=dialog.entity.participants_count
        )
    else:
        entity = None

    return entity
