from fastapi import HTTPException

from telethon.sync import TelegramClient
from telethon.tl.types import ChatAdminRights
from telethon.errors import (
    AdminsTooMuchError,
    AdminRankInvalidError,
    AdminRankEmojiNotAllowedError,
    BotChannelsNaError,
    ChannelInvalidError,
    ChannelsAdminPublicTooMuchError,
    ChatTitleEmptyError,
    ChatAdminRequiredError,
    ChatAdminInviteRequiredError,
    FreshChangeAdminsForbiddenError,
    RightForbiddenError,
    UserCreatorError,
    UserIdInvalidError,
    UserRestrictedError,
    UserNotMutualContactError,
    UserPrivacyRestrictedError,
    UsernameInvalidError,
    UsernameOccupiedError
)
from telethon.tl.functions.channels import (
    EditAdminRequest,
    CreateChannelRequest,
    CheckUsernameRequest,
    UpdateUsernameRequest
)
from telethon.sessions import StringSession
from telethon import types

from ...core.config import api_id, api_hash

from .entitiy import get_list_entity, get_entity


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


async def channelRights(auth_key, db):
    client = TelegramClient(StringSession(auth_key), api_id, api_hash)

    try:
        await client.connect()
    except OSError:
        raise HTTPException(status_code=400, detail="Failed to connect")

    entitys = await get_list_entity([db.channel, db.user], client)

    try:
        rights = ChatAdminRights(
            post_messages=db.post_messages,
            add_admins=db.add_admins,
            invite_users=db.invite_users,
            change_info=db.change_info,
            ban_users=db.ban_users,
            delete_messages=db.delete_messages,
            pin_messages=db.pin_messages,
            edit_messages=db.edit_messages,
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


async def changeChannelType(auth_key, type):
    client = TelegramClient(StringSession(auth_key), api_id, api_hash)
    try:
        await client.connect()
    except OSError:
        raise HTTPException(status_code=400, detail="Failed to connect")
    channel = await get_entity(type.channel_id, client)

    try:
        checkResult = await client(CheckUsernameRequest(
            channel,
            username=type.channel_name
        ))
        if checkResult:
            await client(UpdateUsernameRequest(
                channel,
                username=type.channel_name
            ))

        else:
            raise HTTPException(
                status_code=400,
                detail="Your name is error or already use"
            )

    except ChannelsAdminPublicTooMuchError:
        raise HTTPException(
            status_code=400,
            detail="You're admin of too many public channels,\
                make some channels private to change the username of this channel.")  # noqa: E501

    except UserIdInvalidError:
        raise HTTPException(
            status_code=400,
            detail="Invalid object ID for a user. Make sure to pass the right types,\
                for instance making sure that the request is designed for users \
                or otherwise look for a different one more suited.")  # noqa: E501

    except ChatAdminRequiredError:
        raise HTTPException(
            status_code=400,
            detail="Chat admin privileges are required to do that in the specified chat\
                (for example, to send a message in a channel which is not yours),\
                or invalid permissions used for the channel or group.")  # noqa: E501

    except UsernameInvalidError:
        raise HTTPException(
            status_code=400,
            detail='Nobody is using this username, or the username is unacceptable')  # noqa: E501

    except UsernameOccupiedError:
        raise HTTPException(
            status_code=400,
            detail='The username is already taken.')
