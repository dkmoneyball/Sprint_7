import pytest
import requests
from src.config import ORDERS_URL  # Импортируем URL для заказов из config.py


class TestGetOrders:

    # Тест на создание заказа - проверка статуса кода
    def test_create_order_status_code(self, create_courier_and_login):
        courier_data, courier_id = create_courier_and_login
        assert courier_id is not None, "Ошибка при авторизации курьера."

        # Создаем заказ
        payload = {
            "firstName": "Naruto",
            "lastName": "Uchiha",
            "address": "Konoha, 142 apt.",
            "metroStation": 4,
            "phone": "+7 800 355 35 35",
            "rentTime": 5,
            "deliveryDate": "2020-06-06",
            "comment": "Saske, come back to Konoha",
            "color": ["BLACK"]
        }

        response = requests.post(ORDERS_URL, json=payload)  # Используем ORDERS_URL из config
        assert response.status_code == 201, f"Ожидался код ответа 201, но получен {response.status_code}"

    # Тест на создание заказа - проверка наличия трек-номера
    def test_create_order_contains_track(self, create_courier_and_login):
        courier_data, courier_id = create_courier_and_login
        assert courier_id is not None, "Ошибка при авторизации курьера."

        # Создаем заказ
        payload = {
            "firstName": "Naruto",
            "lastName": "Uchiha",
            "address": "Konoha, 142 apt.",
            "metroStation": 4,
            "phone": "+7 800 355 35 35",
            "rentTime": 5,
            "deliveryDate": "2020-06-06",
            "comment": "Saske, come back to Konoha",
            "color": ["BLACK"]
        }

        response = requests.post(ORDERS_URL, json=payload)  # Используем ORDERS_URL из config
        assert response.status_code == 201, f"Ожидался код ответа 201, но получен {response.status_code}"
        # Проверка трек-номера
        assert "track" in response.json(), "Ответ на создание заказа не содержит трек"

    # Тест на получение списка заказов - проверка статуса кода
    def test_get_orders_list_status_code(self, create_courier_and_login):
        courier_data, courier_id = create_courier_and_login
        assert courier_id is not None, "Ошибка при авторизации курьера."

        # Получаем список заказов
        response = requests.get(ORDERS_URL)  # Используем ORDERS_URL из config
        assert response.status_code == 200, f"Ожидался код ответа 200, но получен {response.status_code}"

    # Тест на получение списка заказов - проверка наличия заказов
    def test_get_orders_list_contains_orders(self, create_courier_and_login):
        courier_data, courier_id = create_courier_and_login
        assert courier_id is not None, "Ошибка при авторизации курьера."

        # Получаем список заказов
        response = requests.get(ORDERS_URL)  # Используем ORDERS_URL из config
        assert response.status_code == 200, f"Ожидался код ответа 200, но получен {response.status_code}"

        orders = response.json().get("orders", [])
        assert isinstance(orders, list), "Ожидался список заказов в теле ответа"
        assert len(orders) > 0, "Список заказов пуст, хотя был создан заказ"
