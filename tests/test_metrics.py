import subprocess
import sys
import re
from pathlib import Path

root = Path(__file__).resolve().parent.parent
tests_dir = root / "tests"

test_files = [
    "test_db.py",
    "test_kernel_unit.py",
    "test_auth_unit.py",
    "test_fs_functional.py",
    "test_scheduler_functional.py",
    "test_syscalls_functional.py",
    "test_integration_full.py",
    "test_stress.py"
]

total_passed = 0
total_failed = 0
files_passed = 0
files_failed = 0

print("=== МЕТРИКИ ТЕСТИРОВАНИЯ StudyOS ===")

for filename in test_files:
    path = tests_dir / filename

    if not path.exists():
        print(f"[MISSING] {filename}")
        files_failed += 1
        continue

    result = subprocess.run(
        [sys.executable, "-X", "utf8", str(path)],
        cwd=root,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace"
    )

    output = result.stdout + "\n" + result.stderr

    passed = len(re.findall(r"^\[PASS\]", output, re.MULTILINE))
    failed = len(re.findall(r"^\[FAIL\]", output, re.MULTILINE))

    if result.returncode != 0:
        failed += 1 
        files_failed += 1
        status = "FAIL"
    elif passed == 0:
        files_failed += 1
        status = "NO TESTS"
    else:
        files_passed += 1
        status = "PASS"

    total_passed += passed
    total_failed += failed

    print(f"{filename}: {status}, PASS={passed}, FAIL={failed}")

    if status != "PASS":
        print(output[-1500:])

total = total_passed + total_failed
success_rate = total_passed / total * 100 if total else 0

print("\n=== ИТОГОВЫЕ МЕТРИКИ ===")
print(f"Успешных проверок: {total_passed}")
print(f"Неуспешных проверок: {total_failed}")
print(f"Всего учтённых результатов: {total}")
print(f"Процент успешных проверок: {success_rate:.1f}%")
print(f"Успешных файлов: {files_passed}")
print(f"Проблемных файлов: {files_failed}")

if files_failed:
    sys.exit(1)
