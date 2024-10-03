import pytest
import requests

BASE_URL = "https://qa-scooter.praktikum-services.ru/api/v1"

class TestCreateOrder:

    @pytest.mark.parametrize("colors", [
        (["BLACK"]),          # Один цвет
        (["GREY"]),           # Один цвет
        (["BLACK", "GREY"]),  # Оба цвета
        ([])                  # Без указания цвета
    ])
    def test_create_order(self, create_courier_and_login, colors):
        courier_data, courier_id = create_courier_and_login
        assert courier_id is not None, "Ошибка при авторизации курьера."

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

        response = requests.post(f"{BASE_URL}/orders", json=payload)
        assert response.status_code == 201, f"Ожидался код ответа 201, но получен {response.status_code}"
        assert "track" in response.json(), "Ответ на создание заказа не содержит трек"
