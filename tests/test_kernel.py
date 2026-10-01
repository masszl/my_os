import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.kernel import kernel_instance


def test_allocate_pid():
    pid1 = kernel_instance.allocate_pid()
    pid2 = kernel_instance.allocate_pid()
    assert pid2 == pid1 + 1
    print(f"[PASS] PID увеличивается: {pid1} -> {pid2}")


def test_allocate_memory():
    result = kernel_instance.allocate_memory(50)
    assert result is True
    print("[PASS] память выделена")


def test_memory_limit():
    result = kernel_instance.allocate_memory(5000)
    assert result is False
    print("[PASS] лимит памяти соблюдается")


def test_free_memory():
    kernel_instance.allocate_memory(100)
    before = kernel_instance.memory_info()["used"]
    kernel_instance.free_memory(100)
    after = kernel_instance.memory_info()["used"]
    assert after == before - 100
    print("[PASS] память освобождена")


if __name__ == "__main__":
    test_allocate_pid()
    test_allocate_memory()
    test_memory_limit()
    test_free_memory()
    print("\nВсе тесты ядра пройдены.")