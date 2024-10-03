import pytest
import requests

BASE_URL = "https://qa-scooter.praktikum-services.ru/api/v1"

class TestCourierLogin:

    # Проверка успешной авторизации курьера
    def test_login_courier_success(self, create_courier):
        courier_data = create_courier
        payload = {
            "login": courier_data[0],
            "password": courier_data[1]
        }
        response = requests.post(f"{BASE_URL}/courier/login", json=payload)
        assert response.status_code == 200, f"Ожидался код ответа 200, но получен {response.status_code}"
        assert "id" in response.json(), "Ожидалось, что ответ содержит 'id'"

    # Проверка на отсутствие обязательных полей
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_login_courier_missing_field(self, create_courier, missing_field):
        courier_data = create_courier
        payload = {
            "login": courier_data[0],
            "password": courier_data[1]
        }
        del payload[missing_field]
        response = requests.post(f"{BASE_URL}/courier/login", json=payload)
        assert response.status_code == 400, f"Ожидался код ответа 400, но получен {response.status_code}"
        assert "message" in response.json(), "Ожидалось сообщение об ошибке в ответе"

    # Проверка неверного логина или пароля
    def test_login_courier_wrong_credentials(self, create_courier):
        courier_data = create_courier

        # Неверный логин
        payload = {
            "login": "wrong_login",
            "password": courier_data[1]
        }
        response = requests.post(f"{BASE_URL}/courier/login", json=payload)
        assert response.status_code == 404, f"Ожидался код ответа 404, но получен {response.status_code}"
        assert "message" in response.json(), "Ожидалось сообщение об ошибке в ответе"

        # Неверный пароль
        payload = {
            "login": courier_data[0],
            "password": "wrong_password"
        }
        response = requests.post
