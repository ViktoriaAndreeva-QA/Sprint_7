import requests
import pytest
import allure
from constants import (
    BASE_URL,
    ORDERS_ENDPOINT,
    SUCCESS_CREATED_CODE
)
from data.orders_data import generate_order_data


@allure.feature('Создание заказа')
class TestCreateOrder:

    @pytest.mark.parametrize("color", [
        ["BLACK"],
        ["GREY"],
        ["BLACK", "GREY"],
        []
    ])
    @allure.title('Создание заказа с цветом {color}')
    @allure.description('Проверка создания заказа с разными вариантами цветов')
    def test_create_order_with_different_colors_success(self, color, delete_order):
        with allure.step('Сгенерировать данные заказа'):
            order_data = generate_order_data()
            order_data["color"] = color

        response = requests.post(f"{BASE_URL}{ORDERS_ENDPOINT}", json=order_data)
        
        with allure.step('Проверить успешное создание и наличие track'):
            assert response.status_code == SUCCESS_CREATED_CODE
            assert "track" in response.json()

        track = response.json()["track"]
        delete_order(track)
