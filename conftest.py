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
def auto_delete_courier():
    """Фикстура сама отслеживает курьеров и удаляет после теста"""
    created_couriers = []
    
    def track_courier(login, password):
        """Получает ID курьера и сохраняет для удаления"""
        login_payload = {"login": login, "password": password}
        login_response = requests.post(f"{BASE_URL}{COURIER_LOGIN_ENDPOINT}", data=login_payload)
        courier_id = login_response.json()["id"]
        created_couriers.append(courier_id)
        return courier_id
    
    yield track_courier
    
    # АВТОМАТИЧЕСКОЕ УДАЛЕНИЕ ПОСЛЕ ТЕСТА
    for courier_id in created_couriers:
        params = {"id": courier_id}
        requests.delete(f"{BASE_URL}{COURIER_ENDPOINT}", params=params)


# ========== ФИКСТУРА ДЛЯ АВТООТМЕНЫ ЗАКАЗОВ ==========

@pytest.fixture
def auto_delete_order():
    """Фикстура сама отслеживает заказы и отменяет после теста"""
    created_orders = []
    
    def track_order(track):
        """Сохраняет track заказа для отмены"""
        created_orders.append(track)
        return track
    
    yield track_order
    
    # АВТОМАТИЧЕСКАЯ ОТМЕНА ПОСЛЕ ТЕСТА
    for track in created_orders:
        payload = {"track": track}
        requests.put(f"{BASE_URL}{ORDERS_CANCEL_ENDPOINT}", json=payload)


# ========== КОМБИНИРОВАННАЯ ФИКСТУРА (создание + автоудаление) ==========

@pytest.fixture
def created_courier(create_courier):
    """Создает курьера перед тестом и автоматически удаляет после"""
    courier = create_courier
    yield courier
