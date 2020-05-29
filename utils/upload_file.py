import uuid

from telethon.tl.types import DocumentAttributeFilename

from security.security import generate_key, create_share_key, created_key, encrypt_file, decrypt_file

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

    n = 1
    chunksize = chuckSize(filename)

    try:
        with open(filename, 'rb') as f:
            filename = uuid.uuid4().hex
            while True:
                data = f.read(chunksize)
                if not data:
                    break
                else:
                    encrypt = encrypt_file(data, encrypt_key)
                    await client.send_file(
                        "me",
                        file=encrypt,
                        attributes=[DocumentAttributeFilename(
                            file_name=_filename(filename, n))]
                    )

                n += 1

        return {'message': 'upload success'}
    except:
        return {'message': 'upload not success'}
