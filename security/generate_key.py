import os

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization

from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from utils._file import create_new_dir


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
