from telethon.tl.types import DocumentAttributeFilename

from security.security import generate_key, create_share_key, created_key, encrypt_file

from utils.get_env import SERVER_TOKEN, SALT, KEY_MASTER
from utils.create_chuck import chuckSize
from utils._file import _filename


async def uploadFilEncrypt(client, password, filename):
    me = await client.get_me()
    dir = f"Chat/{me.id}/key/private_key.txt"

    try:
        share_key = create_share_key(
            dir, password, SERVER_TOKEN.encode(), KEY_MASTER, SALT.encode())
    except ValueError:
        return "wrong password"

    encrypt_key = created_key(share_key, SALT.encode())

    n = 0
    chunksize = chuckSize(filename)

    try:
        with open(filename, 'rb') as f:
            while True:
                data = f.read(chunksize)
                encrypt = encrypt_file(data, encrypt_key)
                n += 1
                if not data:
                    break
                name = _filename(filename, n)
                await client.send_file(
                    "me",
                    file=encrypt,
                    attributes=[DocumentAttributeFilename(
                        file_name=name)]
                )

        return {'message': 'upload success'}
    except:
        return {'message': 'upload not success'}
