import pytest
import requests
import random
import string

BASE_URL = "https://qa-scooter.praktikum-services.ru/api/v1"

# Функция для генерации случайного логина
def generate_random_string(length=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))

# Функция для авторизации курьера
def login_courier(login, password):
    payload = {
        "login": login,
        "password": password
    }
    response = requests.post(f"{BASE_URL}/courier/login", json=payload)
    if response.status_code == 200:
        return response.json().get("id")
    return None

@pytest.fixture
def create_courier():
    # Генерация уникальных данных курьера
    login = generate_random_string()
    password = generate_random_string()
    first_name = generate_random_string()

    # Регистрируем нового курьера
    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }
    response = requests.post(f"{BASE_URL}/courier", json=payload)
    assert response.status_code == 201, f"Ошибка при создании курьера. Ожидался код ответа 201, но получен {response.status_code}"

    # Возвращаем данные о курьере для использования в тестах
    yield login, password, first_name

    # После завершения теста авторизуем курьера и удаляем его
    courier_id = login_courier(login, password)
    if courier_id:
        delete_response = requests.delete(f"{BASE_URL}/courier/{courier_id}")
        assert delete_response.status_code == 200, f"Не удалось удалить курьера, код ответа: {delete_response.status_code}"
    else:
        print(f"Ошибка: не удалось найти ID курьера для удаления. Логин: {login}")

@pytest.fixture
def create_courier_and_login():
    # Генерация уникальных данных курьера
    login = generate_random_string()
    password = generate_random_string()
    first_name = generate_random_string()

    # Регистрируем нового курьера
    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }
    response = requests.post(f"{BASE_URL}/courier", json=payload)
    assert response.status_code == 201, f"Ошибка при создании курьера. Ожидался код ответа 201, но получен {response.status_code}"

    # Авторизуем курьера
    courier_id = login_courier(login, password)
    assert courier_id is not None, "Ошибка при авторизации курьера."

    # Возвращаем данные о курьере и его id для использования в тестах
    yield (login, password, first_name), courier_id

    # После завершения теста удаляем созданного курьера
    delete_response = requests.delete(f"{BASE_URL}/courier/{courier_id}")
    assert delete_response.status_code == 200, f"Не удалось удалить курьера, код ответа: {delete_response.status_code}"
