import requests
import allure
from constants import (
    BASE_URL,
    ORDERS_ENDPOINT,
    SUCCESS_ORDERS_LIST_CODE
)


@allure.feature('Список заказов')
class TestOrdersList:

    @allure.title('Получение списка заказов')
    @allure.description('Проверка, что в ответе возвращается список заказов')
    def test_orders_list_returns_list_of_orders_success(self):
        with allure.step('Отправить запрос на получение списка заказов'):
            response = requests.get(f"{BASE_URL}{ORDERS_ENDPOINT}")

        with allure.step('Проверить успешный ответ и наличие списка'):
            assert response.status_code == SUCCESS_ORDERS_LIST_CODE
            assert "orders" in response.json()
