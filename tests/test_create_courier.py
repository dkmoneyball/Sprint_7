import pytest
import requests
from .conftest import login_courier, generate_random_string  # Используем относительный импорт

BASE_URL = "https://qa-scooter.praktikum-services.ru/api/v1"


class TestCreateCourier:

    # Проверка успешного создания курьера
    def test_create_courier_success(self):
        # Используем уникальный логин для каждого теста
        unique_login = generate_random_string()
        payload = {
            "login": unique_login,
            "password": "1234",
            "firstName": "CourierName"
        }
        response = requests.post(f"{BASE_URL}/courier", json=payload)

        # Проверяем, что курьер успешно создан
        assert response.status_code == 201, f"Ожидался код ответа 201, но получен {response.status_code}"
        response_data = response.json()
        assert response_data.get("ok") is True, "Ожидалось, что ответ содержит 'ok': true"

        # Проверяем, что курьер успешно авторизован
        courier_id = login_courier(unique_login, "1234")
        assert courier_id is not None, "Курьер не был авторизован после создания"

    # Проверка на создание курьера с дублирующимся логином
    def test_create_courier_duplicate(self, create_courier):
        courier_data = create_courier
        payload = {
            "login": courier_data[0],  # Используем тот же логин, чтобы вызвать конфликт
            "password": "1234",
            "firstName": "AnotherCourier"
        }
        response = requests.post(f"{BASE_URL}/courier", json=payload)
        assert response.status_code == 409, f"Ожидался код ответа 409, но получен {response.status_code}"
        assert "message" in response.json(), "Ожидалось сообщение об ошибке в ответе"

    # Проверка на отсутствие обязательных полей
    @pytest.mark.parametrize("missing_field", ["login", "password", "firstName"])
    def test_create_courier_missing_field(self, missing_field):
        payload = {
            "login": generate_random_string(),  # Используем уникальный логин
            "password": "1234",
            "firstName": "CourierName"
        }
        del payload[missing_field]
        response = requests.post(f"{BASE_URL}/courier", json=payload)
        assert response.status_code == 400, f"Ожидался код ответа 400, но получен {response.status_code}"
        assert "message" in response.json(), "Ожидалось сообщение об ошибке в ответе"
