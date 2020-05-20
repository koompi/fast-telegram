from cryptography.fernet import Fernet


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
