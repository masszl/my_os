from db import init_db
import syscalls
from kernel import kernel_instance


def show_help():
    print("\nДоступные команды:")
    print("help        - список команд")
    print("echo TEXT   - вывести текст")
    print("whoami      - текущий пользователь")
    print("login       - войти в систему")
    print("logout      - выйти из аккаунта")
    print("create      - создать файл")
    print("cat PATH    - прочитать файл")
    print("ls          - список файлов")
    print("delete PATH - удалить файл")
    print("run NAME    - запустить процесс")
    print("ps          - список процессов")
    print("kill PID    - завершить процесс")
    print("mem         - информация о памяти")
    print("logs        - журнал системных вызовов")
    print("exit        - выйти из StudyOS")


def main():
    init_db()

    print("====================")
    print("       StudyOS")
    print("====================")
    print("Введите help для просмотра команд.")

    while True:
        current_user = kernel_instance.get_user()
        command = input(f"{current_user}@studyos:~$ ").strip()

        if not command:
            continue

        parts = command.split(maxsplit=1)
        cmd = parts[0]
        arg = parts[1] if len(parts) > 1 else ""

        if cmd == "help":
            show_help()

        elif cmd == "echo":
            print(arg)

        elif cmd == "whoami":
            print(syscalls.sys_whoami())

        elif cmd == "login":
            login = input("Логин: ")
            password = input("Пароль: ")

            if syscalls.sys_login(login, password, current_user):
                print("Вы вошли как", login)
            else:
                print("Ошибка входа")

        elif cmd == "logout":
            syscalls.sys_logout()
            print("Вы вышли из системы")

        elif cmd == "create":
            path = input("Путь: ")
            content = input("Содержимое: ")

            file_id = syscalls.sys_create_file(
                path,
                content,
                current_user
            )

            if file_id == -1:
                print("Файл с таким путём уже существует")
            else:
                print(f"Создан файл с id={file_id}")

        elif cmd == "cat":
            if not arg:
                print("Укажите путь к файлу")
            else:
                content = syscalls.sys_read_file(arg, current_user)

                if content:
                    print(content)
                else:
                    print("(файл пуст или не существует)")

        elif cmd == "ls":
            files = syscalls.sys_list_files(
                arg or "/",
                current_user
            )

            if not files:
                print("(нет файлов)")
            else:
                for file in files:
                    print(file)

        elif cmd == "delete":
            if not arg:
                print("Укажите путь к файлу")
            else:
                if syscalls.sys_delete_file(arg, current_user):
                    print("Файл удалён")
                else:
                    print("Нет прав на удаление или файл не существует")

        elif cmd == "run":
            if not arg:
                print("Укажите имя программы")
            else:
                pid = syscalls.sys_exec(arg, current_user)

                if pid == -1:
                    print("Не удалось запустить: нет свободной памяти")
                else:
                    print(f"Запущен процесс с PID={pid}")

        elif cmd == "ps":
            processes = syscalls.sys_ps(current_user)

            if not processes:
                print("(нет процессов)")
            else:
                for process in processes:
                    print(process)

        elif cmd == "kill":
            if not arg:
                print("Укажите PID процесса")
            else:
                try:
                    pid = int(arg)
                except ValueError:
                    print("PID должен быть числом")
                    continue

                if syscalls.sys_kill(pid, current_user):
                    print(f"Процесс {pid} завершён")
                else:
                    print(f"Не удалось завершить процесс {pid}")

        elif cmd == "mem":
            info = kernel_instance.memory_info()
            print("Использовано:", info["used"])
            print("Всего:", info["limit"])
            print("Свободно:", info["free"])

        elif cmd == "logs":
            logs = syscalls.sys_logs(10)

            if not logs:
                print("(журнал пуст)")
            else:
                for log in logs:
                    print(log)

        elif cmd == "exit":
            print("Завершение StudyOS")
            break

        else:
            print("Неизвестная команда")


if __name__ == "__main__":
    main()