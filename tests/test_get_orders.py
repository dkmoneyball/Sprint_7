import pytest
import requests
from src.config import ORDERS_URL  # Импортируем URL для заказов из config.py
from src.test_data import get_order_payload  # Импортируем функцию для получения пейлоада заказа

class TestGetOrders:

    @pytest.mark.parametrize("colors", [
        (["BLACK"]),          # Один цвет
        (["GREY"]),           # Один цвет
        (["BLACK", "GREY"]),  # Оба цвета
        ([])                  # Без указания цвета
    ])
    def test_create_order_status_code(self, create_courier_and_login, colors):
        # Получаем ID курьера из фикстуры
        _, courier_id = create_courier_and_login

        # Получаем пейлоад для создания заказа и изменяем цвет
        order_payload = get_order_payload()
        order_payload["color"] = colors

        response = requests.post(ORDERS_URL, json=order_payload)

        # Проверяем статус код
        assert response.status_code == 201, f"Ожидался код ответа 201, но получен {response.status_code}"

    @pytest.mark.parametrize("colors", [
        (["BLACK"]),          # Один цвет
        (["GREY"]),           # Один цвет
        (["BLACK", "GREY"]),  # Оба цвета
        ([])                  # Без указания цвета
    ])
    def test_create_order_contains_track(self, create_courier_and_login, colors):
        # Получаем ID курьера из фикстуры
        _, courier_id = create_courier_and_login

        # Получаем пейлоад для создания заказа и изменяем цвет
        order_payload = get_order_payload()
        order_payload["color"] = colors

        response = requests.post(ORDERS_URL, json=order_payload)

        # Проверяем наличие трек-номера
        assert "track" in response.json(), "Ответ на создание заказа не содержит трек"

    def test_get_orders_list_status_code(self, create_courier_and_login):
        # Получаем ID курьера из фикстуры
        _, courier_id = create_courier_and_login

        response = requests.get(ORDERS_URL)

        # Проверяем статус код
        assert response.status_code == 200, f"Ожидался код ответа 200, но получен {response.status_code}"

    def test_get_orders_list_contains_orders(self, create_courier_and_login):
        # Получаем ID курьера из фикстуры
        _, courier_id = create_courier_and_login

        response = requests.get(ORDERS_URL)
        orders = response.json().get("orders", [])

        # Проверяем, что в ответе есть список заказов
        assert isinstance(orders, list), "Ожидался список заказов в теле ответа"
        assert len(orders) > 0, "Список заказов пуст, хотя был создан заказ"
