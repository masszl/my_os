import sqlite3
from pathlib import Path

DB_PATH = Path("db/os.sqlite")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    DB_PATH.parent.mkdir(exist_ok=True)

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            login TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS processes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            state TEXT NOT NULL,
            owner TEXT NOT NULL,
            memory INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            path TEXT UNIQUE NOT NULL,
            content TEXT,
            owner TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS syscalls_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            syscall_name TEXT NOT NULL,
            arguments TEXT,
            username TEXT,
            status TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)


    cursor.execute("""
     CREATE TABLE IF NOT EXISTS memory_state (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        used INTEGER DEFAULT 0,
        "limit" INTEGER DEFAULT 1024
    )
""")

    conn.commit()
    conn.close()


def execute_insert(table, data):
    keys = ", ".join(data.keys())
    placeholders = ", ".join(["?"] * len(data))

    sql = f"INSERT INTO {table} ({keys}) VALUES ({placeholders})"

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(sql, tuple(data.values()))
    conn.commit()

    last_id = cursor.lastrowid
    conn.close()

    return last_id


def execute_select(table, conditions=None):
    sql = f"SELECT * FROM {table}"
    params = ()

    if conditions:
        where = " AND ".join([f"{key} = ?" for key in conditions.keys()])
        sql += f" WHERE {where}"
        params = tuple(conditions.values())

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(sql, params)

    rows = cursor.fetchall()
    result = [dict(row) for row in rows]

    conn.close()

    return result


def execute_update(table, data, conditions):
    set_clause = ", ".join([f"{key} = ?" for key in data.keys()])
    where_clause = " AND ".join(
        [f"{key} = ?" for key in conditions.keys()]
    )

    sql = f"UPDATE {table} SET {set_clause} WHERE {where_clause}"

    params = tuple(data.values()) + tuple(conditions.values())

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(sql, params)
    conn.commit()
    conn.close()


def execute_delete(table, conditions):
    where_clause = " AND ".join(
        [f"{key} = ?" for key in conditions.keys()]
    )

    sql = f"DELETE FROM {table} WHERE {where_clause}"

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(sql, tuple(conditions.values()))
    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()
    print("База данных создана успешно")