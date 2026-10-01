class Kernel:
    def __init__(self):
        self.current_user = "guest"
        self.process_counter = 0
        self.memory_used = 0
        self.memory_limit = 1024

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
        return True

    def free_memory(self, size):
        self.memory_used = max(0, self.memory_used - size)

    def memory_info(self):
        return {
            "used": self.memory_used,
            "limit": self.memory_limit,
            "free": self.memory_limit - self.memory_used
        }


kernel_instance = Kernel()