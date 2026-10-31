import json
import os

VAULT_FILE = "vault.json"


class Vault:
    """Хранилище паролей: держит записи в памяти и умеет сохранять их в файл."""

    def __init__(self, key):
        self.key = key          # ключ шифрования (пока не используется)
        self.entries = {}       # {"сайт": {"login": ..., "password": ...}}

    # --- работа с файлом ---

    def load(self):
        """Загрузить записи из файла. Если файла нет — оставить пустой словарь."""
        if not os.path.exists(VAULT_FILE):
            self.entries = {}
            return
        with open(VAULT_FILE, "r", encoding="utf-8") as f:
            self.entries = json.load(f)

    def save(self):
        """Записать все записи в файл."""
        with open(VAULT_FILE, "w", encoding="utf-8") as f:
            json.dump(self.entries, f, ensure_ascii=False, indent=4)

    # --- операции с записями ---

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