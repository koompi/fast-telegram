from telethon.tl.types import (
    # InputMessagesFilterEmpty,
    InputMessagesFilterPhotos,
    InputMessagesFilterContacts,
    InputMessagesFilterDocument,
    InputMessagesFilterGeo,
    InputMessagesFilterGif,
    InputMessagesFilterMusic,
    InputMessagesFilterMyMentions,
    InputMessagesFilterPhotoVideo,
    InputMessagesFilterVideo,
    InputMessagesFilterUrl,
    InputMessagesFilterVoice
)


def get_filters(filters):
    if filters is None:
        # _filter = InputMessagesFilterEmpty
        _filter = None
    elif filters == 'photo':
        _filter = InputMessagesFilterPhotos
    elif filters == 'contact':
        _filter = InputMessagesFilterContacts
    elif filters == 'document':
        _filter = InputMessagesFilterDocument
    elif filters == 'geo':
        _filter = InputMessagesFilterGeo
    elif filters == 'gif':
        _filter = InputMessagesFilterGif
    elif filters == 'music':
        _filter = InputMessagesFilterMusic
    elif filters == 'my_mentions':
        _filter = InputMessagesFilterMyMentions
    elif filters == 'photo_video':
        _filter = InputMessagesFilterPhotoVideo
    elif filters == 'video':
        _filter = InputMessagesFilterVideo
    elif filters == 'url':
        _filter = InputMessagesFilterUrl
    elif filters == 'voice':
        _filter = InputMessagesFilterVoice
    else:
        _filter = None
    return _filter
