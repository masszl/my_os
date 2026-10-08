import sys
from pathlib import Path

root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(root))
sys.path.insert(0, str(root / "src"))

from src import db, fs


def cleanup():
    for path in fs.list_files("/f08_"):
        fs.delete_file(path)


def test_create_file():
    result = fs.create_file("/f08_01.txt", "hello", "admin")

    assert result > 0
    assert fs.read_file("/f08_01.txt") == "hello"
    print("[PASS] FT-01: создание файла")


def test_create_duplicate():
    result = fs.create_file("/f08_01.txt", "second", "admin")

    assert result == -1
    assert fs.read_file("/f08_01.txt") == "hello"
    print("[PASS] FT-02: дубликат отклонён")


def test_read_file():
    result = fs.read_file("/f08_01.txt")

    assert result == "hello"
    print("[PASS] FT-03: чтение файла")


def test_read_missing():
    result = fs.read_file("/f08_missing.txt")

    assert result == ""
    print("[PASS] FT-04: отсутствующий файл")


def test_write_file():
    fs.write_file("/f08_01.txt", "new")

    assert fs.read_file("/f08_01.txt") == "new"
    print("[PASS] FT-05: изменение файла")


def test_delete_file():
    fs.create_file("/f08_06.txt", "delete", "admin")
    fs.delete_file("/f08_06.txt")

    assert fs.get_file_info("/f08_06.txt") is None
    print("[PASS] FT-06: удаление файла")


def test_list_files():
    fs.create_file("/f08_07a.txt", "a", "admin")
    fs.create_file("/f08_07b.txt", "b", "admin")

    files = fs.list_files("/f08_")

    assert "/f08_07a.txt" in files
    assert "/f08_07b.txt" in files
    print("[PASS] FT-07: список файлов")


def test_get_owner():
    result = fs.get_owner("/f08_01.txt")

    assert result == "admin"
    print("[PASS] FT-08: получение владельца")


def test_get_owner_missing():
    result = fs.get_owner("/f08_missing.txt")

    assert result is None
    print("[PASS] FT-09: отсутствующий владелец")


def test_get_file_info():
    info = fs.get_file_info("/f08_01.txt")

    assert info is not None
    assert info["path"] == "/f08_01.txt"
    assert info["content"] == "new"
    assert info["owner"] == "admin"

    print("[PASS] FT-10: информация о файле")


if __name__ == "__main__":
    db.init_db()
    cleanup()

    try:
        test_create_file()
        test_create_duplicate()
        test_read_file()
        test_read_missing()
        test_write_file()
        test_delete_file()
        test_list_files()
        test_get_owner()
        test_get_owner_missing()
        test_get_file_info()

        print("\nВсе функциональные тесты fs.py пройдены")
    finally:
        cleanup()