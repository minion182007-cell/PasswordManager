import json
import os
from crypto_utils import encrypt, decrypt

VAULT_FILE = "vault.dat"


class Vault:
    """Хранилище паролей: держит записи в памяти и умеет сохранять их в файл."""

    def __init__(self, key):
        self.key = key
        self.entries = {}

    def load(self):
        """Загрузить записи из файла. Если файла нет — оставить пустой словарь."""
        if not os.path.exists(VAULT_FILE):
            self.entries = {}
            return
        with open(VAULT_FILE, "rb") as f:
            token = f.read()

        data = decrypt(token, self.key)
        txt = data.decode()
        self.entries = json.loads(txt)

    def save(self):
        """Записать все записи в файл."""
        txt = json.dumps(self.entries, ensure_ascii=False, indent=4)
        token = encrypt(txt.encode(), self.key)
        with open(VAULT_FILE, "wb") as f:
            f.write(token)

    def exists(self, website):
        return website in self.entries

    def add(self, website, login, password):
        """Добавить или перезаписать запись и сразу сохранить."""
        self.entries[website] = {"login": login, "password": password}
        self.save()

    def get(self, website):
        """Вернуть запись (словарь) или None, если такой нет."""
        return self.entries.get(website)

    def delete(self, website):
        """Удалить запись. Вернуть True, если удалили, и False, если такой не было."""
        if website not in self.entries:
            return False
        del self.entries[website]
        self.save()
        return True

    def list_sites(self):
        """Список пар (сайт, логин) без паролей."""
        return [(site, data["login"]) for site, data in self.entries.items()]
