import sys
from pathlib import Path

root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root))
sys.path.insert(0, str(root / "src"))

from src import db


TEST_LOGIN = "day7_test_user"


def cleanup():
    db.execute_delete("users", {"login": TEST_LOGIN})


def test_insert():
    cleanup()

    user_id = db.execute_insert("users", {
        "login": TEST_LOGIN,
        "password_hash": "test_hash",
        "role": "user"
    })

    assert user_id > 0
    print("[PASS] добавление записи")


def test_select():
    users = db.execute_select("users", {"login": TEST_LOGIN})

    assert len(users) == 1
    assert users[0]["login"] == TEST_LOGIN
    print("[PASS] выборка записи")


def test_update():
    db.execute_update(
        "users",
        {"role": "admin"},
        {"login": TEST_LOGIN}
    )

    users = db.execute_select("users", {"login": TEST_LOGIN})

    assert users[0]["role"] == "admin"
    print("[PASS] обновление записи")


def test_delete():
    db.execute_delete("users", {"login": TEST_LOGIN})

    users = db.execute_select("users", {"login": TEST_LOGIN})

    assert len(users) == 0
    print("[PASS] удаление записи")


def test_select_missing():
    users = db.execute_select(
        "users",
        {"login": "day7_missing_user"}
    )

    assert len(users) == 0
    print("[PASS] поиск отсутствующей записи")


def test_multiple_records():
    cleanup()

    db.execute_insert("users", {
        "login": TEST_LOGIN,
        "password_hash": "test_hash",
        "role": "user"
    })

    users = db.execute_select("users")

    assert len(users) >= 1
    print("[PASS] выборка нескольких записей")

    cleanup()


if __name__ == "__main__":
    db.init_db()

    test_insert()
    test_select()
    test_update()
    test_delete()
    test_select_missing()
    test_multiple_records()

    print("\nВсе тесты db.py пройдены")