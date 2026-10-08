import sys
from pathlib import Path

root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root))
sys.path.insert(0, str(root / "src"))

from src import db, fs, scheduler, syscalls
from src.auth import register_user
from src.kernel import kernel_instance


def test_login():
    assert syscalls.sys_login("admin", "secret") is True
    print("[PASS] ST-01: вход администратора")


def test_whoami():
    assert syscalls.sys_whoami() == "admin"
    print("[PASS] ST-02: текущий пользователь")


def test_create_file():
    result = syscalls.sys_create_file(
        "/f08_syscalls.txt", "hello", "admin"
    )
    assert result > 0
    print("[PASS] ST-03: создание файла")


def test_duplicate_file():
    result = syscalls.sys_create_file(
        "/f08_syscalls.txt", "again", "admin"
    )
    assert result == -1
    print("[PASS] ST-04: запрет дубликата")


def test_read_file():
    assert syscalls.sys_read_file(
        "/f08_syscalls.txt", "admin"
    ) == "hello"
    print("[PASS] ST-05: чтение файла")


def test_list_files():
    files = syscalls.sys_list_files("/f08_", "admin")
    assert "/f08_syscalls.txt" in files
    print("[PASS] ST-06: список файлов")


def test_delete_denied():
    result = syscalls.sys_delete_file(
        "/f08_syscalls.txt", "day8_test_user"
    )
    assert result is False
    assert fs.get_owner("/f08_syscalls.txt") == "admin"
    print("[PASS] ST-07: запрет удаления чужого файла")


def test_delete_allowed():
    assert syscalls.sys_delete_file(
        "/f08_syscalls.txt", "admin"
    ) is True
    assert fs.get_owner("/f08_syscalls.txt") is None
    print("[PASS] ST-08: удаление файла администратором")


def test_exec_and_ps():
    pid = syscalls.sys_exec("f08_program", "admin")
    assert pid > 0

    processes = syscalls.sys_ps("admin")
    assert any(p["id"] == pid for p in processes)

    print("[PASS] ST-09: запуск и список процессов")
    return pid


def test_kill(pid):
    assert syscalls.sys_kill(pid, "admin") is True
    assert scheduler.get_process(pid) is None
    print("[PASS] ST-10: завершение процесса")


def test_logs():
    logs = syscalls.sys_logs(100)
    names = [log["syscall_name"] for log in logs]

    assert "sys_create_file" in names
    assert "sys_exec" in names
    assert "sys_kill" in names

    print("[PASS] ST-11: журнал системных вызовов")


if __name__ == "__main__":
    db.init_db()

    if not db.execute_select("users", {"login": "day8_test_user"}):
        register_user("day8_test_user", "1234")

    fs.delete_file("/f08_syscalls.txt")

    try:
        test_login()
        test_whoami()
        test_create_file()
        test_duplicate_file()
        test_read_file()
        test_list_files()
        test_delete_denied()
        test_delete_allowed()

        pid = test_exec_and_ps()
        try:
            test_kill(pid)
        finally:
            if scheduler.get_process(pid) is not None:
                scheduler.terminate_process(pid)

        test_logs()

        print("\nВсе 11 функциональных тестов syscalls.py пройдены")
    finally:
        fs.delete_file("/f08_syscalls.txt")
        syscalls.sys_logout()