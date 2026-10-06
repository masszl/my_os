import sys
from pathlib import Path

root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root))
sys.path.insert(0, str(root / "src"))

from src import db
from src.auth import (
    hash_password,
    register_user,
    authenticate,
    check_permission
)


TEST_USER = "day7_auth_user"


def cleanup():
    db.execute_delete("users", {"login": TEST_USER})


def test_hash_password():
    result = hash_password("secret")

    assert len(result) == 64
    assert result != "secret"
    print("[PASS] пароль хэшируется")


def test_same_password_hash():
    first = hash_password("secret")
    second = hash_password("secret")

    assert first == second
    print("[PASS] одинаковые пароли дают одинаковый хэш")


def test_different_password_hash():
    first = hash_password("secret")
    second = hash_password("password")

    assert first != second
    print("[PASS] разные пароли дают разные хэши")


def test_register_user():
    cleanup()

    user_id = register_user(TEST_USER, "1234", "user")

    assert user_id is not None
    assert user_id > 0
    print("[PASS] регистрация пользователя")


def test_duplicate_user():
    cleanup()

    register_user(TEST_USER, "1234", "user")
    result = register_user(TEST_USER, "5678", "user")

    assert result is None
    print("[PASS] повторная регистрация отклонена")


def test_authenticate_correct():
    cleanup()

    register_user(TEST_USER, "1234", "user")
    user = authenticate(TEST_USER, "1234")

    assert user is not None
    assert user["login"] == TEST_USER
    print("[PASS] вход с правильным паролем")


def test_authenticate_wrong():
    cleanup()

    register_user(TEST_USER, "1234", "user")
    user = authenticate(TEST_USER, "wrong")

    assert user is None
    print("[PASS] неверный пароль отклонён")


def test_user_permission():
    cleanup()

    register_user(TEST_USER, "1234", "user")

    result = check_permission(
        TEST_USER,
        "delete_file",
        "admin"
    )

    assert result is False
    print("[PASS] удаление чужого файла запрещено")

    cleanup()


if __name__ == "__main__":
    db.init_db()

    test_hash_password()
    test_same_password_hash()
    test_different_password_hash()
    test_register_user()
    test_duplicate_user()
    test_authenticate_correct()
    test_authenticate_wrong()
    test_user_permission()

    print("\nВсе тесты auth.py пройдены")