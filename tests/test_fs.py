import sys
from pathlib import Path

root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root))
sys.path.insert(0, str(root / "src"))

from src import fs


def test_create_and_read():
    fs.create_file("/t1.txt", "content1", "admin")
    assert fs.read_file("/t1.txt") == "content1"
    print("[PASS] создание и чтение файла")


def test_duplicate_path():
    fs.create_file("/t2.txt", "a", "admin")
    result = fs.create_file("/t2.txt", "b", "admin")
    assert result == -1
    print("[PASS] дубликат пути отклонён")


def test_update():
    fs.create_file("/t3.txt", "old", "admin")
    fs.write_file("/t3.txt", "new")
    assert fs.read_file("/t3.txt") == "new"
    print("[PASS] содержимое обновлено")


def test_delete():
    fs.create_file("/t4.txt", "x", "admin")
    fs.delete_file("/t4.txt")
    assert fs.read_file("/t4.txt") == ""
    print("[PASS] удаление файла")


def test_owner():
    fs.create_file("/t5.txt", "x", "admin")
    assert fs.get_owner("/t5.txt") == "admin"
    assert fs.get_owner("/missing") is None
    print("[PASS] владелец определён")


def test_list():
    fs.create_file("/list1.txt", "a", "admin")
    fs.create_file("/list2.txt", "b", "admin")

    files = fs.list_files("/")

    assert "/list1.txt" in files
    assert "/list2.txt" in files
    print("[PASS] список файлов по префиксу")


if __name__ == "__main__":
    test_create_and_read()
    test_duplicate_path()
    test_update()
    test_delete()
    test_owner()
    test_list()

    print("Все тесты файловой системы пройдены")