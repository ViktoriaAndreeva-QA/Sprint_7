import requests
import pytest
import allure
from constants import (
    BASE_URL, 
    COURIER_LOGIN_ENDPOINT,
    SUCCESS_LOGIN_CODE,
    ERROR_BAD_REQUEST_CODE,
    ERROR_NOT_FOUND_CODE,
    ERROR_MISSING_LOGIN_DATA_MESSAGE,
    ERROR_ACCOUNT_NOT_FOUND_MESSAGE
)


@allure.feature('Логин курьера')
class TestLoginCourier:

    @allure.title('Успешный логин курьера')
    @allure.description('Проверка авторизации с существующими логином и паролем')
    def test_login_courier_with_existing_login_and_password_success(self, created_courier, auto_delete_courier):
        with allure.step('Зарегистрировать курьера для автоудаления'):
            auto_delete_courier(created_courier["login"], created_courier["password"])

        with allure.step('Отправить запрос на логин'):
            payload = {
                "login": created_courier["login"],
                "password": created_courier["password"]
            }

        response = requests.post(f"{BASE_URL}{COURIER_LOGIN_ENDPOINT}", data=payload)

        with allure.step('Успешный ответ и ID'):
            assert response.status_code == SUCCESS_LOGIN_CODE
            assert response.json()["id"] == created_courier["id"]

    @pytest.mark.parametrize("missing_field", ["login", "password"])
    @allure.title('Логин без обязательного поля')
    @allure.description('Проверка ошибки при отсутствии логина или пароля')
    def test_login_courier_with_missing_required_field_fails(self, created_courier, missing_field, auto_delete_courier):
        with allure.step('Зарегистрировать курьера для автоудаления'):
            auto_delete_courier(created_courier["login"], created_courier["password"])

        with allure.step(f'Отправить запрос без поля {missing_field}'):
            payload = {
                "login": created_courier["login"],
                "password": created_courier["password"]
            }

        payload[missing_field] = ""

        response = requests.post(f"{BASE_URL}{COURIER_LOGIN_ENDPOINT}", data=payload)

        assert response.status_code == ERROR_BAD_REQUEST_CODE
        assert response.json().get("message") == ERROR_MISSING_LOGIN_DATA_MESSAGE

    @pytest.mark.parametrize("field, wrong_value", [
        ("login", "another_login"),
        ("password", "another_password")
    ])
    @allure.title('Логин с неправильными данными')
    @allure.description('Проверка ошибки при неправильном логине или пароле')
    def test_login_courier_with_wrong_credentials_fails(self, created_courier, field, wrong_value, auto_delete_courier):
        with allure.step('Зарегистрировать курьера для автоудаления'):
            auto_delete_courier(created_courier["login"], created_courier["password"])

        with allure.step(f'Отправить запрос с неправильным {field}'):
            payload = {
                "login": created_courier["login"],
                "password": created_courier["password"]
            }

        payload[field] = wrong_value

        response = requests.post(f"{BASE_URL}{COURIER_LOGIN_ENDPOINT}", data=payload)

        assert response.status_code == ERROR_NOT_FOUND_CODE
        assert response.json().get("message") == ERROR_ACCOUNT_NOT_FOUND_MESSAGE

    @allure.title('Логин несуществующего курьера')
    @allure.description('Проверка ошибки при авторизации несуществующего пользователя')
    def test_login_courier_nonexistent_courier_fails(self):
        with allure.step('Отправить запрос с несуществующими данными'):
            payload = {
                "login": "nonexistentLogin",
                "password": "nonexistentPassword"
            }

        response = requests.post(f"{BASE_URL}{COURIER_LOGIN_ENDPOINT}", data=payload)

        assert response.status_code == ERROR_NOT_FOUND_CODE
        assert response.json().get("message") == ERROR_ACCOUNT_NOT_FOUND_MESSAGE
