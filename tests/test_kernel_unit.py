import sys
from pathlib import Path

root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root))
sys.path.insert(0, str(root / "src"))

from src.kernel import Kernel


def new_kernel():
    k = Kernel()
    k.memory_used = 0
    k.memory_limit = 1024
    return k


def test_default_user():
    k = new_kernel()

    assert k.get_user() == "guest"
    print("[PASS] пользователь по умолчанию guest")


def test_set_user():
    k = new_kernel()
    k.set_user("admin")

    assert k.get_user() == "admin"
    print("[PASS] смена текущего пользователя")


def test_allocate_pid():
    k = new_kernel()

    first = k.allocate_pid()
    second = k.allocate_pid()

    assert second == first + 1
    print("[PASS] последовательная выдача PID")


def test_allocate_memory():
    k = new_kernel()

    result = k.allocate_memory(100)

    assert result is True
    assert k.memory_used == 100
    print("[PASS] выделение памяти")


def test_memory_limit():
    k = new_kernel()

    result = k.allocate_memory(2000)

    assert result is False
    assert k.memory_used == 0
    print("[PASS] превышение лимита памяти отклонено")


def test_free_memory():
    k = new_kernel()

    k.allocate_memory(100)
    k.free_memory(40)

    assert k.memory_used == 60
    print("[PASS] освобождение памяти")


def test_memory_not_negative():
    k = new_kernel()

    k.allocate_memory(50)
    k.free_memory(100)

    assert k.memory_used == 0
    print("[PASS] память не становится отрицательной")


def test_memory_info():
    k = new_kernel()

    k.allocate_memory(100)
    info = k.memory_info()

    assert info["used"] == 100
    assert info["limit"] == 1024
    assert info["free"] == 924
    print("[PASS] информация о памяти")


def test_save_memory_state():
    from src import db

    k = new_kernel()
    k.allocate_memory(100)
    k.save_memory_state()

    states = db.execute_select("memory_state")

    assert len(states) >= 1
    assert states[0]["used"] == 100
    print("[PASS] состояние памяти сохранено в БД")


if __name__ == "__main__":
    test_default_user()
    test_set_user()
    test_allocate_pid()
    test_allocate_memory()
    test_memory_limit()
    test_free_memory()
    test_memory_not_negative()
    test_memory_info()
    test_save_memory_state()

    print("\nВсе тесты kernel.py пройдены")