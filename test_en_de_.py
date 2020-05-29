from utils.create_chuck import chuckSize
import hashlib
import uuid
import os
from utils.get_env import SERVER_TOKEN, SALT, KEY_MASTER


from security.security import decrypt_file, get_decrypt_key


decrypt_key = get_decrypt_key('123', '467551940')
name = '0bb0aad55413485eb81ccb8c64c2114e'
n = 1

while n <= 2:
    with open(f'Z_key/{name}_{n}.txt', 'rb') as f:
        token = f.read()
    data = decrypt_file(token, decrypt_key)

    with open(f'Z_key/read.md', 'ab') as f:
        f.write(data)
    n += 1
