
import sys
import sqlite3
import tempfile
from pathlib import Path

root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root))
sys.path.insert(0, str(root / "src"))

from src import db


def test_first_start():
    original_path = db.DB_PATH

    with tempfile.TemporaryDirectory() as temp_dir:
        db.DB_PATH = Path(temp_dir) / "os.sqlite"

        try:
            db.init_db()

            assert db.DB_PATH.exists()

            conn = sqlite3.connect(db.DB_PATH)
            try:
                tables = {
                    row[0]
                    for row in conn.execute(
                        "SELECT name FROM sqlite_master WHERE type='table'"
                    )
                }
            finally:
                conn.close()

            required = {
                "users",
                "processes",
                "files",
                "syscalls_log",
                "memory_state"
            }

            assert required.issubset(tables)

            print("[PASS] SS-01: база данных успешно создана")
            print("[PASS] Все 5 таблиц StudyOS присутствуют")

        finally:
            db.DB_PATH = original_path


if __name__ == "__main__":
    test_first_start()
