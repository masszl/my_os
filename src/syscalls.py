from db import get_connection
from auth import authenticate, check_permission
from kernel import kernel_instance
import fs
import scheduler


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


def sys_login(login, password, current_user="guest"):
    log_syscall("sys_login", login, current_user, "check")

    user = authenticate(login, password)

    if user:
        kernel_instance.set_user(user["login"])
        log_syscall("sys_login", login, user["login"], "OK")
        return True

    log_syscall("sys_login", login, current_user, "DENIED")
    return False


def sys_logout():
    user = kernel_instance.get_user()
    log_syscall("sys_logout", "", user, "OK")
    kernel_instance.set_user("guest")
    return True


def sys_whoami():
    user = kernel_instance.get_user()
    log_syscall("sys_whoami", "", user, "OK")
    return user


def sys_create_file(path, content, current_user="guest"):
    log_syscall("sys_create_file", path, current_user, "check")

    file_id = fs.create_file(path, content, current_user)

    if file_id == -1:
        log_syscall("sys_create_file", path, current_user, "EXISTS")
        return -1

    log_syscall("sys_create_file", path, current_user, "OK")
    return file_id


def sys_read_file(path, current_user="guest"):
    log_syscall("sys_read_file", path, current_user, "check")

    content = fs.read_file(path)

    log_syscall("sys_read_file", path, current_user, "OK")
    return content


def sys_list_files(prefix="/", current_user="guest"):
    log_syscall("sys_list_files", prefix, current_user, "OK")
    return fs.list_files(prefix)


def sys_delete_file(path, current_user="guest"):
    log_syscall("sys_delete_file", path, current_user, "check")

    owner = fs.get_owner(path)

    if owner is None:
        log_syscall("sys_delete_file", path, current_user, "NOT_FOUND")
        return False

    if not check_permission(current_user, "delete_file", owner):
        log_syscall("sys_delete_file", path, current_user, "DENIED")
        return False

    fs.delete_file(path)
    log_syscall("sys_delete_file", path, current_user, "OK")
    return True


def sys_exec(name, current_user="guest"):
    log_syscall("sys_exec", name, current_user, "check")

    pid = scheduler.create_process(name, current_user)

    if pid == -1:
        log_syscall("sys_exec", name, current_user, "NO_MEMORY")
        return -1

    log_syscall("sys_exec", name, current_user, "OK")
    return pid


def sys_ps(current_user="guest"):
    log_syscall("sys_ps", "", current_user, "OK")
    return scheduler.list_processes()


def sys_kill(pid, current_user="guest"):
    log_syscall("sys_kill", str(pid), current_user, "check")

    if not check_permission(current_user, "kill"):
        log_syscall("sys_kill", str(pid), current_user, "DENIED")
        return False

    result = scheduler.terminate_process(pid)

    if result:
        log_syscall("sys_kill", str(pid), current_user, "OK")
    else:
        log_syscall("sys_kill", str(pid), current_user, "NOT_FOUND")

    return result


def sys_mem_alloc(size):
    user = kernel_instance.get_user()
    log_syscall("sys_mem_alloc", size, user, "check")

    result = kernel_instance.allocate_memory(size)

    if result:
        log_syscall("sys_mem_alloc", size, user, "OK")
    else:
        log_syscall("sys_mem_alloc", size, user, "NO_MEMORY")

    return result


def sys_logs(limit=20):
    user = kernel_instance.get_user()
    log_syscall("sys_logs", limit, user, "OK")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM syscalls_log ORDER BY id DESC LIMIT ?",
        (limit,)
    )

    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]


def sys_shutdown():
    user = kernel_instance.get_user()
    log_syscall("sys_shutdown", "", user, "OK")
    return True