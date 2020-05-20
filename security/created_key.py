import base64
import os

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization

from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


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
