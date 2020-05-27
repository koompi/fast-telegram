import hashlib
import os
from utils.get_env import SERVER_TOKEN, SALT, KEY_MASTER

from security.security import create_token, decrypt_token

# dir = f"Chat/467551940/key/public_key.txt"

# with open(dir, "rb") as f:
#     token = create_token(f.read(), KEY_MASTER, SALT.encode())

# data = decrypt_token(token, KEY_MASTER, SALT.encode())
# print(token.decode())


import os
import sys


def chuckSize(filename):
    bytes = os.stat(filename).st_size
    if (bytes < 650):
        bytes = 650

    size = bytes // 30

    return size + 1


print(chuckSize("vdo.mp4"))
