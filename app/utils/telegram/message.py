from fastapi import HTTPException
from typing import List
from telethon import TelegramClient
from telethon.sessions import StringSession

from ...core.config import api_id, api_hash
from .entitiy import get_entity
from ...models.message import (
    Contact,
    Geo,
    Venue,
    Invoice,
    Message,
    Poll, PollAnswer, PollAnswerVoters,
    Game,
    WebPage
)


async def get_all_messages(auth_key, msg):
    client = TelegramClient(StringSession(auth_key), api_id, api_hash)
    try:
        await client.connect()
    except OSError:
        raise HTTPException(status_code=400, detail="Failed to connect")

    entity = await get_entity(msg.entity, msg.access_hash, client)
    res = []
    replys = []
    inline_replys = []
    async for message in client.iter_messages(
        entity=entity,
        limit=msg.limit,
        offset_date=msg.offset_date,
        min_id=msg.min_id,
        max_id=msg.max_id,
        reverse=msg.reverse,
        search=msg.search,
        from_user=msg.from_user,
        ids=msg.ids
    ):
        if message.text is not None:
            try:
                user = await client.get_entity(message.from_id)
                from_user = f"{user.first_name} {user.last_name}"
            except TypeError:
                from_user = ""

            if message.is_reply:
                text = await get_message_text(message)
                msg_reply = await client.get_messages(
                    entity, ids=message.reply_to_msg_id
                )
                replys.append((msg_reply.id, from_user, text))
                text = ""
            else:
                text = await get_message_text(message)
            for reply in replys:
                if reply[0] == message.id:
                    inline = {
                        "from_user": reply[1],
                        "message": reply[2]
                    }
                    inline_replys.append(inline)
                    text = await get_message_text(message)
            if inline_replys or text != "":
                res_msg = {
                    "message_id": message.id,
                    "from_user": from_user,
                    "message": text,
                    "inline_replys": inline_replys
                }
                inline_replys = []
                res.append(res_msg)
            # s1 = message.web_preview.url
            # s2 = message.text
            # if s1 in s2:
            #     s3 = s2.replace(s1, '')
            print(message.web_preview)
    return res


async def get_message_text(message):
    # try:
    if message.contact:
        text = Contact(
            phone_number=message.contact.phone_number,
            first_name=message.contact.first_name,
            last_name=message.contact.last_name,
            vcard=message.contact.vcard,
            user_id=message.contact.user_id
        )
    elif message.venue:
        text = Venue(
            long=message.venue.geo.long,
            lat=message.venue.geo.lat,
            access_hash=message.venue.geo.access_hash,
            title=message.venue.title,
            address=message.venue.address,
            provider=message.venue.provider,
            venue_id=message.venue.venue_id,
            venue_type=message.venue.venue_type
        )
    elif message.geo:
        text = Geo(
            long=message.geo.long,
            lat=message.geo.lat,
            access_hash=message.geo.access_hash
        )
    elif message.poll:
        poll = message.poll
        answers: List[PollAnswer] = []
        for answer in poll.poll.answers:
            answers.append(
                PollAnswer(
                    text=answer.text,
                    option=answer.option
                )
            )
        results: List[PollAnswerVoters] = []
        for result in poll.results.results:
            results.append(
                PollAnswerVoters(
                    option=result.option,
                    voters=result.voters,
                    chosen=result.chosen,
                    correct=result.correct
                )
            )
        text = Poll(
            id=poll.poll.id,
            question=poll.poll.question,
            answers=answers,
            closed=poll.poll.closed,
            public_voters=poll.poll.public_voters,
            multiple_choice=poll.poll.multiple_choice,
            quiz=poll.poll.quiz,
            close_period=poll.poll.close_period,
            close_date=poll.poll.close_date,
            min=poll.results.min,
            results=results,
            total_voters=poll.results.total_voters,
            recent_voters=poll.results.recent_voters,
            solution=poll.results.solution,
        )
    elif message.game:
        text = Game(
            id=message.game.id,
            access_hash=message.game.access_hash,
            short_name=message.game.short_name,
            title=message.game.title,
            descriptio=message.game.description
        )
    elif message.web_preview:
        s1 = message.web_preview.url
        s2 = message.text
        if s1 in s2:
            s3 = s2.replace(s1, '')
        text = WebPage(
            url=message.web_preview.url,
            site_name=message.web_preview.site_name,
            title=message.web_preview.title,
            description=message.web_preview.description,
            caption=s3[1:]
        )
    elif message.invoice:
        invoice = message.invoice
        text = Invoice(
            title=invoice.title,
            description=invoice.description,
            currency=invoice.currency,
            total_amount=invoice.total_amount,
            start_param=invoice.start_param,
            shipping_address_requested=invoice.shipping_address_requested,
            test=invoice.test,
            receipt_msg_id=invoice.receipt_msg_id
        )
    elif message.raw_text:
        text = Message(
            text=message.raw_text
        )
    else:
        text = "unsupport message"
    # except Exception:
    #     raise HTTPException(status_code=400, detail="Get message Error")
    return text


def get_file(message):
    if message.invoice:
        file = "invoice type (unsupport)"
    
    elif message.web_preview:
        file = message.message
    elif message.sticker:
        file = "sticker"
    elif message.gif:
        file = "GIF"
    elif message.photo:
        file = "photo"
    elif message.video_note or message.video:
        file = "video"
    elif message.voice:
        file = "voice message"
    elif message.audio:
        file = "audio"

    return file
