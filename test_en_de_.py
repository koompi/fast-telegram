import base64
import os

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization
from cryptography.fernet import Fernet

from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def generate_key(key_name, password):
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

    private_key_dir = f'{key_name}_private_key.txt'
    public_key_dir = f'{key_name}_public_key.txt'

    with open(private_key_dir, 'wb') as f:
        f.write(serialized_private_key)

    with open(public_key_dir, 'wb') as f:
        f.write(serialized_public_key)


def create_share_key(sp_private, ps_public, password):
    password = password.encode('UTF-8')

    with open(sp_private, "rb") as key_file:
        sp_private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=password,
            backend=default_backend()
        )

    with open(ps_public, "rb") as key_file:
        ps_public_key = serialization.load_pem_public_key(
            key_file.read(),
            backend=default_backend()
        )

    shared_key = sp_private_key.exchange(
        ec.ECDH(), ps_public_key)

    return shared_key


def create_derived_key(shared_key, salt):
    derived_key = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    ).derive(shared_key)

    derived_key = base64.urlsafe_b64encode(derived_key)

    return derived_key


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


salt = "awds".encode('UTF-8')

pfile = "Z_key/peer_private_key.txt"
sfile = "Z_key/server_public_key.txt"
share_key = create_share_key(pfile, sfile, "123")
key = create_derived_key(share_key, salt=salt)

chunksize = 1024


with open("vdo.mp4", 'rb') as f:
    while True:
        data = f.read(chunksize)
        if not data:
            break  # done
        encrypt = encrypt_file(data, key)
        print(encrypt)
