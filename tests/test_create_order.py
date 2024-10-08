import pytest
import requests
from src.config import ORDERS_URL  # Импортируем URL для заказов из config.py

# Фикстура для создания заказа
def create_order(courier_id, colors):
    payload = {
        "firstName": "Naruto",
        "lastName": "Uchiha",
        "address": "Konoha, 142 apt.",
        "metroStation": 4,
        "phone": "+7 800 355 35 35",
        "rentTime": 5,
        "deliveryDate": "2020-06-06",
        "comment": "Saske, come back to Konoha",
        "color": colors
    }
    return requests.post(ORDERS_URL, json=payload)  # Используем ORDERS_URL из config

class TestCreateOrder:

    @pytest.mark.parametrize("colors", [
        (["BLACK"]),          # Один цвет
        (["GREY"]),           # Один цвет
        (["BLACK", "GREY"]),  # Оба цвета
        ([])                  # Без указания цвета
    ])
    def test_create_order_status_code(self, create_courier_and_login, colors):
        # Тест проверяет только код ответа
        courier_data, courier_id = create_courier_and_login
        assert courier_id is not None, "Ошибка при авторизации курьера."

        response = create_order(courier_id, colors)
        assert response.status_code == 201, f"Ожидался код ответа 201, но получен {response.status_code}"

    @pytest.mark.parametrize("colors", [
        (["BLACK"]),          # Один цвет
        (["GREY"]),           # Один цвет
        (["BLACK", "GREY"]),  # Оба цвета
        ([])                  # Без указания цвета
    ])
    def test_create_order_contains_track(self, create_courier_and_login, colors):
        # Тест проверяет, что ответ содержит трек-номер
        courier_data, courier_id = create_courier_and_login
        assert courier_id is not None, "Ошибка при авторизации курьера."

        response = create_order(courier_id, colors)
        assert response.status_code == 201, f"Ожидался код ответа 201, но получен {response.status_code}"
        assert "track" in response.json(), "Ответ на создание заказа не содержит трек"
