import db

try:
    from src.kernel import kernel_instance
except ModuleNotFoundError:
    from kernel import kernel_instance


def create_process(name, owner, memory_size=10):
    if not kernel_instance.allocate_memory(memory_size):
        return -1

    pid = kernel_instance.allocate_pid()

    db.execute_insert(
        "processes",
        {
            "id": pid,
            "name": name,
            "state": "ready",
            "owner": owner,
            "memory": memory_size
        }
    )

    return pid


def list_processes():
    return db.execute_select("processes")


def get_process(pid):
    processes = db.execute_select("processes", {"id": pid})

    if not processes:
        return None

    return processes[0]


def terminate_process(pid):
    process = get_process(pid)

    if not process:
        return False

    kernel_instance.free_memory(process["memory"])
    db.execute_delete("processes", {"id": pid})

    return True


def schedule_round_robin():
    processes = db.execute_select("processes")

    if not processes:
        return None

    for process in processes:
        db.execute_update(
            "processes",
            {"state": "ready"},
            {"id": process["id"]}
        )

    first = processes[0]

    db.execute_update(
        "processes",
        {"state": "running"},
        {"id": first["id"]}
    )

    return get_process(first["id"])


def process_count():
    return len(list_processes())