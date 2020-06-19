from fastapi import HTTPException

from telethon.sync import TelegramClient
from telethon.tl.types import ChatAdminRights
from telethon.errors import (
    ChatTitleEmptyError,
    UserRestrictedError,
    AdminsTooMuchError,
    AdminRankEmojiNotAllowedError,
    AdminRankInvalidError,
    BotChannelsNaError,
    ChannelInvalidError,
    ChatAdminInviteRequiredError,
    ChatAdminRequiredError,
    FreshChangeAdminsForbiddenError,
    RightForbiddenError,
    UserCreatorError,
    UserIdInvalidError,
    UserNotMutualContactError,
    UserPrivacyRestrictedError
)
from telethon.tl.functions.channels import (
    EditAdminRequest,
    CreateChannelRequest
)
from telethon.sessions import StringSession
from telethon import types

from ...core.config import api_id, api_hash

from .entitiy import get_list_entity


async def createChannel(auth_key, dbchannel):
    client = TelegramClient(StringSession(auth_key), api_id, api_hash)

    try:
        await client.connect()
    except OSError:
        raise HTTPException(status_code=400, detail="Failed to connect")

    try:
        result = await client(CreateChannelRequest(
            title=dbchannel.channel_name,
            about=dbchannel.about,
            megagroup=dbchannel.megagroup,
            geo_point=types.InputGeoPoint(
                lat=dbchannel.lat,
                long=dbchannel.long
            ),
            address=dbchannel.address,

        ))
    except ChatTitleEmptyError:
        raise HTTPException(
            status_code=400,
            detail="No chat title provided")
    except UserRestrictedError:
        raise HTTPException(
            status_code=400,
            detail="You're spamreported, you can't create channels or chats")  # noqa: E501
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="someting went wrong")
    return result.updates[1].channel_id


async def channelRights(auth_key, dbright):
    client = TelegramClient(StringSession(auth_key), api_id, api_hash)

    try:
        await client.connect()
    except OSError:
        raise HTTPException(status_code=400, detail="Failed to connect")

    entitys = await get_list_entity([dbright.channel, dbright.user], client)

    try:
        rights = ChatAdminRights(
            post_messages=dbright.post_messages,
            add_admins=dbright.add_admins,
            invite_users=dbright.invite_users,
            change_info=dbright.change_info,
            ban_users=dbright.ban_users,
            delete_messages=dbright.delete_messages,
            pin_messages=dbright.pin_messages,
            edit_messages=dbright.edit_messages,
        )

        await client(EditAdminRequest(
            entitys[0],
            entitys[1],
            rights,
            rank="member"
            ))
    except AdminsTooMuchError:
        raise HTTPException(
            status_code=400,
            detail="Too many admins")

    except AdminRankEmojiNotAllowedError:
        raise HTTPException(
            status_code=400,
            detail="Emoji are not allowed in admin titles or ranks")

    except AdminRankInvalidError:
        raise HTTPException(
            status_code=400,
            detail="The given admin title or rank was invalid\
                (possibly larger than 16 characters)")

    except BotChannelsNaError:
        raise HTTPException(
            status_code=400,
            detail="Bots can't edit admin privileges")

    except ChannelInvalidError:
        raise HTTPException(
            status_code=400,
            detail="Invalid channel object. Make sure to pass the right types,\
                for instance making sure that the request is designed for \
                channels or otherwise look for a different one more suited")  # noqa: E501

    except ChatAdminInviteRequiredError:
        raise HTTPException(
            status_code=400,
            detail="You do not have the rights to do this")

    except ChatAdminInviteRequiredError:
        raise HTTPException(
            status_code=400,
            detail="You do not have the rights to do this")

    except ChatAdminRequiredError:
        raise HTTPException(
            status_code=400,
            detail="Chat admin privileges are required to do that in the specified chat\
                (for example, to send a message in a channel which is not yours),\
                or invalid permissions used for the channel or group.")  # noqa: E501

    except FreshChangeAdminsForbiddenError:
        raise HTTPException(
            status_code=400,
            detail="Recently logged-in users cannot add or change admins")

    except RightForbiddenError:
        raise HTTPException(
            status_code=400,
            detail="Either your admin rights do not allow you to do this \
                or you passed the wrong rights combination\
                (some rights only apply to channels and vice versa)")

    except UserCreatorError:
        raise HTTPException(
            status_code=400,
            detail="You can't leave this channel, because you're its creator.")  # noqa: E501

    except UserIdInvalidError:
        raise HTTPException(
            status_code=400,
            detail="Invalid object ID for a user. Make sure to pass the right types,\
                for instance making sure that the request is designed for users \
                or otherwise look for a different one more suited.")  # noqa: E501

    except UserNotMutualContactError:
        raise HTTPException(
            status_code=400,
            detail="The provided user is not a mutual contact")

    except UserPrivacyRestrictedError:
        raise HTTPException(
            status_code=400,
            detail="The user's privacy settings do not allow you to do this")  # noqa: E501

    except Exception:
        raise HTTPException(
            status_code=400,
            detail="something went wrong")

# 1474787884, 1266629372
