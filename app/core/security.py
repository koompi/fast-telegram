import os
import bcrypt
import base64

from passlib.context import CryptContext
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet

from ..core.config import SECRET_KEY, SALT

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def generate_salt():
    return bcrypt.gensalt().decode()


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def generate_private_public_key(password):
    private_key = ec.generate_private_key(ec.SECP384R1(), default_backend())
    public_key = private_key.public_key()

    if password is not None:
        password = password.encode('UTF-8')

        serialized_private_key = private_key.private_bytes(
            encoding=(serialization.Encoding.PEM),
            format=(serialization.PrivateFormat.PKCS8),
            encryption_algorithm=(
                serialization.BestAvailableEncryption(password))
        )

    else:
        serialized_private_key = private_key.private_bytes(
            encoding=(serialization.Encoding.PEM),
            format=(serialization.PrivateFormat.PKCS8),
            encryption_algorithm=(serialization.NoEncryption())
        )
    serialized_public_key = public_key.public_bytes(
        encoding=(serialization.Encoding.PEM),
        format=(serialization.PublicFormat.SubjectPublicKeyInfo)

    )
    try:
        os.mkdir('./key')
    except FileExistsError:
        pass
    diretory = './key'
    private_key_dir = f"{diretory}/private_key.txt"
    public_key_dir = f"{diretory}/public_key.txt"

    with open(private_key_dir, 'wb') as (f):
        f.write(serialized_private_key)
    with open(public_key_dir, 'wb') as (f):
        f.write(serialized_public_key)

    data = [private_key_dir, public_key_dir]
    return data


def create_derive_key(key, salt):
    key = PBKDF2HMAC(algorithm=(
        hashes.SHA256()),
        length=32,
        salt=salt,
        iterations=100000,
        backend=(default_backend())
    ).derive(key)

    key = base64.urlsafe_b64encode(key)

    return key


def create_token(public_key):
    key = create_derive_key(
        salt=(SALT.encode()),
        key=(str(SECRET_KEY).encode())
    )
    f = Fernet(key)
    token = f.encrypt(public_key)
    return token


def decrypt_token(token):
    key = create_derive_key(
        salt=(SALT.encode()),
        key=(str(SECRET_KEY).encode())
        )
    f = Fernet(key)
    public_key = f.decrypt(token)

    return public_key


def create_encrypt_key(password, public_key, salt):
    if password is None:
        password = None
    else:
        password = password.encode('UTF-8')

    with open('./key/private_key.txt', 'rb') as f:
        private_key = serialization.load_pem_private_key(
            f.read(),
            password=password,
            backend=default_backend()
        )
    public_key = serialization.load_pem_public_key(
        public_key,
        backend=default_backend()
    )
    shared_key = private_key.exchange(
        ec.ECDH(), public_key)

    crypto_key = create_derive_key(shared_key, salt.encode())

    return crypto_key


def encrypt_file(bytes, key):
    f = Fernet(key)
    token = f.encrypt(bytes)
    return token
