import db


class Kernel:
    def __init__(self):
        self.current_user = "guest"
        self.memory_used = 0
        self.memory_limit = 1024

        processes = db.execute_select("processes")

        if processes:
            self.process_counter = max(p["id"] for p in processes)
        else:
            self.process_counter = 0

        self.load_memory_state()

    def set_user(self, login):
        self.current_user = login

    def get_user(self):
        return self.current_user

    def allocate_pid(self):
        self.process_counter += 1
        return self.process_counter

    def allocate_memory(self, size):
        if self.memory_used + size > self.memory_limit:
            return False

        self.memory_used += size
        self.save_memory_state()
        return True

    def free_memory(self, size):
        self.memory_used = max(0, self.memory_used - size)
        self.save_memory_state()

    def memory_info(self):
        return {
            "used": self.memory_used,
            "limit": self.memory_limit,
            "free": self.memory_limit - self.memory_used
        }

    def save_memory_state(self):
        states = db.execute_select("memory_state")

        if states:
            db.execute_update(
                "memory_state",
                {
                    "used": self.memory_used,
                    "memory_limit": self.memory_limit
                },
                {"id": states[0]["id"]}
            )
        else:
            db.execute_insert(
                "memory_state",
                {
                    "used": self.memory_used,
                    "memory_limit": self.memory_limit
                }
            )

    def load_memory_state(self):
        states = db.execute_select("memory_state")

        if states:
            self.memory_used = states[0]["used"]
            self.memory_limit = states[0]["memory_limit"]


kernel_instance = Kernel()