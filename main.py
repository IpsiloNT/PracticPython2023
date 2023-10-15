import json
from prettytable import PrettyTable
from datetime import datetime

# Функция для загрузки данных из JSON-файла
def load_data():
    try:
        with open("users.json", "r") as f:
            data = json.load(f)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        data = []

    for user in data:
        user.setdefault("login_count", 0)
        user.setdefault("last_login_time", None)

    return data

# Функция для сохранения данных в JSON-файл
def save_data(data):
    with open("users.json", "w") as f:
        json.dump(data, f, indent=4)


# Функция для проверки существования пользователя по логину
def check_user_existence(login, data):
    return any(user["login"] == login for user in data)

# Функция для авторизации пользователя
def authenticate(data):
    while True:
        user_login = input("Введите логин: ")
        password = input("Введите пароль: ")

        user = next((user for user in data if user["login"] == user_login and user["password"] == password), None)

        if user:
            if user["status"] == "inactive":
                print("Вы не можете войти, так как вы отключены от системы. Обратитесь к администратору.")
                continue

            # Обновление времени последнего входа
            user["last_login_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            print(f"Вы вошли как {'Администратор' if user['role'] == 1 else 'Пользователь'}")

            # Увеличение счетчика входов для пользователя
            user["login_count"] += 1

            # Сохранение обновленных данных в JSON
            save_data(data)

            if user["role"] == 1:
                admin_menu(data)
            break

        else:
            print("Ошибка авторизации. Проверьте логин и пароль.")

# Функция для отображения данных всех пользователей через PrettyTable
def view_users(data):
    if not data:
        print("Нет зарегистрированных пользователей.")
    else:
        table = PrettyTable()
        table.field_names = ["ID", "Фамилия", "Имя", "Логин", "Пароль", "Роль", "Статус"]

        for user in data:
            role = "Администратор" if user["role"] == 1 else "Пользователь"
            status = "Включен" if user["status"] == "active" else "Отключен"
            table.add_row([user["id"], user["surname"], user["name"], user["login"], user["password"], role, status])
        print(table)

# Функция для добавления нового пользователя
def add_user(data):
    last_name = input("Введите фамилию: ")
    first_name = input("Введите имя: ")

    while True:
        login = input("Введите логин: ")
        if not login:
            print("Логин не может быть пустым. Пожалуйста, введите логин.")
        elif check_user_existence(login, data):
            print("Пользователь с таким логином уже существует. Пожалуйста, выберите другой логин.")
        else:
            break

    while True:
        password = input("Введите пароль: ")
        if len(password) < 6:
            print("Пароль должен содержать как минимум 6 символов. Пожалуйста, введите пароль заново.")
        else:
            break

    while True:
        role = input("Введите роль (0 для пользователя, 1 для администратора): ")
        if role not in ("0", "1"):
            print("Роль должна быть 0 или 1.")
        else:
            role = int(role)
            break

    user_id = len(data) + 1
    user = {
        "id": user_id,
        "surname": last_name,
        "name": first_name,
        "login": login,
        "password": password,
        "role": role,
        "status": "active"
    }

    data.append(user)
    save_data(data)
    print("Пользователь успешно добавлен в базу данных.")
    view_users(data)

# Функция для изменения статуса пользователя
def change_user_status(data):
    while True:
        view_users(data)
        login_to_change_status = input("Введите логин пользователя, статус которого вы хотите изменить (или нажмите Enter для отмены): ")

        if not login_to_change_status:
            break

        user_to_change_status = next((user for user in data if user["login"] == login_to_change_status), None)

        if user_to_change_status:
            if user_to_change_status["status"] == "active":
                user_to_change_status["status"] = "inactive"
                print(f"Статус пользователя с логином '{login_to_change_status}' изменен на 'Отключен'.")
            else:
                user_to_change_status["status"] = "active"
                print(f"Статус пользователя с логином '{login_to_change_status}' изменен на 'Включен'.")
            save_data(data)
        else:
            print(f"Пользователь с логином '{login_to_change_status}' не найден.")

# Функция для удаления пользователя
def delete_user(data):
    view_users(data)
    login_to_delete = input("Введите логин пользователя, которого вы хотите удалить: ")

    user_to_delete = next((user for user in data if user["login"] == login_to_delete), None)

    if user_to_delete:
        data.remove(user_to_delete)
        save_data(data)
        print(f"Пользователь с логином '{login_to_delete}' успешно удален.")
        view_users(data)
    else:
        print(f"Пользователь с логином '{login_to_delete}' не найден.")

# Функция для изменения данных пользователя
def change_user_data(data):
    view_users(data)
    login_to_change = input("Введите логин пользователя, данные которого вы хотите изменить (или нажмите Enter для отмены): ")

    user_to_change = next((user for user in data if user["login"] == login_to_change), None)

    if user_to_change:
        print("Введите новые данные для пользователя (оставьте поле пустым, чтобы оставить без изменений):")
        new_last_name = input(f"Новая фамилия ({user_to_change['surname']}): ")
        new_first_name = input(f"Новое имя ({user_to_change['name']}): ")
        new_login = input(f"Новый логин ({user_to_change['login']}): ")

        while True:
            new_password = input(f"Новый пароль ({user_to_change['password']}): ")
            if new_password and len(new_password) < 6:
                print("Пароль должен содержать как минимум 6 символов.")
            else:
                break

        if new_last_name:
            user_to_change['surname'] = new_last_name
        if new_first_name:
            user_to_change['name'] = new_first_name
        if new_login:
            if check_user_existence(new_login, data):
                print("Пользователь с таким логином уже существует.")
            else:
                user_to_change['login'] = new_login
        if new_password:
            user_to_change['password'] = new_password

        save_data(data)
        print(f"Данные пользователя с логином '{login_to_change}' успешно изменены.")
        view_users(data)
    elif login_to_change:
        print(f"Пользователь с логином '{login_to_change}' не найден.")

# Функция для админ меню
def admin_menu(data):
    while True:
        print("\033[96m1.\033[0m Посмотреть данные пользователей")
        print("\033[96m2.\033[0m Добавить нового пользователя")
        print("\033[96m3.\033[0m Удалить пользователя")
        print("\033[96m4.\033[0m Изменить данные пользователя")
        print("\033[96m5.\033[0m Изменить статус пользователя (включен/отключен)")
        print("\033[96m6.\033[0m Просмотр статистики")
        print("\033[96m7.\033[0m Выход")
        choice = input("Выберите действие: ")

        if choice == "1":
            view_users(data)
        elif choice == "2":
            add_user(data)
        elif choice == "3":
            delete_user(data)
        elif choice == "4":
            change_user_data(data)
        elif choice == "5":
            change_user_status(data)
        elif choice == "6":
            view_stats_menu(data)
        elif choice == "7":
            break
        else:
            print("Неверный выбор. Пожалуйста, выберите 1, 2, 3, 4, 5, 6 или 7.")

def view_work_duration(user_to_view_duration):
    if user_to_view_duration:
        login_time = user_to_view_duration["last_login_time"]
        if login_time:
            login_time = datetime.strptime(login_time, "%Y-%m-%d %H:%M:%S")
            current_time = datetime.now()
            duration = current_time - login_time
            hours, remainder = divmod(duration.total_seconds(), 3600)
            minutes, seconds = divmod(remainder, 60)
            duration_str = f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"
            print(f"Пользователь с логином '{user_to_view_duration['login']}' последний раз вошел в {login_time}, и он был в системе {duration_str}.")
        else:
            print(f"Пользователь с логином '{user_to_view_duration['login']}' еще не входил в систему.")
    else:
        print("Пользователь не найден.")

def view_stats_menu(data):
    while True:
        print("\033[96m1.\033[0m По входам в систему")
        print("\033[96m2.\033[0m По продолжительности работы пользователей")
        print("\033[96m3.\033[0m Выход")
        choice = input("Выберите тип статистики: ")

        if choice == "1":
            # TODO: Реализовать код для просмотра статистики по входам в систему
            pass
        elif choice == "2":
            view_users(data)
            login_to_view_duration = input(
            "Введите логин пользователя для просмотра продолжительности работы (или нажмите Enter для отмены): ")
            user_to_view_duration = next((user for user in data if user["login"] == login_to_view_duration), None)
            view_work_duration(user_to_view_duration)
            pass
        elif choice == "3":
            break
        else:
            print("Неверный выбор. Пожалуйста, выберите 1, 2 или 3.")

# Основной цикл программы
while True:
    print("1. Вход")
    print("2. Выход")
    choice = input("Выберите действие: ")

    if choice == "1":
        data = load_data()
        authenticate(data)
    elif choice == "2":
        break
    else:
        print("Неверный выбор. Пожалуйста, выберите 1 или 2.")
