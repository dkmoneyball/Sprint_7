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
