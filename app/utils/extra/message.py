import os
import mimetypes
from typing import List
from fastapi import HTTPException
from ..extra.is_exit import is_not_exit
from ...core.config import (
    sticker_dir, image_type, image_dir,
    gif_dir, git_type,
    voice_dir, voice_type,
    audio_dir, audio_type,
    video_dir, video_type,
    file_dir
)
from ...models.message import (
    Contact,
    Geo,
    Venue,
    Invoice,
    Message,
    Poll, PollAnswer, PollAnswerVoters,
    Game,
    WebPage,
    Document,
    DocumentAudio,
    DocumentVideo,
    DocumentVoice,
    Sticker,
    Gif,
    Photo
)


async def get_message_text(message, client):
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
        s3 = ''
        if s1 in s2:
            s3 = s2.replace(s1, '')
        text = WebPage(
            url=message.web_preview.url,
            site_name=message.web_preview.site_name,
            title=message.web_preview.title,
            description=message.web_preview.description,
            caption=s3
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
    elif message.sticker:
        id = message.sticker.id
        sticker = f"{sticker_dir}{id}.{image_type}"
        if is_not_exit(sticker_dir, sticker, image_type):
            with open(sticker, 'wb') as fd:
                async for chunk in client.iter_download(message.sticker):
                    fd.write(chunk)
        text = Sticker(
            sticker=os.path.abspath(sticker),
            caption=message.message
        )

    elif message.gif:
        id = message.gif.id
        gif = f"{gif_dir}{id}.{git_type}"
        if is_not_exit(gif_dir, gif, git_type):
            with open(gif, 'wb') as fd:
                async for chunk in client.iter_download(message.gif):
                    fd.write(chunk)
        text = Gif(
            gif=os.path.abspath(gif),
            caption=message.message
        )

    elif message.voice:
        id = message.voice.id
        voice = f"{voice_dir}{id}.{voice_type}"
        if is_not_exit(voice_dir, voice, voice_type):
            with open(voice, 'wb') as fd:
                async for chunk in client.iter_download(message.voice):
                    fd.write(chunk)
        text = DocumentVoice(
            voice=os.path.abspath(voice),
            caption=message.message,
            duration=message.voice.attributes[0].duration
        )

    elif message.audio:
        id = message.audio.id
        audio = f"{audio_dir}{id}.{audio_type}"
        file = os.path.abspath(audio)
        if is_not_exit(audio_dir, audio, audio_type):
            file = "audio"
        try:
            filename = message.audio.attributes[1].file_name
        except Exception:
            filename = ""
        text = DocumentAudio(
            audio=file,
            filename=filename,
            caption=message.message,
            duration=message.audio.attributes[0].duration
        )

    elif message.video:
        text = None
        id = message.video.id
        video = f"{video_dir}{id}.{video_type}"
        file = os.path.abspath(video)
        if is_not_exit(video_dir, video, video_type):
            file = "video"
        try:
            filename = message.video.attributes[1].file_name
        except Exception:
            filename = ""
        text = DocumentVideo(
            video=file,
            filename=filename,
            caption=message.message,
            duration=message.video.attributes[0].duration
        )

    elif message.photo:
        text = ""
        id = message.photo.id
        photo = f"{image_dir}{id}.{image_type}"
        if is_not_exit(image_dir, photo, image_type):
            with open(photo, 'wb') as fd:
                async for chunk in client.iter_download(message.photo):
                    fd.write(chunk)
        text = Photo(
            photo=os.path.abspath(photo),
            caption=message.message
        )

    elif message.document:
        id = message.document.id
        types = mimetypes.guess_extension(message.document.mime_type)
        file = f"{file_dir}{id}.{types}"
        _file = os.path.abspath(file)
        if is_not_exit(file_dir, file, types):
            _file = "document"
        try:
            filename = message.document.attributes[0].file_name
        except Exception:
            filename = ""
        text = Document(
            file=_file,
            filename=filename,
            caption=message.message,
        )

    elif message.raw_text:
        text = Message(
            text=message.raw_text
        )
    else:
        text = Message(
            text=""
        )
    # except Exception:
    #     raise HTTPException(status_code=400, detail="Get message Error")
    return text


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
        try:
            alt = (dialog.sticker.attributes)[1].alt
            message = f"{alt} sticker"
        except AttributeError:
            message = "sticker"

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

    elif dialog.raw_text:
        message = dialog.raw_text
    else:
        message = "unsupport message"

    return message
