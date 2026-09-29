from db import get_connection


current_user = "guest"


def log_syscall(name, arguments="", username="guest", status="success"):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO syscalls_log
        (syscall_name, arguments, username, status)
        VALUES (?, ?, ?, ?)
        """,
        (name, str(arguments), username, status)
    )

    conn.commit()
    conn.close()


def sys_login(login, password):
    global current_user

    if login == "admin" and password == "admin":
        current_user = "admin"
        log_syscall("sys_login", login, current_user)
        return True

    log_syscall("sys_login", login, current_user, "failed")
    return False


def sys_logout():
    global current_user

    log_syscall("sys_logout", "", current_user)
    current_user = "guest"
    return True


def sys_whoami():
    log_syscall("sys_whoami", "", current_user)
    return current_user


def sys_create_file(path, content):
    log_syscall("sys_create_file", path, current_user)
    return 1


def sys_read_file(path):
    log_syscall("sys_read_file", path, current_user)
    return ""


def sys_delete_file(path):
    log_syscall("sys_delete_file", path, current_user)
    return True


def sys_list_files(path="/"):
    log_syscall("sys_list_files", path, current_user)
    return []


def sys_exec(name):
    log_syscall("sys_exec", name, current_user)
    return 42


def sys_ps():
    log_syscall("sys_ps", "", current_user)
    return []


def sys_kill(pid):
    log_syscall("sys_kill", pid, current_user)
    return True


def sys_mem_alloc(size):
    log_syscall("sys_mem_alloc", size, current_user)
    return size


def sys_logs(limit):
    log_syscall("sys_logs", limit, current_user)
    return []


def sys_shutdown():
    log_syscall("sys_shutdown", "", current_user)
    return True


if __name__ == "__main__":
    print("Проверка системных вызовов")

    print("login:", sys_login("admin", "admin"))
    print("whoami:", sys_whoami())
    print("create:", sys_create_file("/test.txt", "Hello"))
    print("ps:", sys_ps())