import json
import os
import base64
from password_manager.crypto_utils import encrypt, decrypt, hash_master, derive_key,verify_master

DEFAULT_PATH = "vault.json"


class PasswordManager:
    """Хранилище паролей: держит записи в памяти и умеет сохранять их в файл."""

    def __init__(self, path: str = DEFAULT_PATH) -> None:
        self._path = path
        self._entries: dict[str, dict[str, str]] = {}
        self._key: bytes | None = None
        self._master_salt: bytes | None = None
        self._master_hash: bytes | None = None
        self._key_salt: bytes | None = None

    def _load(self) -> dict[str, str]:
        """Прочитать файл хранилища и вернуть его содержимое."""
        with open(self._path, "r", encoding="utf-8") as f:
            raw: dict[str, str] = json.load(f)
        return raw

    def _persist(self) -> None:
        """Зашифровать записи и записать хранилище в JSON-файл."""
        key = self._require_unlocked()
        if self._master_salt is None or self._master_hash is None or self._key_salt is None:
            raise RuntimeError("Хранилище не инициализировано")


        plain = json.dumps(self._entries, ensure_ascii=False).encode()
        token = encrypt(plain, key).decode()


        raw = {
            "master_salt": base64.b64encode(self._master_salt).decode(),
            "master_hash": base64.b64encode(self._master_hash).decode(),
            "key_salt": base64.b64encode(self._key_salt).decode(),
            "data": token,
        }

        with open(self._path, "w", encoding="utf-8") as f:
            json.dump(raw, f, indent=2)


    def has_entry(self, name: str) -> bool:
        """Проверить, есть ли запись с таким названием."""
        return name in self._entries

    def add_entry(self, name: str, login: str, pwd: str) -> None:
        """Добавить или перезаписать запись и сразу сохранить."""
        self._entries[name] = {"login": login, "password": pwd}
        self._persist()

    def get_entry(self, name: str) -> dict[str, str] | None:
        """Вернуть запись (словарь) или None, если такой нет."""
        return self._entries.get(name)

    def delete_entry(self, name: str) -> bool:
        """Удалить запись. Вернуть True, если удалили, и False, если такой не было."""
        if name not in self._entries:
            return False
        del self._entries[name]
        self._persist()
        return True

    def list_entries(self) -> list[str]:
        """Вернуть назваание всех записей."""
        self._require_unlocked()
        return list(self._entries)

    def init_master(self, password: str) -> None:
        """Создает хранилище"""
        if os.path.exists(self._path):
            raise FileExistsError(f"Хранилище уже существует: {self._path}")

        self._key_salt = os.urandom(16)
        self._master_salt = os.urandom(16)
        self._master_hash = hash_master(password, self._master_salt)

        self._key = derive_key(password, self._key_salt)
        self._entries = {}
        self._persist()
    def unlock(self, password: str) -> bool:
        """Проверить мастер-пароль и загрузить записи. Вернуть True при успехе."""
        if not os.path.exists(self._path):
            return False
        raw=self._load()


        master_salt = base64.b64decode(raw["master_salt"])
        master_hash = base64.b64decode(raw["master_hash"])
        key_salt=base64.b64decode(raw["key_salt"])
        if not verify_master(password,master_salt,master_hash):
            return False
        self._master_salt = master_salt
        self._master_hash = master_hash
        self._key_salt = key_salt
        self._key=derive_key(password,self._key_salt)

        token = raw["data"].encode()
        plain = decrypt(token, self._key)
        self._entries = json.loads(plain.decode())
        return True

    def _require_unlocked(self) -> bytes:
        """Вернуть ключ шифрования или выбросить PermissionError, если хранилище закрыто."""
        if self._key is None:
            raise PermissionError("Хранилище закрыто: сначала вызовите unlock()")
        return self._key
