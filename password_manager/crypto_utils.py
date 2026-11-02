"""Криптография: получение ключа из пароля, шифрование и расшифровка."""

import base64

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

ITERATIONS = 600_000


def derive_key(password, salt):
    """Получить ключ Fernet из мастер-пароля (строка) и соли (байты)."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=ITERATIONS
    )
    password = password.encode()
    key = base64.urlsafe_b64encode(kdf.derive(password))
    return key


def encrypt(data, key):
    """Зашифровать байты data ключом key, вернуть токен (байты)."""
    f = Fernet(key)
    return f.encrypt(data)


def decrypt(token, key):
    """Расшифровать токен ключом key, вернуть исходные байты.
    При неверном ключе выбрасывает InvalidToken."""
    f = Fernet(key)
    return f.decrypt(token)
