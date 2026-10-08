import sys
from pathlib import Path

root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root))
sys.path.insert(0, str(root / "src"))

from src import db, scheduler
from src.kernel import kernel_instance


def test_create_process():
    pid = scheduler.create_process("f08_app", "admin")
    assert pid > 0
    print("[PASS] FT-11: создание процесса")
    return pid


def test_memory_limit():
    before = kernel_instance.memory_used
    pid = scheduler.create_process("f08_huge", "admin", 5000)
    assert pid == -1
    assert kernel_instance.memory_used == before
    print("[PASS] FT-12: ограничение памяти")


def test_list_processes(pid):
    processes = scheduler.list_processes()
    assert any(p["id"] == pid for p in processes)
    print("[PASS] FT-13: список процессов")


def test_get_process(pid):
    process = scheduler.get_process(pid)
    assert process is not None
    assert process["name"] == "f08_app"
    print("[PASS] FT-14: получение процесса")


def test_missing_process():
    assert scheduler.get_process(99999) is None
    print("[PASS] FT-15: отсутствующий PID")


def test_free_memory():
    before = kernel_instance.memory_used
    pid = scheduler.create_process("f08_memory", "admin", 50)
    assert pid > 0

    assert kernel_instance.memory_used == before + 50
    assert scheduler.terminate_process(pid) is True
    assert kernel_instance.memory_used == before

    print("[PASS] FT-16: освобождение памяти")


def test_terminate_missing():
    assert scheduler.terminate_process(99999) is False
    print("[PASS] FT-17: завершение отсутствующего процесса")


def test_round_robin():
    pid1 = scheduler.create_process("f08_rr1", "admin")
    pid2 = scheduler.create_process("f08_rr2", "admin")

    assert pid1 > 0
    assert pid2 > 0

    process = scheduler.schedule_round_robin()

    assert process is not None
    assert process["state"] == "running"

    print("[PASS] FT-18: Round Robin")

    scheduler.terminate_process(pid1)
    scheduler.terminate_process(pid2)


def test_process_count():
    assert scheduler.process_count() == len(scheduler.list_processes())
    print("[PASS] FT-19: количество процессов")


if __name__ == "__main__":
    db.init_db()

    pid = test_create_process()

    try:
        test_memory_limit()
        test_list_processes(pid)
        test_get_process(pid)
        test_missing_process()
        test_free_memory()
        test_terminate_missing()
        test_round_robin()
        test_process_count()

        print("\nВсе функциональные тесты scheduler.py пройдены")
    finally:
        scheduler.terminate_process(pid)