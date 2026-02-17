import requests
import pytest
import random
import string
import allure
from courier_generate_method import register_new_courier_and_return_login_password
from constants import (
    BASE_URL, 
    COURIER_ENDPOINT,
    COURIER_LOGIN_ENDPOINT,
    ERROR_MISSING_FIELD_MESSAGE,
    ERROR_LOGIN_ALREADY_EXISTS_MESSAGE,
    SUCCESS_CREATED_CODE,
    SUCCESS_CREATED_MESSAGE,
    SUCCESS_LOGIN_CODE,
    ERROR_CONFLICT_CODE,
    ERROR_BAD_REQUEST_CODE
)


@allure.feature('Создание курьера')
class TestCreateCourier:

    @allure.title('Успешное создание курьера')
    @allure.description('Проверка создания курьера с валидными данными')
    def test_create_courier_with_valid_data_success(self, auto_delete_courier):
        with allure.step('Создать курьера через метод регистрации'):
            courier = register_new_courier_and_return_login_password()

        payload = {
                "login": courier[0],
                "password": courier[1]
            }
        
        with allure.step('Проверить, что курьер создан и доступен для логина'):
            response = requests.post(f"{BASE_URL}{COURIER_LOGIN_ENDPOINT}", data=payload)

        assert response.status_code == SUCCESS_LOGIN_CODE
        assert "id" in response.json()

        with allure.step('Зарегистрировать курьера для автоудаления'):
            auto_delete_courier(courier[0], courier[1])

    @allure.title('Создание двух одинаковых курьеров')
    @allure.description('Проверка невозможности создания двух курьеров с одинаковыми данными')
    def test_create_two_couriers_with_the_same_data_fails(self, auto_delete_courier):
        with allure.step('Создать первого курьера'):
            first_courier = register_new_courier_and_return_login_password()

        with allure.step('Зарегистрировать первого курьера для автоудаления'):
            auto_delete_courier(first_courier[0], first_courier[1])
    
        with allure.step('Попытаться создать второго с теми же данными'):
            payload = {
                "login": first_courier[0],
                "password": first_courier[1],
                "firstName": first_courier[2]
            }

        with allure.step('Получена ошибка конфликта'):
            response = requests.post(f"{BASE_URL}{COURIER_ENDPOINT}", data=payload)

        assert response.status_code == ERROR_CONFLICT_CODE
        assert response.json().get("message") == ERROR_LOGIN_ALREADY_EXISTS_MESSAGE

    @allure.title('Создание курьера только с обязательными полями')
    @allure.description('Проверка создания курьера только с логином и паролем')
    def test_create_courier_with_only_required_fields_success(self, auto_delete_courier):
        with allure.step('Сгенерировать логин и пароль'):
            login = ''.join(random.choices(string.ascii_lowercase, k=10))
            password = ''.join(random.choices(string.ascii_lowercase, k=10))
    
        payload = {
            "login": login,
            "password": password
        }

        response = requests.post(f"{BASE_URL}{COURIER_ENDPOINT}", data=payload)

        with allure.step('Зарегистрировать курьера для автоудаления'):
            auto_delete_courier(login, password)

        with allure.step('Проверить успешное создание'):
            assert response.status_code == SUCCESS_CREATED_CODE
            assert response.json() == SUCCESS_CREATED_MESSAGE

    @pytest.mark.parametrize("missing_field", ["login", "password"])
    @allure.title('Создание курьера без обязательного поля')
    @allure.description('Проверка ошибки при отсутствии логина или пароля')
    def test_create_courier_without_required_field_fails(self, missing_field):
        with allure.step('Сгенерировать уникальные данные'):
            login = ''.join(random.choices(string.ascii_lowercase, k=10))
            password = ''.join(random.choices(string.ascii_lowercase, k=10))
            first_name = ''.join(random.choices(string.ascii_lowercase, k=10))

        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }

        payload[missing_field] = ""

        with allure.step('Отправить запрос с отсутствующим полем'):
            response = requests.post(f"{BASE_URL}{COURIER_ENDPOINT}", data=payload)

        assert response.status_code == ERROR_BAD_REQUEST_CODE
        assert response.json().get("message") == ERROR_MISSING_FIELD_MESSAGE

    @allure.title('Создание курьера с существующим логином')
    @allure.description('Проверка ошибки при создании курьера с уже существующим логином')
    def test_create_courier_with_existing_login_fails(self, created_courier, auto_delete_courier):
        with allure.step('Зарегистрировать существующего курьера для автоудаления'):
            auto_delete_courier(created_courier["login"], created_courier["password"])
        
        with allure.step('Попытаться создать второго курьера с тем же логином'):
            second_courier = {
                "login": created_courier["login"],
                "password": "another_password",
                "firstName": "another_name"
            }

        response = requests.post(f"{BASE_URL}{COURIER_ENDPOINT}", json=second_courier)

        assert response.status_code == ERROR_CONFLICT_CODE
        assert response.json().get("message") == ERROR_LOGIN_ALREADY_EXISTS_MESSAGE
