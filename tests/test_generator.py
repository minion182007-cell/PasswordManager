import pytest

from password_manager.crypto_utils import generate_password
import string


def test_password_has_requested_length():
    # сгенерировать пароль длиной, например, 20 → len(...) должен быть 20
    pwd = generate_password(20)
    assert len(pwd) == 20


def test_password_contains_all_kinds():
    pwd = generate_password()
    assert any(ch in string.ascii_letters for ch in pwd)
    assert any(ch in string.digits for ch in pwd)
    assert any(ch in string.punctuation for ch in pwd)


def test_passwords_are_different():
    pwd = generate_password()
    pwd2 = generate_password()
    assert pwd != pwd2


def test_too_short_length_fails():
    with pytest.raises(ValueError):
        generate_password(6)
