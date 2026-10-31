from vault import Vault
from commands import add_entry, list_entries, get_entry, delete_entry


def main():
    vault = Vault(None)
    vault.load()

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
