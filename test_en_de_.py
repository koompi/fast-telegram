import os
from utils.get_env import SERVER_TOKEN, SALT, KEY_MASTER

from security.security import create_share_key, created_key, encrypt_file


dir = f"Chat/467551940/key/private_key.txt"

share_key = create_share_key(
    dir, "awds", SERVER_TOKEN.encode(), KEY_MASTER, SALT.encode())
encrypt_key = created_key(share_key, SALT.encode())

filesize = os.stat('Z_key/vdo.mp4').st_size
chunksize = (filesize // 2) + 1
with open("requirements.txt", 'rb') as f:
    while True:
        data = f.read(chunksize)
        encrypt = encrypt_file(data, encrypt_key)
        print(encrypt)
        if not data:
            break  # done
