"""Тесты класса PasswordManager."""

from pathlib import Path

import pytest

from password_manager.core import PasswordManager


def make_vault(tmp_path: Path) -> str:
    """Создать хранилище с паролем "secret" во временной папке, вернуть путь."""
    path = str(tmp_path / "vault.json")
    PasswordManager(path).init_master("secret")
    return path


def test_unlock_with_correct_password(tmp_path: Path) -> None:
    """Сверяет пароль"""
    manager = PasswordManager(make_vault(tmp_path))
    assert manager.unlock("secret") is True


def test_unlock_with_wrong_password(tmp_path: Path) -> None:
    """Открывает хранилище неверным паролем -> должно вернуться False"""
    tst = PasswordManager(make_vault(tmp_path))
    assert tst.unlock("secret") is True
    assert tst.unlock("Неверный паролььььь") is False


def test_init_twice_fails(tmp_path: Path) -> None:
    """Повторный init_master по тому же пути выбрасывает FileExistsError."""
    path = make_vault(tmp_path)
    with pytest.raises(FileExistsError):
        PasswordManager(path).init_master("other")


def test_add_then_list_and_get(tmp_path: Path) -> None:
    """Тест проверки списка и получения по имени"""
    tst = PasswordManager(make_vault(tmp_path))
    assert tst.unlock("secret") is True
    tst.add_entry("github.com", "ivan", "qwerty")
    assert "github.com" in tst.list_entries()
    assert tst.get_entry("github.com") == {"login": "ivan", "password": "qwerty"}


def test_entry_survives_reopen(tmp_path: Path) -> None:
    """Тест на запись"""
    path = make_vault(tmp_path)

    first = PasswordManager(path)
    first.unlock("secret")
    first.add_entry("github.com", "ivan", "qwerty")

    second = PasswordManager(path)
    second.unlock("secret")
    assert second.get_entry("github.com") == {"login": "ivan", "password": "qwerty"}


def test_delete_removes_entry(tmp_path: Path) -> None:
    """Тест удаления"""
    path = make_vault(tmp_path)

    first = PasswordManager(path)
    first.unlock("secret")
    first.add_entry("github.com", "ivan", "qwerty")
    b = first.delete_entry("github.com")
    assert b
    assert first.get_entry("github.com") is None
    assert first.delete_entry("github.com") is False


def test_file_has_no_plaintext(tmp_path: Path) -> None:
    """Тест на наличие в str паролей"""
    path = make_vault(tmp_path)

    first = PasswordManager(path)
    first.unlock("secret")
    first.add_entry("github.com", "ivan", "qwerty")

    with open(path, encoding="utf-8") as content:
        t = content.read()
        assert "qwerty" not in t
        assert "secret" not in t


def test_locked_manager_refuses(tmp_path: Path) -> None:
    """Тест на прочтения не открытого файла"""
    tst = PasswordManager(make_vault(tmp_path))
    with pytest.raises(PermissionError):
        tst.list_entries()
