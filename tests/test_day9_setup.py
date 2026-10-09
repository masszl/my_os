
import sys
from pathlib import Path

root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root))
sys.path.insert(0, str(root / "src"))

from src import db, fs
from src.auth import register_user, authenticate


def prepare_user(login, password, role):
    users = db.execute_select("users", {"login": login})

    if not users:
        register_user(login, password, role)
        print(f"[OK] Пользователь {login} создан")
    else:
        print(f"[OK] Пользователь {login} уже существует")


def main():
    db.init_db()

    prepare_user("admin", "admin123", "admin")
    prepare_user("user", "user1234", "user")

    admin = authenticate("admin", "admin123")
    user = authenticate("user", "user1234")

    print("Вход admin с admin123:", admin is not None)
    print("Вход user с user1234:", user is not None)

    path = "/ss02_a.txt"

    if fs.get_file_info(path) is None:
        fs.create_file(path, "admin file", "admin")
        print("[OK] Файл администратора создан")
    else:
        print("[OK] Файл администратора уже существует")

    assert fs.get_owner(path) == "admin"

    print("\nПодготовка завершена")


if __name__ == "__main__":
    main()
