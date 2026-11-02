import json
import os
from password_manager.crypto_utils import encrypt, decrypt

DEFAULT_PATH = "vault.json"


class PasswordManager:
    """Хранилище паролей: держит записи в памяти и умеет сохранять их в файл."""

    def __init__(self, key: bytes, path: str = DEFAULT_PATH) -> None:
        self._key = key
        self._path = path
        self._entries: dict[str, dict[str, str]] = {}

    def _load(self) -> None:
        """Загрузить записи из файла. Если файла нет — оставить пустой словарь."""
        if not os.path.exists(self._path):
            self._entries = {}
            return
        with open(self._path, "rb") as f:
            token = f.read()

        data = decrypt(token, self._key)
        txt = data.decode()
        self._entries = json.loads(txt)

    def _persist(self) -> None:
        """Записать все записи в файл."""
        txt = json.dumps(self._entries, ensure_ascii=False)
        token = encrypt(txt.encode(), self._key)
        with open(self._path, "wb") as f:
            f.write(token)

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
        return list(self._entries)
