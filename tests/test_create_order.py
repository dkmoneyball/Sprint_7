import pytest
import requests
from src.config import ORDERS_URL  # Импортируем URL для заказов из config.py

class TestCreateOrder:

    @pytest.mark.parametrize("colors", [
        (["BLACK"]),          # Один цвет
        (["GREY"]),           # Один цвет
        (["BLACK", "GREY"]),  # Оба цвета
        ([])                  # Без указания цвета
    ])
    def test_create_order_status_code(self, create_courier_and_login, order_payload, colors):
        # Используем фикстуру для авторизованного курьера, проверку авторизации убираем
        _, courier_id = create_courier_and_login

        # Изменяем цвет в пейлоаде заказа перед отправкой запроса
        order_payload["color"] = colors
        response = requests.post(ORDERS_URL, json=order_payload)

        # Проверяем код ответа
        assert response.status_code == 201, f"Ожидался код ответа 201, но получен {response.status_code}"

    @pytest.mark.parametrize("colors", [
        (["BLACK"]),          # Один цвет
        (["GREY"]),           # Один цвет
        (["BLACK", "GREY"]),  # Оба цвета
        ([])                  # Без указания цвета
    ])
    def test_create_order_contains_track(self, create_courier_and_login, order_payload, colors):
        # Используем фикстуру для авторизованного курьера, проверку авторизации убираем
        _, courier_id = create_courier_and_login

        # Изменяем цвет в пейлоаде заказа перед отправкой запроса
        order_payload["color"] = colors
        response = requests.post(ORDERS_URL, json=order_payload)

        # Проверяем наличие трек-номера в ответе
        assert "track" in response.json(), "Ответ на создание заказа не содержит трек-номер"

    def test_create_order_missing_track(self, create_courier_and_login, order_payload):
        # Используем фикстуру для авторизованного курьера, проверку авторизации убираем
        _, courier_id = create_courier_and_login

        # Отправляем запрос
        response = requests.post(ORDERS_URL, json=order_payload)

        # Проверяем наличие трек-номера в ответе
        assert "track" in response.json(), "Ответ на создание заказа не содержит трек-номер"
