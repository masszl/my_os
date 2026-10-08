import sys
from pathlib import Path

root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root))
sys.path.insert(0, str(root / "src"))

from src import db, fs, scheduler, syscalls
from src.auth import register_user
from src.kernel import kernel_instance


PREFIX = "/day8_integration_"
TEST_USER = "day8_integration_user"


def prepare():
    db.init_db()

    if not db.execute_select("users", {"login": TEST_USER}):
        register_user(TEST_USER, "1234")

    for path in fs.list_files(PREFIX):
        fs.delete_file(path)


def test_is01_create():
    result = syscalls.sys_create_file(
        PREFIX + "01.txt", "hello", "admin"
    )

    assert result > 0
    assert fs.read_file(PREFIX + "01.txt") == "hello"

    print("[PASS] IS-01: создание файла")


def test_is02_read():
    result = syscalls.sys_read_file(
        PREFIX + "01.txt", "admin"
    )

    assert result == "hello"

    print("[PASS] IS-02: чтение файла")


def test_is03_delete_denied():
    result = syscalls.sys_delete_file(
        PREFIX + "01.txt", TEST_USER
    )

    assert result is False
    assert fs.get_owner(PREFIX + "01.txt") == "admin"

    print("[PASS] IS-03: запрет удаления чужого файла")


def test_is04_run():
    before = kernel_instance.memory_used

    pid = syscalls.sys_exec("day8_editor", "admin")

    assert pid > 0
    assert scheduler.get_process(pid) is not None
    assert kernel_instance.memory_used == before + 10

    print("[PASS] IS-04: запуск процесса")

    return pid


def test_is05_kill(pid):
    process = scheduler.get_process(pid)
    assert process is not None

    before = kernel_instance.memory_used
    memory = process["memory"]

    result = syscalls.sys_kill(pid, "admin")

    assert result is True
    assert scheduler.get_process(pid) is None
    assert kernel_instance.memory_used == before - memory

    print("[PASS] IS-05: завершение процесса")


def test_is06_admin():
    assert syscalls.sys_login("admin", "secret") is True
    assert syscalls.sys_whoami() == "admin"

    path = PREFIX + "admin.txt"

    assert syscalls.sys_create_file(path, "admin data", "admin") > 0
    assert syscalls.sys_read_file(path, "admin") == "admin data"

    pid = syscalls.sys_exec("day8_admin_app", "admin")
    assert pid > 0

    try:
        processes = syscalls.sys_ps("admin")
        assert any(p["id"] == pid for p in processes)
        assert syscalls.sys_kill(pid, "admin") is True
    finally:
        if scheduler.get_process(pid) is not None:
            scheduler.terminate_process(pid)

    print("[PASS] IS-06: сценарий администратора")


def test_is07_user():
    assert syscalls.sys_login(TEST_USER, "1234") is True
    assert syscalls.sys_whoami() == TEST_USER

    own_path = PREFIX + "user.txt"

    assert syscalls.sys_create_file(
        own_path, "user data", TEST_USER
    ) > 0

    assert syscalls.sys_delete_file(
        PREFIX + "admin.txt", TEST_USER
    ) is False

    pid = syscalls.sys_exec("day8_user_app", TEST_USER)
    assert pid > 0

    try:
        assert syscalls.sys_kill(pid, TEST_USER) is False
        assert scheduler.get_process(pid) is not None
    finally:
        scheduler.terminate_process(pid)

    print("[PASS] IS-07: сценарий обычного пользователя")


def test_is08_logs():
    logs = syscalls.sys_logs(100)
    names = [log["syscall_name"] for log in logs]

    assert "sys_create_file" in names
    assert "sys_read_file" in names
    assert "sys_exec" in names
    assert "sys_kill" in names

    print("[PASS] IS-08: журнал системных вызовов")


def test_is09_denied_log():
    logs = syscalls.sys_logs(100)

    denied = [
        log for log in logs
        if log["status"] == "DENIED"
    ]

    assert any(
        log["syscall_name"] == "sys_delete_file"
        for log in denied
    )

    assert any(
        log["syscall_name"] == "sys_kill"
        for log in denied
    )

    print("[PASS] IS-09: журнал отказов")


def test_is10_cleanup():
    path = PREFIX + "cleanup.txt"

    assert syscalls.sys_create_file(path, "temp", "admin") > 0
    assert syscalls.sys_delete_file(path, "admin") is True
    assert fs.get_file_info(path) is None

    before = kernel_instance.memory_used

    pid = syscalls.sys_exec("day8_cleanup", "admin")
    assert pid > 0

    assert syscalls.sys_kill(pid, "admin") is True
    assert scheduler.get_process(pid) is None
    assert kernel_instance.memory_used == before

    print("[PASS] IS-10: очистка ресурсов")


if __name__ == "__main__":
    prepare()

    try:
        test_is01_create()
        test_is02_read()
        test_is03_delete_denied()

        pid = test_is04_run()

        try:
            test_is05_kill(pid)
        finally:
            if scheduler.get_process(pid) is not None:
                scheduler.terminate_process(pid)

        test_is06_admin()
        test_is07_user()
        test_is08_logs()
        test_is09_denied_log()
        test_is10_cleanup()

        print("\nВсе 10 интеграционных тестов пройдены")

    finally:
        for path in fs.list_files(PREFIX):
            fs.delete_file(path)

        syscalls.sys_logout()