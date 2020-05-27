import base64
import os

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet

from utils._file import create_new_dir

from utils.get_env import SERVER_TOKEN, SALT, KEY_MASTER


def generate_key(password, id):
    private_key = ec.generate_private_key(
        ec.SECP384R1(), default_backend()
    )
    public_key = private_key.public_key()

    password = password.encode('UTF-8')

    serialized_private_key = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.BestAvailableEncryption(password)
    )

    serialized_public_key = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    diretory = create_new_dir(f'./Chat/{id}', 'key')
    private_key_dir = f'{diretory}/private_key.txt'
    public_key_dir = f'{diretory}/public_key.txt'

    with open(private_key_dir, 'wb') as f:
        f.write(serialized_private_key)

    with open(public_key_dir, 'wb') as f:
        f.write(serialized_public_key)

    data = [private_key_dir, public_key_dir]

    return data


def created_key(shared_key, salt):
    key = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    ).derive(shared_key)

    key = base64.urlsafe_b64encode(key)

    return key


def create_token(public_key, key, salt):
    password = key.encode()
    key = created_key(password, salt)
    token = encrypt_file(public_key, key)

    return token


def decrypt_token(token, key, salt):
    password = key.encode()
    key = created_key(password, salt)
    data = decrypt_file(token, key)

    return data


def encrypt_file(bytes, key):
    try:
        bytes = bytes.encode()
    except:
        bytes = bytes

    f = Fernet(key)
    token = f.encrypt(bytes)

    return token


def decrypt_file(file, key):
    f = Fernet(key)
    data = f.decrypt(file)

    return data


def create_share_key(sp_private, password, token, key, salt):
    password = password.encode('UTF-8')

    with open(sp_private, "rb") as key_file:
        sp_private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=password,
            backend=default_backend()
        )

    data = decrypt_token(token, key, salt)

    ps_public_key = serialization.load_pem_public_key(
        data,
        backend=default_backend()
    )

    shared_key = sp_private_key.exchange(
        ec.ECDH(), ps_public_key)

    return shared_key


def get_decrypt_key(password, id):
    dir = f"Chat/{id}/key/private_key.txt"
    try:
        share_key = create_share_key(
            dir, password, SERVER_TOKEN.encode(), KEY_MASTER, SALT.encode())
    except ValueError:
        return {"message": "wrong password"}

    decrypt_key = created_key(share_key, SALT.encode())
    return decrypt_key
