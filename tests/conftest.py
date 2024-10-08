import pytest
from src.utils import generate_random_string, login_courier, BASE_URL
import requests

@pytest.fixture
def courier_payload():
    """Фикстура для генерации данных курьера"""
    return {
        "login": generate_random_string(),
        "password": generate_random_string(),
        "firstName": generate_random_string()
    }

@pytest.fixture
def create_courier(courier_payload):
    """Фикстура для создания нового курьера"""
    response = requests.post(f"{BASE_URL}/courier", json=courier_payload)
    # Здесь мы можем сделать проверку статуса в тестах, а не в фикстуре

    yield courier_payload["login"], courier_payload["password"], courier_payload["firstName"]

    # После завершения теста авторизуем курьера и удаляем его
    courier_id = login_courier(courier_payload["login"], courier_payload["password"])
    if courier_id:
        requests.delete(f"{BASE_URL}/courier/{courier_id}")

@pytest.fixture
def create_courier_and_login(courier_payload):
    """Фикстура для создания и авторизации курьера"""
    response = requests.post(f"{BASE_URL}/courier", json=courier_payload)
    # Проверку статуса переносим в тесты

    # Авторизуем курьера
    courier_id = login_courier(courier_payload["login"], courier_payload["password"])

    yield (courier_payload["login"], courier_payload["password"], courier_payload["firstName"]), courier_id

    # После завершения теста удаляем созданного курьера
    if courier_id:
        requests.delete(f"{BASE_URL}/courier/{courier_id}")
