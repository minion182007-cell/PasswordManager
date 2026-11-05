"""Криптография: ключ и хеш из пароля, шифрование записей, генератор паролей."""

import base64
import hmac
import secrets
import string

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

ITERATIONS = 600_000
MIN_PASSWORD_LENGTH = 8
ALPHABET = string.ascii_letters + string.digits + string.punctuation


def derive_key(password: str, salt: bytes) -> bytes:
    """Получить ключ Fernet из мастер-пароля (строка) и соли (байты)."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(), length=32, salt=salt, iterations=ITERATIONS
    )
    password_byte = password.encode()
    key = base64.urlsafe_b64encode(kdf.derive(password_byte))
    return key


def encrypt(data: bytes, key: bytes) -> bytes:
    """Зашифровать байты data ключом key, вернуть токен (байты)."""
    f = Fernet(key)
    return f.encrypt(data)


def decrypt(token: bytes, key: bytes) -> bytes:
    """Расшифровать токен ключом key, вернуть исходные байты.
    При неверном ключе выбрасывает InvalidToken."""
    f = Fernet(key)
    return f.decrypt(token)


def hash_master(password: str, salt: bytes) -> bytes:
    """Возвращает хеш мастер-пароля(32 сырых байта)"""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(), length=32, salt=salt, iterations=ITERATIONS
    )
    password_byte = password.encode()
    return kdf.derive(password_byte)


def verify_master(password: str, salt: bytes, expected: bytes) -> bool:
    """Возвращает True если хеш совпадает с паролем"""
    hm = hash_master(password, salt)
    return hmac.compare_digest(hm, expected)


def generate_password(length: int = 16) -> str:
    """Сгенерировать пароль из букв, цифр и спецсимволов, в котором есть все три вида."""
    if length < MIN_PASSWORD_LENGTH:
        raise ValueError("Длина не достигает 8")
    while True:
        pwd = "".join(secrets.choice(ALPHABET) for _ in range(length))
        if (
            any(ch in string.ascii_letters for ch in pwd)
            and any(ch in string.digits for ch in pwd)
            and any(ch in string.punctuation for ch in pwd)
        ):
            return pwd
