from ...models.dialog import (
    UserBase,
    ChannelBase,
    ChatBase,
)


def get_lastest_message(dialog):
    if dialog.geo:
        message = "Location"

    elif dialog.venue:
        message = f"Location, {dialog.venue.title}"

    elif dialog.invoice:
        message = "Invoice"

    elif dialog.poll:
        message = dialog.poll.poll.question

    elif dialog.web_preview:
        message = dialog.message

    elif dialog.contact:
        message = "Contact"

    elif dialog.game:
        message = "game"

    elif dialog.sticker:
        alt = (dialog.sticker.attributes)[1].alt
        message = f"{alt} sticker"

    elif dialog.gif:
        message = "GIF"

    elif dialog.photo:
        message = "photo"

    elif dialog.video_note or dialog.video:
        message = "video"

    elif dialog.voice:
        message = "voice message"

    elif dialog.audio:
        message = "audio"

    elif dialog.text or dialog.raw_text:
        message = dialog.text
    else:
        message = "unknow type message"

    return message


def get_info(dialog):
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
