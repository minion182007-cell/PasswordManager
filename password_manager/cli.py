"""Интерфейс командной строки: вход и главное меню."""

import argparse
import sys
from getpass import getpass

from password_manager.core import PasswordManager

MAX_ATTEMPTS = 3


def build_parser() -> argparse.ArgumentParser:
    """Создать парсер аргументов командной строки."""
    parser = argparse.ArgumentParser(description="Менеджер паролей в терминале")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--init", action="store_true", help="создать новое хранилище")
    group.add_argument("--unlock", action="store_true", help="открыть хранилище и перейти в меню")
    group.add_argument("--generate", action="store_true", help="сгенерировать надёжный пароль")

    args = parser.parse_args()
    return (parser)


def run_init(manager: PasswordManager) -> int:
    """Создать хранилище. Вернуть код выхода: 0 — успех, 1 — ошибка."""
    pwd = getpass("Придумайте мастер паролей: ")
    pwd2 = getpass("Повторите мастер паролей:")
    if pwd == "":
        print("Ваш текст про пустой пароль")
        return 1
    if pwd != pwd2:
        print("Ваши пароли не совпали")
        return 1
    try:
        manager.init_master(pwd)
    except FileExistsError:
        print("Хранилище уже создано. Используйте --unlock")
        return 1
    print("Хранилище создано")
    return 0


def run_unlock(manager: PasswordManager) -> bool:
    """До MAX_ATTEMPTS попыток ввести мастер-пароль. True — открыто."""
    atempt = MAX_ATTEMPTS
    for i in range(atempt):
        pwd = getpass("Придумайте мастер паролей: ")
        if manager.unlock(pwd):
            return True
        atempt -= 1
        if atempt > 0:
            print(f"Неверный пароль, осталось {atempt}")
    return False

def cmd_get(manager: PasswordManager) -> None:
    """Повторно спросить мастер-пароль, затем показать логин и пароль."""


def menu(manager: PasswordManager) -> None:
    """Главное меню — бывший цикл while из main()."""


def main(argv: list[str] | None = None) -> int:
    """Разобрать аргументы и запустить нужный режим. Вернуть код выхода."""


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



def main(argv: list[str] | None = None) -> int:
    """Разобрать аргументы и запустить нужный режим. Вернуть код выхода."""
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.init:
        return run_init(PasswordManager())

    if args.unlock:
        manager = PasswordManager()
        if not manager.exists():
            print("Хранилище не найдено. Сначала выполните --init")
            return 1
        if not run_unlock(manager):
            return 1
        menu(manager)
        return 0

    if args.generate:
        print("тут будет --generate")
        return 0

    parser.print_help()
    return 1
