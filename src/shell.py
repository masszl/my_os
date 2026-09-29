from db import init_db
import syscalls


def show_help():
    print("\nДоступные команды:")
    print("help    - список команд")
    print("whoami  - текущий пользователь")
    print("login   - войти в систему")
    print("create  - создать файл")
    print("ls      - список файлов")
    print("ps      - список процессов")
    print("exit    - выйти из MyOS")


def main():
    init_db()

    print("====================")
    print("       StudyOS")
    print("====================")
    print("Введите help для просмотра команд.")

    while True:
        command = input(f"{syscalls.current_user}@studyos> ").strip()

        if command == "help":
            show_help()

        elif command == "whoami":
            print(syscalls.sys_whoami())

        elif command == "login":
            login = input("Логин: ")
            password = input("Пароль: ")

            if syscalls.sys_login(login, password):
                print("Вход выполнен")
            else:
                print("Неверный логин или пароль")

        elif command == "create":
            path = input("Путь к файлу: ")
            content = input("Содержимое: ")

            file_id = syscalls.sys_create_file(path, content)
            print("Файл создан. ID:", file_id)

        elif command == "ls":
            files = syscalls.sys_list_files("/")

            if files:
                for file in files:
                    print(file)
            else:
                print("Файлов пока нет")

        elif command == "ps":
            processes = syscalls.sys_ps()

            if processes:
                for process in processes:
                    print(process)
            else:
                print("Процессов пока нет")

        elif command == "exit":
            print("Завершение работы StudyOS")
            break

        else:
            print("Неизвестная команда. Введите help.")


if __name__ == "__main__":
    main()