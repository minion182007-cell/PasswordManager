"""Интерфейс командной строки: вход и главное меню."""

import os
from getpass import getpass

from password_manager.core import PasswordManager
from password_manager.crypto_utils import derive_key

SALT_PATH = "salt.bin"


def cmd_add(manager: PasswordManager) -> None:
    """Спросить сайт, логин и пароль и добавить запись."""
    name = input("Введите сайт: ").strip()
    login = input("Введите логин: ").strip()
    pwd = getpass("Пароль: ")

    if not name or not pwd:
        print("Сайт и пароль не могут быть пустыми")
        return

    if manager.has_entry(name):
        answer = input("Запись уже есть. Перезаписать? (да/нет): ").strip().lower()
        if answer != "да":
            print("Отменено")
            return

    manager.add_entry(name, login, pwd)
    print("Сохранено")


def cmd_list(manager: PasswordManager) -> None:
    """Показать названия всех записей."""
    names = manager.list_entries()
    if not names:
        print("Записей нет")
        return
    for name in names:
        print(f"- {name}")


def cmd_get(manager: PasswordManager) -> None:
    """Спросить сайт и показать его логин и пароль."""
    name = input("Введите сайт: ").strip()
    entry = manager.get_entry(name)
    if entry is None:
        print("Не найдено")
        return
    print(f"Логин:  {entry['login']}")
    print(f"Пароль: {entry['password']}")


def cmd_delete(manager: PasswordManager) -> None:
    """Спросить сайт и удалить его запись."""
    name = input("Введите сайт: ").strip()
    if manager.delete_entry(name):
        print("Удалено")
    else:
        print("Не найдено")


def _temporary_login() -> PasswordManager:
    """Временный вход: соль + мастер-пароль → ключ. Заменится в задании 2."""
    if os.path.exists(SALT_PATH):
        with open(SALT_PATH, "rb") as f:
            salt = f.read()
    else:
        salt = os.urandom(16)
        with open(SALT_PATH, "wb") as f:
            f.write(salt)

    password = getpass("Мастер-пароль: ")
    manager = PasswordManager(derive_key(password, salt))
    manager._load()
    return manager


def main() -> None:
    """Войти и запустить главное меню."""
    manager = _temporary_login()

    while True:
        print("\n=== Менеджер паролей ===")
        print("1. Добавить запись")
        print("2. Список записей")
        print("3. Показать пароль")
        print("4. Удалить запись")
        print("0. Выход")

        choice = input("> ").strip()

        if choice == "1":
            cmd_add(manager)
        elif choice == "2":
            cmd_list(manager)
        elif choice == "3":
            cmd_get(manager)
        elif choice == "4":
            cmd_delete(manager)
        elif choice == "0":
            print("До свидания")
            break
        else:
            print("Нет такой команды")
