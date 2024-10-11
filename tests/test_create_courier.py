import pytest
import requests
from src.utils import login_courier
from src.config import COURIER_URL  # Используем URL из файла config.py


class TestCreateCourier:

    # Проверка успешного создания курьера: статус ответа
    def test_create_courier_status_code(self, courier_payload):
        payload = courier_payload
        response = requests.post(COURIER_URL, json=payload)  # Используем COURIER_URL из config
        assert response.status_code == 201 or response.status_code == 409, f"Ожидался код ответа 201 или 409, но получен {response.status_code}"

    # Проверка успешной авторизации курьера: статус ответа
    def test_courier_login_status_code(self, create_courier):
        login, password, _ = create_courier
        courier_id = login_courier(login, password)
        assert courier_id is not None, "Курьер не был авторизован после создания"

    # Проверка успешной авторизации курьера: наличие id в ответе
    def test_courier_login_contains_id(self, create_courier):
        login, password, _ = create_courier
        courier_id = login_courier(login, password)
        assert courier_id is not None, "Курьер не был авторизован после создания"

    # Проверка на создание курьера с дублирующимся логином: статус ответа
    def test_create_courier_duplicate_status_code(self, create_courier):
        login, password, _ = create_courier
        payload = {
            "login": login,  # Используем тот же логин, чтобы вызвать конфликт
            "password": "1234",
            "firstName": "AnotherCourier"
        }
        response = requests.post(COURIER_URL, json=payload)  # Используем COURIER_URL из config
        assert response.status_code == 409, f"Ожидался код ответа 409, но получен {response.status_code}"

    # Проверка на отсутствие обязательных полей: статус ответа
    @pytest.mark.parametrize("missing_field", ["login", "password", "firstName"])
    def test_create_courier_missing_field_status_code(self, courier_payload, missing_field):
        payload = courier_payload
        del payload[missing_field]
        response = requests.post(COURIER_URL, json=payload)  # Используем COURIER_URL из config
        assert response.status_code == 400, f"Ожидался код ответа 400, но получен {response.status_code}"
