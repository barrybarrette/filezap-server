import hashlib


def hash_password(plaintext_password, salt):
    sha256 = hashlib.sha256(plaintext_password.encode())
    sha256.update(salt)
    return sha256.hexdigest()