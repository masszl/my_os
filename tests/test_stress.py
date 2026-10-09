import sys
from pathlib import Path

root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root))
sys.path.insert(0, str(root / "src"))

from src import db, scheduler, fs
from src.kernel import kernel_instance


def test_ten_processes():
    db.init_db()

    pids = []

    try:
        for i in range(10):
            pid = scheduler.create_process(
                f"stress_app_{i}",
                "admin",
                10
            )

            assert pid > 0, f"Не удалось создать процесс {i}"
            pids.append(pid)

        processes = scheduler.list_processes()
        active = [p for p in processes if p["id"] in pids]

        assert len(active) == 10

        print("[PASS] ST-01: 10 процессов успешно созданы")

    finally:
        for pid in pids:
            scheduler.terminate_process(pid)


def test_memory_limit():
    from src.kernel import kernel_instance

    before = kernel_instance.memory_used
    limit = kernel_instance.memory_limit
    requested = limit - before + 1

    assert requested > 0, "Память уже превышает лимит"

    pid = scheduler.create_process(
        "stress_memory_overflow",
        "admin",
        requested
    )

    assert pid == -1, "Система разрешила превышение лимита памяти"
    assert kernel_instance.memory_used == before

    print("[PASS] ST-02: превышение лимита памяти отклонено")



def test_fifty_files():
    prefix = "/stress_day9_"
    paths = [f"{prefix}{i}.txt" for i in range(50)]

    try:
        for path in paths:
            if fs.get_file_info(path) is not None:
                fs.delete_file(path)

        for i, path in enumerate(paths):
            result = fs.create_file(
                path,
                f"Stress test content {i}",
                "admin"
            )

            assert result > 0, f"Ошибка создания {path}"

        for i, path in enumerate(paths):
            content = fs.read_file(path)

            assert content == f"Stress test content {i}", (
                f"Ошибка чтения {path}"
            )

        print("[PASS] ST-03: 50 файлов созданы и прочитаны")

    finally:
        for path in paths:
            if fs.get_file_info(path) is not None:
                fs.delete_file(path)


def test_twenty_users():
    from src.auth import register_user, authenticate

    db.init_db()

    for i in range(20):
        login = f"stress_day9_user_{i}"
        password = f"test_password_{i}"

        existing = db.execute_select("users", {"login": login})

        if not existing:
            register_user(login, password, "user")

        account = authenticate(login, password)

        assert account is not None, f"Ошибка входа: {login}"
        assert account["role"] == "user"

    print("[PASS] ST-04: 20 пользователей зарегистрированы и проверены")





if __name__ == "__main__":
    test_ten_processes()
    test_memory_limit()
    test_fifty_files()
    test_twenty_users()