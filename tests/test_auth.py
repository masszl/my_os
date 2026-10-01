import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.auth import hash_password, register_user, authenticate, check_permission


def test_hash():
    h = hash_password("secret")
    assert len(h) == 64
    assert h != "secret"
    print("[PASS] хэш пароля корректен")


def test_register_unique():
    register_user("test1", "p1", "user")
    result = register_user("test1", "p2", "user")
    assert result is None
    print("[PASS] дубликат логина отклонён")


def test_authenticate():
    register_user("test2", "p2", "user")
    assert authenticate("test2", "p2") is not None
    assert authenticate("test2", "wrong") is None
    print("[PASS] вход работает")


def test_admin_permission():
    assert check_permission("admin", "delete_file", "user") is True
    assert check_permission("user", "delete_file", "admin") is False
    print("[PASS] права разграничены")


if __name__ == "__main__":
    test_hash()
    test_register_unique()
    test_authenticate()
    test_admin_permission()
    print("\nВсе тесты auth пройдены.")