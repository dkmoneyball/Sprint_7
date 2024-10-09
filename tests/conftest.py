import pytest
import requests
from src.utils import generate_random_string, login_courier, BASE_URL
from src.test_data import get_order_payload  # Импортируем тестовые данные

@pytest.fixture
def courier_payload():
    return {
        "login": generate_random_string(),
        "password": generate_random_string(),
        "firstName": generate_random_string()
    }

@pytest.fixture
def create_courier(courier_payload):
    """Фикстура для создания нового курьера"""
    response = requests.post(f"{BASE_URL}/courier", json=courier_payload)

    yield courier_payload["login"], courier_payload["password"], courier_payload["firstName"]

    courier_id = login_courier(courier_payload["login"], courier_payload["password"])
    if courier_id:
        requests.delete(f"{BASE_URL}/courier/{courier_id}")

@pytest.fixture
def create_courier_and_login(courier_payload):
    response = requests.post(f"{BASE_URL}/courier", json=courier_payload)
    courier_id = login_courier(courier_payload["login"], courier_payload["password"])

    yield (courier_payload["login"], courier_payload["password"], courier_payload["firstName"]), courier_id

    if courier_id:
        requests.delete(f"{BASE_URL}/courier/{courier_id}")

@pytest.fixture
def order_payload():
    """Фикстура для получения данных заказа"""
    return get_order_payload()  # Используем функцию для получения данных заказа
