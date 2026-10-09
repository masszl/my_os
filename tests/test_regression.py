
import subprocess
import sys
from pathlib import Path

root = Path(__file__).resolve().parent.parent
runner = root / "tests" / "run_all.py"

results = []

print("=== РЕГРЕССИОННОЕ ТЕСТИРОВАНИЕ StudyOS ===")

for attempt in range(1, 4):
    print(f"\n=== ПРОГОН {attempt}/3 ===")

    result = subprocess.run(
        [sys.executable, "-X", "utf8", str(runner)],
        cwd=root,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace"
    )

    print(result.stdout)

    if result.stderr:
        print(result.stderr)

    successful = (
        result.returncode == 0
        and "Файлов с ошибками: 0" in result.stdout
        and "Пропущено файлов: 0" in result.stdout
        and "Всего файлов: 8" in result.stdout
    )

    results.append(successful)

    if successful:
        print(f"[PASS] Прогон {attempt}")
    else:
        print(f"[FAIL] Прогон {attempt}")

print("\n=== ИТОГ РЕГРЕССИИ ===")

for i, success in enumerate(results, 1):
    status = "PASS" if success else "FAIL"
    print(f"Прогон {i}: {status}")

print(f"Успешных прогонов: {sum(results)}/3")

if not all(results):
    sys.exit(1)
