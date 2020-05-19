import os

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization

from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

salt = os.urandom(16)


def generate_key(password):
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

    with open('server_private_key.txt', 'wb') as f:
        f.write(serialized_private_key)

    with open('server_public_key.txt', 'wb') as f:
        f.write(serialized_public_key)


# generate_key('123')


def load_pbKey(password):
    with open('server_private_key.txt', 'rb') as f:
        private_key = f.read()
    password = password.encode('UTF-8')

    loaded_private_key = serialization.load_pem_private_key(
        private_key,
        password=password,
        backend=default_backend()
    )
    public_key = loaded_private_key.public_key()

    public_key = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ).decode('UTF-8')

    return public_key


public_key = load_pbKey('123')
print(public_key)

# peer_private_key = ec.generate_private_key(
#     ec.SECP384R1(), default_backend()
# )
# shared_key = server_private_key.exchange(
#     ec.ECDH(), peer_private_key.public_key())


# derived_key = PBKDF2HMAC(
#     algorithm=hashes.SHA256(),
#     length=64,
#     salt=salt,
#     iterations=100000,
#     backend=default_backend()
# ).derive(shared_key)


# same_shared_key = peer_private_key.exchange(
#     ec.ECDH(), server_private_key.public_key())


# # Perform key derivation.
# same_derived_key = PBKDF2HMAC(
#     algorithm=hashes.SHA256(),
#     length=64,
#     salt=salt,
#     iterations=100000,
#     backend=default_backend()
# ).derive(same_shared_key)

# if derived_key == same_derived_key:

#     byte_array = bytearray(derived_key)
#     derived_key = byte_array.hex()
#     print(derived_key)

#     byte_array = bytearray(same_derived_key)
#     same_derived_key = byte_array.hex()
#     print(same_derived_key)
