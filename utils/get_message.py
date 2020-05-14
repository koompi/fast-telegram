
from utils.dowload_file import download_file


async def get_lastest_message(user, client, entity):
    if user.geo:
        message = str(user.geo)

    elif user.venue:
        message = str(user.venue)

    elif user.invoice:
        message = str(user.invoice)

    elif user.poll:
        message = user.poll.poll.question

    elif user.web_preview:
        message = user.message

    elif user.contact:
        message = "Contact"

    elif user.game:
        message = "game"

    elif user.sticker:
        alt = (user.sticker.attributes)[1].alt
        message = f"{alt} sticker"

    elif user.gif:
        message = "GIF"

    elif user.photo:
        message = "photo"

    elif user.video_note or user.video:
        message = "video"

    elif user.voice:
        message = "voice message"

    elif user.audio:
        message = "audio"

    elif user.is_reply:
        msg_reply = await client.get_messages(entity, ids=user.reply_to_msg_id)
        message = {"reply_msg_to": msg_reply.message, "msg": user.text}

    elif user.text or user.raw_text:
        message = user.text
    else:
        message = "unknow type message"

    return message


async def get_all_message_data(message, client, entity, chat_id, username):
    if message.geo:
        data = "geo type (unsupport)"

    elif message.venue:
        data = "venue type (unsupport)"

    elif message.invoice:
        data = "invoice type (unsupport)"

    elif message.poll:
        data = "poll type (unsupport)"

    elif message.game:
        data = "game type (unsupport)"

    elif message.web_preview:
        data = message.message

    elif message.contact:
        phone_number = message.contact.phone_number
        first_name = message.contact.first_name
        last_name = message.contact.last_name
        vcard = message.contact.vcard
        user_id = message.contact.user_id

        data = {
            "message_id": user_id,
            "phone_number": phone_number,
            "name": f"{first_name} {last_name}",
            "vcard":  vcard
        }
    elif message.sticker:
        filename = await download_file(message.file, chat_id, client, "sticker")
        data = {"sctiker": filename}

    elif message.gif:
        filename = await download_file(message.file, chat_id, client, "gif")
        data = {"git": filename}

    elif message.photo:
        filename = await download_file(message.file, chat_id, client, "photo")
        data = {"photo": filename}

    elif message.video_note or message.video:
        filename = await download_file(message.file, chat_id, client, "video")
        data = {"video": filename}

    elif message.voice:
        filename = await download_file(message.file, chat_id, client, "voice")
        data = {"voice": filename}

    elif message.audio:
        filename = await download_file(message.file, chat_id, client, "audio")
        data = {"audio": filename}

    elif message.is_reply:
        msg_reply = await client.get_messages(entity, ids=message.reply_to_msg_id)
        data = {"reply_msg_to": msg_reply.message, "msg": message.text}

    elif message.text:
        data = message.text

    else:
        data = "unknow type message"

    all_data = {
        'message_id': message.id,
        'from_user': username,
        'message': data,
        'date': message.date,
    }

    return all_data
