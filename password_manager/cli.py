"""Интерфейс командной строки: вход и главное меню."""

import argparse
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
    return parser


def run_init(manager: PasswordManager) -> int:
    """Создать хранилище. Вернуть код выхода: 0 — успех, 1 — ошибка."""
    if manager.exists():
        print("Хранилище уже создано. Используйте --unlock")
        return 1
    pwd = getpass("Придумайте мастер-пароль: ")
    pwd2 = getpass("Повторите мастер-пароль: ")
    if not pwd:
        print("Мастер-пароль не может быть пустым")
        return 1
    if pwd != pwd2:
        print("Пароли не совпали, запустите --init ещё раз")
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
    attempts_left = MAX_ATTEMPTS
    for _ in range(MAX_ATTEMPTS):
        pwd = getpass("Введите мастер-пароль: ")
        if manager.unlock(pwd):
            return True
        attempts_left -= 1
        if attempts_left > 0:
            print(f"Неверный пароль, осталось попыток: {attempts_left}")
    print("Попытки закончились")
    return False


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
    """Спросить сайт, подтвердить мастер-паролем и показать логин и пароль."""
    name = input("Введите сайт: ").strip()
    entry = manager.get_entry(name)
    if entry is None:
        print("Нет такого сайта в базе")
        return
    pwd = getpass("Подтвердите мастер-пароль: ")
    if not manager.verify(pwd):
        print("Неверный мастер-пароль")
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


def menu(manager: PasswordManager) -> None:
    """Главное меню: цикл команд до выхода."""
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


def _run(argv: list[str] | None) -> int:
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


def main(argv: list[str] | None = None) -> int:
    """Точка входа: запустить программу и аккуратно обработать Ctrl+C."""
    try:
        return _run(argv)
    except KeyboardInterrupt:
        print("\nВыход")
        return 130
