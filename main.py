import json
from prettytable import PrettyTable

# Функция для сохранения данных в JSON-файл
def save_data(data):
    with open("users.json", "w") as f:
        json.dump(data, f, indent=4)

# Функция для загрузки данных из JSON-файла
def load_data():
    try:
        with open("users.json", "r") as f:
            data = json.load(f)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        data = []
    return data

# Функция для авторизации пользователя
def login():
    data = load_data()
    login = input("Введите логин: ")
    password = input("Введите пароль: ")

    user = next((user for user in data if user["login"] == login and user["password"] == password), None)

    if user:
        if user["role"] == 1:
            print("\033[95m\033[1mВы вошли как Администратор\033[0m")  # Сиреневый цвет и жирный текст
            print("\033[94m\033[1m***Админ панель***\033[0m")  # Синий цвет и жирный текст
            admin_menu()
        else:
            print("Вы вошли как Пользователь")
    else:
        print("Ошибка авторизации. Проверьте логин и пароль.")

def admin_menu():
    while True:
        print("\033[96m1.\033[0m Посмотреть данные пользователей")
        print("\033[96m2.\033[0m Добавить нового пользователя")
        print("\033[96m3.\033[0m Удалить пользователя")
        print("\033[96m4.\033[0m Изменить данные пользователя")
        print("\033[96m5.\033[0m Отключить пользователя")
        print("\033[96m6.\033[0m Просмотр статистики")
        print("\033[96m7.\033[0m Выход")
        choice = input("Выберите действие: ")

        if choice == "1":
            view_users()
        elif choice == "2":
            add_user()
        elif choice == "3":
            delete_user()
        elif choice == "4":
            change_user()
        elif choice == "5":
            disconnect_user()
        elif choice == "6":
            view_stat()
        elif choice == "7":
            break
        else:
            print("Неверный выбор. Пожалуйста, выберите 1, 2, 3, 4, 5, 6 или 7.")

# Функция для отображения данных всех пользователей с использованием PrettyTable
def view_users():
    data = load_data()
    if not data:
        print("Нет зарегистрированных пользователей.")
    else:
        table = PrettyTable()
        table.field_names = ["ID", "Фамилия", "Имя", "Логин", "Роль"]

        for user in data:
            role = "Администратор" if user["role"] == 1 else "Пользователь"
            table.add_row([user["id"], user["surname"], user["name"], user["login"], role])

        print(table)

def add_user():
    data = load_data()

    while True:
        last_name = input("Введите фамилию: ")
        first_name = input("Введите имя: ")

        while True:
            login = input("Введите логин: ")
            if not login:
                print("Логин не может быть пустым. Пожалуйста, введите логин.")
            elif any(user["login"] == login for user in data):
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

        print("Пожалуйста, проверьте введенные данные:")
        print(f"Фамилия: {last_name}")
        print(f"Имя: {first_name}")
        print(f"Логин: {login}")
        print(f"Пароль: {password}")
        print(f"Роль: {'Администратор' if role == 1 else 'Пользователь'}")

        confirmation = input("Все ли верно? (да/нет): ")
        if confirmation.lower() == "да":
            break

    user_id = len(data) + 1
    user = {
        "id": user_id,
        "surname": last_name,
        "name": first_name,
        "login": login,
        "password": password,
        "role": role
    }

    data.append(user)
    save_data(data)
    print("Пользователь успешно добавлен в базу данных!")
    view_users()

def delete_user():
    view_users()
    data = load_data()
    login_to_delete = input("Введите \033[4mлогин\033[0m пользователя, которого вы хотите удалить: ")

    user_to_delete = None
    for user in data:
        if user["login"] == login_to_delete:
            user_to_delete = user
            break

    if user_to_delete:
        data.remove(user_to_delete)
        save_data(data)
        print(f"Пользователь с логином '{login_to_delete}' успешно удален.")
    else:
        print(f"Пользователь с логином '{login_to_delete}' не найден.")


def change_user():
    view_users()
    data = load_data()
    login_to_change = input("Введите логин пользователя, данные которого вы хотите изменить: ")

    user_to_change = next((user for user in data if user["login"] == login_to_change), None)

    if user_to_change:
        print("Введите новые данные для пользователя (оставьте поле пустым, чтобы оставить без изменений):")
        new_last_name = input(f"Новая фамилия ({user_to_change['surname']}): ")
        new_first_name = input(f"Новое имя ({user_to_change['name']}): ")
        new_login = input(f"Новый логин ({user_to_change['login']}): ")
        new_password = input(f"Новый пароль ({user_to_change['password']}): ")

        if new_last_name:
            user_to_change['surname'] = new_last_name
        if new_first_name:
            user_to_change['name'] = new_first_name
        if new_login:
            if any(user["login"] == new_login for user in data):
                print("Пользователь с таким логином уже существует.")
            else:
                user_to_change['login'] = new_login
        if new_password:
            user_to_change['password'] = new_password

        save_data(data)
        print(f"Данные пользователя с логином '{login_to_change}' успешно изменены.")
    else:
        print(f"Пользователь с логином '{login_to_change}' не найден.")

def disconnect_user():
    # Add code to disconnect a user from the database
    return

def view_stat():
    return

# Основной цикл программы
while True:
    print("1. Вход")
    print("2. Выход")
    choice = input("Выберите действие: ")

    if choice == "1":
        login()
    elif choice == "2":
        break
    else:
        print("Неверный выбор. Пожалуйста, выберите 1 или 2.")