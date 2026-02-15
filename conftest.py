import pytest
import requests
from courier_generate_method import register_new_courier_and_return_login_password
from constants import (
    BASE_URL, 
    COURIER_LOGIN_ENDPOINT,
    COURIER_ENDPOINT,
    ORDERS_CANCEL_ENDPOINT
)
from data.orders_data import generate_order_data


# ========== ФИКСТУРА ДЛЯ СОЗДАНИЯ ==========

@pytest.fixture
def create_courier():
    """Создает курьера и возвращает его данные (логин, пароль, ID)"""
    # Получаем данные нового курьера
    courier_data = register_new_courier_and_return_login_password()
    login = courier_data[0]
    password = courier_data[1]
    
    # Логинимся, чтобы получить ID
    login_payload = {"login": login, "password": password}
    login_response = requests.post(f"{BASE_URL}{COURIER_LOGIN_ENDPOINT}", data=login_payload)
    courier_id = login_response.json()["id"]
    
    # Возвращаем полные данные
    return {
        "login": login,
        "password": password,
        "id": courier_id
    }


# ========== ФИКСТУРЫ ДЛЯ УДАЛЕНИЯ ==========

@pytest.fixture
def delete_courier():
    """Возвращает функцию для удаления курьера по ID"""
    def _delete_courier(courier_id):
        params = {"id": courier_id}
        response = requests.delete(f"{BASE_URL}{COURIER_ENDPOINT}", params=params)
        return response.status_code == 200
    return _delete_courier


@pytest.fixture
def delete_order():
    """Возвращает функцию для отмены заказа по track"""
    def _delete_order(track):
        payload = {"track": track}
        response = requests.put(f"{BASE_URL}{ORDERS_CANCEL_ENDPOINT}", json=payload)
        return response.status_code == 200
    return _delete_order


# ========== КОМБИНИРОВАННАЯ ФИКСТУРА (создание + автоудаление) ==========

@pytest.fixture
def created_courier(create_courier, delete_courier):
    """Создает курьера перед тестом и автоматически удаляет после"""
    courier = create_courier
    yield courier
    delete_courier(courier["id"])
