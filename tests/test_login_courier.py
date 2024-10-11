import pytest
import requests
from src.config import COURIER_LOGIN_URL  # Импортируем URL для авторизации курьера из config.py


class TestCourierLogin:

    # Проверка успешной авторизации курьера - проверка статуса кода
    def test_login_courier_status_code(self, create_courier):
        courier_data = create_courier
        payload = {
            "login": courier_data[0],
            "password": courier_data[1]
        }
        response = requests.post(COURIER_LOGIN_URL, json=payload)  # Используем COURIER_LOGIN_URL из config
        assert response.status_code == 200, f"Ожидался код ответа 200, но получен {response.status_code}"

    # Проверка успешной авторизации курьера - проверка наличия id в ответе
    def test_login_courier_contains_id(self, create_courier):
        courier_data = create_courier
        payload = {
            "login": courier_data[0],
            "password": courier_data[1]
        }
        response = requests.post(COURIER_LOGIN_URL, json=payload)  # Используем COURIER_LOGIN_URL из config
        assert response.status_code == 200, f"Ожидался код ответа 200, но получен {response.status_code}"
        assert "id" in response.json(), "Ожидалось, что ответ содержит 'id'"

    # Проверка на отсутствие обязательных полей - проверка статуса кода
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_login_courier_missing_field_status_code(self, create_courier, missing_field):
        courier_data = create_courier
        payload = {
            "login": courier_data[0],
            "password": courier_data[1]
        }
        del payload[missing_field]
        response = requests.post(COURIER_LOGIN_URL, json=payload)  # Используем COURIER_LOGIN_URL из config
        assert response.status_code == 400, f"Ожидался код ответа 400, но получен {response.status_code}"

    # Проверка на отсутствие обязательных полей - проверка наличия сообщения об ошибке
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_login_courier_missing_field_contains_message(self, create_courier, missing_field):
        courier_data = create_courier
        payload = {
            "login": courier_data[0],
            "password": courier_data[1]
        }
        del payload[missing_field]
        response = requests.post(COURIER_LOGIN_URL, json=payload)  # Используем COURIER_LOGIN_URL из config
        # Проверка кода ответа
        assert response.status_code == 400, f"Ожидался код ответа 400, но получен {response.status_code}"
        # Проверка наличия сообщения об ошибке
        assert "message" in response.json(), "Ожидалось сообщение об ошибке в ответе"

    # Проверка неверного логина - проверка статуса кода
    def test_login_courier_wrong_login_status_code(self, create_courier):
        courier_data = create_courier
        payload = {
            "login": "wrong_login",
            "password": courier_data[1]
        }
        response = requests.post(COURIER_LOGIN_URL, json=payload)  # Используем COURIER_LOGIN_URL из config
        assert response.status_code == 404, f"Ожидался код ответа 404, но получен {response.status_code}"

    # Проверка неверного логина - проверка наличия сообщения об ошибке
    def test_login_courier_wrong_login_contains_message(self, create_courier):
        courier_data = create_courier
        payload = {
            "login": "wrong_login",
            "password": courier_data[1]
        }
        response = requests.post(COURIER_LOGIN_URL, json=payload)  # Используем COURIER_LOGIN_URL из config
        assert response.status_code == 404, f"Ожидался код ответа 404, но получен {response.status_code}"
        assert "message" in response.json(), "Ожидалось сообщение об ошибке в ответе"

    # Проверка неверного пароля - проверка статуса кода
    def test_login_courier_wrong_password_status_code(self, create_courier):
        courier_data = create_courier
        payload = {
            "login": courier_data[0],
            "password": "wrong_password"
        }
        response = requests.post(COURIER_LOGIN_URL, json=payload)  # Используем COURIER_LOGIN_URL из config
        assert response.status_code == 404, f"Ожидался код ответа 404, но получен {response.status_code}"

    # Проверка неверного пароля - проверка наличия сообщения об ошибке
    def test_login_courier_wrong_password_contains_message(self, create_courier):
        courier_data = create_courier
        payload = {
            "login": courier_data[0],
            "password": "wrong_password"
        }
        response = requests.post(COURIER_LOGIN_URL, json=payload)  # Используем COURIER_LOGIN_URL из config
        assert response.status_code == 404, f"Ожидался код ответа 404, но получен {response.status_code}"
        assert "message" in response.json(), "Ожидалось сообщение об ошибке в ответе"
