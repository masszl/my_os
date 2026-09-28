from db import init_db
from syscalls import sys_echo, sys_get_users


def show_help():
    print("\nДоступные команды:")
    print("help - список команд")
    print("echo - вывести сообщение")
    print("users - показать пользователей")
    print("exit - выйти из MyOS")


def main():
    init_db()

    print("====================")
    print("   Добро пожаловать")
    print("       в MyOS")
    print("====================")

    while True:
        command = input("\nMyOS> ").strip()

        if command == "help":
            show_help()

        elif command.startswith("echo "):
            message = command[5:]
            print(sys_echo(message))

        elif command == "users":
            users = sys_get_users()

            if users:
                for user in users:
                    print(user)
            else:
                print("Пользователей пока нет")

        elif command == "exit":
            print("Завершение работы MyOS")
            break

        else:
            print("Неизвестная команда. Введите help.")


if __name__ == "__main__":
    main()