from db import get_connection


def log_syscall(name, arguments, username, status):
    """Записывает системный вызов в журнал."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO syscalls_log
        (syscall_name, arguments, username, status)
        VALUES (?, ?, ?, ?)
        """,
        (name, arguments, username, status)
    )

    conn.commit()
    conn.close()


def sys_echo(message, username="user"):
    """Возвращает переданное сообщение."""
    log_syscall("sys_echo", message, username, "success")
    return message


def sys_get_users(username="user"):
    """Возвращает список пользователей."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id, login, role FROM users")
    users = cursor.fetchall()

    conn.close()

    log_syscall("sys_get_users", "", username, "success")
    return users