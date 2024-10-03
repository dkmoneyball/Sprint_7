import pytest
import requests

BASE_URL = "https://qa-scooter.praktikum-services.ru/api/v1"

class TestGetOrders:

    def test_get_orders_list(self, create_courier_and_login):
        # Используем фикстуру create_courier_and_login для создания и авторизации курьера
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

        response = requests.post(f"{BASE_URL}/orders", json=payload)
        assert response.status_code == 201, f"Ожидался код ответа 201, но получен {response.status_code}"
        assert "track" in response.json(), "Ответ на создание заказа не содержит трек"

        # Получаем список заказов
        response = requests.get(f"{BASE_URL}/orders")
        assert response.status_code == 200, f"Ожидался код ответа 200, но получен {response.status_code}"

        orders = response.json().get("orders", [])
        assert isinstance(orders, list), "Ожидался список заказов в теле ответа"
        assert len(orders) > 0, "Список заказов пуст, хотя был создан заказ"
