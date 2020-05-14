import os

from telethon.tl.custom.file import File

from utils._file import create_filename, create_new_dir, exit_files


async def download_file(media, chat_id, client, specific_dir=None):
    files = File(media)

    dirName = f'./Chat/{chat_id}'

    dirName = create_new_dir(dirName, specific_dir)

    filename = create_filename(
        dirName,
        files.media.media.access_hash,
        files.media.mime_type
    )

    if exit_files(dirName, filename, files.media.mime_type):
        with open(filename, 'wb') as fd:
            async for chunk in client.iter_download(files.media.media):
                fd.write(chunk)
    return filename


async def download_profile_photo(entity, client, chat_id, chat_name):
    dirname = f"Chat/{chat_id}"
    create_new_dir(dirname, "profile")

    filename = f"{dirname}/profile/{chat_name}"
    try:
        os.remove(f"{filename}.jpg")
    except IOError:
        pass
    file = await client.download_profile_photo(entity, file=filename, download_big=False)
    if file is None:
        filename = None

    return filename
