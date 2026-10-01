Отчёт по дню 4

 Что сделано

- Расширен db.py: добавлены execute_insert, execute_select, execute_update, execute_delete.
- Создан kernel.py с классом Kernel и шестью методами.
- Создан auth.py с функциями hash_password, register_user, authenticate, check_permission.
- Обновлён syscalls.py: sys_login, sys_whoami, sys_delete_file, sys_kill используют реальные модули.
- Обновлён shell.py: команды login и mem работают.
- Написаны тесты test_kernel.py и test_auth.py.

 Проверки

- Записи в syscalls_log: sys_login, sys_whoami, sys_delete_file, sys_kill.
- Пароль в базе хранится в виде хэша длиной 64 символа.
- Права разграничены: admin может всё, user — нет.
- Отладка в VS Code: скриншот сохранён.

 Замечания

- Пустой пароль допускается. В следующих итерациях следует добавить валидацию.