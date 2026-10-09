import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TESTS = ROOT / "tests"

test_files = [
    "test_db.py",
    "test_kernel_unit.py",
    "test_auth_unit.py",
    "test_fs_functional.py",
    "test_scheduler_functional.py",
    "test_syscalls_functional.py",
    "test_integration_full.py"
    "test_stress.py"
]

passed = 0
failed = 0
skipped = 0

print("=== StudyOS: общий запуск тестов ===")

for filename in test_files:
    path = TESTS / filename

    print(f"\n--- {filename} ---")

    if not path.exists():
        print("SKIP: файл не найден")
        skipped += 1
        continue

    result = subprocess.run(
        [sys.executable, str(path)],
        cwd=ROOT,
        capture_output=True,
        text=True
    )

    if result.stdout:
        print(result.stdout)

    if result.stderr:
        print(result.stderr)

    if result.returncode == 0:
        print(f"OK: {filename} завершился без ошибок")
        passed += 1
    else:
        print(f"FAIL: {filename}")
        failed += 1

print("\n=== ИТОГ ===")
print(f"Файлов без ошибок: {passed}")
print(f"Файлов с ошибками: {failed}")
print(f"Пропущено файлов: {skipped}")
print(f"Всего файлов: {len(test_files)}")
