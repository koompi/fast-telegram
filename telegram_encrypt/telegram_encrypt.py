import os

from telethon import TelegramClient
from telethon.sessions import StringSession

from utils.get_env import api_hash, api_id
from utils.get_env import api_hash, api_id
from utils._file import create_new_dir

from security.generate_key import generate_key


from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization

from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


async def get_key(auth_key, password):
    try:
        client = TelegramClient(StringSession(auth_key), api_id, api_hash)
        await client.connect()
    except:
        return "client error"

    me = await client.get_me()

    diretory = generate_key(password, me.id)

    for file in diretory:
        await client.send_file("me", file=file)

    return True


async def load_private_key(file, password):
    with open(file, "rb") as key_file:
        loaded_private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=password,
            backend=default_backend()
        )
    return load_private_key


def load_pubic_key(file):
    with open(file, "rb") as key_file:
        loaded_public_key = serialization.load_pem_public_key(
            key_file.read(),
            backend=default_backend()
        )
    return load_pubic_key


def create_share_key(server_private_key, peer_public_key):
    shared_key = server_private_key.exchange(
        ec.ECDH(), peer_public_key())
    return shared_key


def create_derived_key(shared_key, salt):
    derived_key = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=64,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    ).derive(shared_key)
