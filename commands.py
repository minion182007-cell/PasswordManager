"""Диалоги с пользователем: ввод данных и вывод результатов."""

from getpass import getpass


def add_entry(vault):
    """Спросить сайт, логин и пароль и добавить запись в хранилище."""
    website = input("Введите сайт: ").strip()
    login = input("Введите логин: ").strip()
    password = getpass("Пароль: ")

    if not website or not password:
        print("Сайт и пароль не могут быть пустыми")
        return

    if vault.exists(website):
        answer = input("Запись уже есть. Перезаписать? (да/нет): ").strip().lower()
        if answer != "да":
            print("Отменено")
            return

    vault.add(website, login, password)
    print("Сохранено")


def list_entries(vault):
    """Показать все записи: сайт и логин, пароль скрыт звёздочками."""
    sites = vault.list_sites()
    if not sites:
        print("Записей нет")
        return
    for site, login in sites:
        print(f"{site:20} | {login:20} | {'*' * 8}")


def get_entry(vault):
    """Спросить сайт и показать его логин и пароль в открытом виде."""
    website = input("Введите сайт: ").strip()
    data = vault.get(website)
    if data is None:
        print("Не найдено")
        return
    print(f"Логин:  {data['login']}")
    print(f"Пароль: {data['password']}")


def delete_entry(vault):
    """Спросить сайт и удалить его запись из хранилища."""
    website = input("Введите сайт: ").strip()
    if vault.delete(website):
        print("Удалено")
    else:
        print("Не найдено")