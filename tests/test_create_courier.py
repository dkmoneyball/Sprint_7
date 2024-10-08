import pytest
import requests
from src.utils import generate_random_string, login_courier
from src.config import COURIER_URL  # Импортируем URL для курьера из config.py

@pytest.fixture
def unique_login():
    return generate_random_string()

@pytest.fixture
def create_courier_and_return_login_password():
    # Создаем курьера и возвращаем логин и пароль
    login = generate_random_string()
    password = "1234"
    payload = {
        "login": login,
        "password": password,
        "firstName": "CourierName"
    }
    response = requests.post(COURIER_URL, json=payload)  # Используем COURIER_URL из config
    if response.status_code == 201:
        return login, password
    return None, None

class TestCreateCourier:

    # Проверка успешного создания курьера: статус ответа
    def test_create_courier_status_code(self, unique_login):
        payload = {
            "login": unique_login,
            "password": "1234",
            "firstName": "CourierName"
        }
        response = requests.post(COURIER_URL, json=payload)  # Используем COURIER_URL из config
        assert response.status_code == 201 or response.status_code == 409, f"Ожидался код ответа 201 или 409, но получен {response.status_code}"

    # Проверка успешной авторизации курьера
    def test_courier_login_success(self, create_courier_and_return_login_password):
        login, password = create_courier_and_return_login_password
        assert login is not None and password is not None, "Курьер не был создан."
        courier_id = login_courier(login, password)
        assert courier_id is not None, "Курьер не был авторизован после создания"

    # Проверка на создание курьера с дублирующимся логином: статус ответа
    def test_create_courier_duplicate_status_code(self, create_courier):
        courier_data = create_courier
        payload = {
            "login": courier_data[0],  # Используем тот же логин, чтобы вызвать конфликт
            "password": "1234",
            "firstName": "AnotherCourier"
        }
        response = requests.post(COURIER_URL, json=payload)  # Используем COURIER_URL из config
        assert response.status_code == 409, f"Ожидался код ответа 409, но получен {response.status_code}"

    # Проверка на отсутствие обязательных полей: статус ответа
    @pytest.mark.parametrize("missing_field", ["login", "password", "firstName"])
    def test_create_courier_missing_field_status_code(self, missing_field):
        payload = {
            "login": generate_random_string(),
            "password": "1234",
            "firstName": "CourierName"
        }
        del payload[missing_field]
        response = requests.post(COURIER_URL, json=payload)  # Используем COURIER_URL из config
        assert response.status_code == 400, f"Ожидался код ответа 400, но получен {response.status_code}"
