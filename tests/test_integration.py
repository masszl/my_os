import sys
from pathlib import Path

root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root))
sys.path.insert(0, str(root / "src"))

from src import fs
from src import scheduler
from src.kernel import kernel_instance
from src.syscalls import (
    sys_create_file,
    sys_read_file,
    sys_delete_file,
    sys_exec,
    sys_ps
)


def test_file_create():
    path = "/integration1.txt"

    if fs.get_file_info(path):
        fs.delete_file(path)

    result = sys_create_file(path, "hello", "admin")

    assert result > 0
    print("[PASS] создание файла через syscall")


def test_file_read():
    path = "/integration2.txt"

    if fs.get_file_info(path):
        fs.delete_file(path)

    sys_create_file(path, "integration", "admin")
    content = sys_read_file(path, "admin")

    assert content == "integration"
    print("[PASS] чтение файла через syscall")


def test_duplicate_file():
    path = "/integration3.txt"

    if fs.get_file_info(path):
        fs.delete_file(path)

    sys_create_file(path, "first", "admin")
    result = sys_create_file(path, "second", "admin")

    assert result == -1
    print("[PASS] дубликат файла отклонён")


def test_permission_delete():
    path = "/admin_integration.txt"

    if fs.get_file_info(path):
        fs.delete_file(path)

    sys_create_file(path, "secret", "admin")
    result = sys_delete_file(path, "user")

    assert result is False
    print("[PASS] user не может удалить файл admin")


def test_process_create():
    pid = sys_exec("integration_app", "admin")

    assert pid > 0

    processes = sys_ps("admin")
    process = next((p for p in processes if p["id"] == pid), None)

    assert process is not None
    print("[PASS] запуск процесса через syscall")


def test_process_terminate():
    pid = scheduler.create_process("integration_temp", "admin", 10)

    assert pid > 0

    result = scheduler.terminate_process(pid)

    assert result is True
    assert scheduler.get_process(pid) is None
    print("[PASS] завершение процесса")


def test_memory_limit():
    before = kernel_instance.memory_used

    pid = scheduler.create_process(
        "integration_huge",
        "admin",
        5000
    )

    assert pid == -1
    assert kernel_instance.memory_used == before
    print("[PASS] ограничение памяти работает")


if __name__ == "__main__":
    test_file_create()
    test_file_read()
    test_duplicate_file()
    test_permission_delete()
    test_process_create()
    test_process_terminate()
    test_memory_limit()

    print("Все интеграционные тесты пройдены")