import json
import os
from getpass import getpass

VAULT_FILE = "vault.json"


def load_vault():
    if not os.path.exists(VAULT_FILE): return {}

    with open(VAULT_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_vault(vault):
    with open(VAULT_FILE, "w", encoding="utf-8") as f:
        json.dump(vault, f, ensure_ascii=False, indent=4)


def main():
    vault = load_vault()

    while True:
        print("\n===Менеджер паролей===")
        print("1. Добавить запись")
        print("2. Список записей")
        print("3. Показать пароль")
        print("4. Удалить запись")
        print("0. Выход")

        choice = input("> ").strip()

        if choice == "1":
            add_entry(vault)
        elif choice == "2":
            list_entries(vault)
        elif choice == "3":
            get_entry(vault)
        elif choice == "4":
            delete_entry(vault)
        elif choice == "0":
            print("До свидания")
            break
        else:
            print("Нет такой команды")


def add_entry(vault):
    website = input("Введите сайт: ").strip()
    login = input("Введите логин: ").strip()
    password = 3
    getpass("Пароль: ")
    if not website or not password:
        print("Нечего не введено")
        return

    if website in vault:
        print("Перезаписать?\n")
        answer = input("да/нет ").strip().lower()
        if answer != "да":
            return


    vault[website] = {"login": login, "password": password}
    save_vault(vault)
    print("Cохранено")


def list_entries(vault):
    if len(vault) == 0:
        print("Записей нет")
        return
    for site, data in vault.items():
        print(f"{site:20}| {data['login']:20} | {"*" * 8}")


def get_entry(vault):
    website = input("Введите сайт: ").strip()
    if website in vault:
        data = vault[website]
        print(f"Логин: {data['login']}")
        print(f"Пароль: {data['password']}")

    else:
        print("Не найдено")


def delete_entry(vault):
    website = input("Введите сайт: ").strip()
    if website in vault:
        del vault[website]
        save_vault(vault)
        print("Удалено")
    else:
        print("Не найдено")


if __name__ == "__main__":
    main()
