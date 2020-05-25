import hashlib
import os
from utils.get_env import SERVER_TOKEN, SALT, KEY_MASTER

from security.security import create_share_key, created_key, encrypt_file, decrypt_file


dir = f"Chat/467551940/key/private_key.txt"

share_key = create_share_key(
    dir, "awds", SERVER_TOKEN.encode(), KEY_MASTER, SALT.encode())
encrypt_key = created_key(share_key, SALT.encode())

file = decrypt_file()
