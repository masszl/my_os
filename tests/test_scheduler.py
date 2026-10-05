import sys
from pathlib import Path

root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root))
sys.path.insert(0, str(root / "src"))

from src import scheduler
from src.kernel import kernel_instance


def test_create_process():
    pid = scheduler.create_process("test_app", "admin", 10)
    assert pid > 0
    print(f"[PASS] процесс создан, PID={pid}")


def test_memory_limits():
    before = kernel_instance.memory_used
    pid = scheduler.create_process("huge", "admin", 2000)

    assert pid == -1
    assert kernel_instance.memory_used == before
    print("[PASS] превышение памяти отклонено")


def test_terminate_frees_memory():
    pid = scheduler.create_process("temp", "admin", 50)
    used_after_create = kernel_instance.memory_used

    result = scheduler.terminate_process(pid)

    assert result is True
    assert kernel_instance.memory_used == used_after_create - 50
    print("[PASS] память освобождена при завершении")


def test_get_process():
    pid = scheduler.create_process("lookup", "admin", 5)
    process = scheduler.get_process(pid)

    assert process is not None
    assert process["name"] == "lookup"
    print("[PASS] получение процесса")


def test_terminate_nonexistent():
    result = scheduler.terminate_process(99999)

    assert result is False
    print("[PASS] завершение несуществующего процесса")


def test_round_robin():
    scheduler.create_process("rr1", "admin", 5)
    scheduler.create_process("rr2", "admin", 5)

    running = scheduler.schedule_round_robin()

    assert running is not None
    assert running["state"] == "running"
    print("[PASS] Round Robin выбирает процесс")


if __name__ == "__main__":
    test_create_process()
    test_memory_limits()
    test_terminate_frees_memory()
    test_get_process()
    test_terminate_nonexistent()
    test_round_robin()

    print("Все тесты планировщика пройдены")