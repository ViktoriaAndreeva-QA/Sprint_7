# URL сервиса
BASE_URL = "https://qa-scooter.praktikum-services.ru"

# Эндпоинты
COURIER_ENDPOINT = "/api/v1/courier"
COURIER_LOGIN_ENDPOINT = "/api/v1/courier/login"
ORDERS_ENDPOINT = "/api/v1/orders"
ORDERS_CANCEL_ENDPOINT = "/api/v1/orders/cancel"

# Ожидаемые ответы на запросы
SUCCESS_CREATED_CODE = 201
SUCCESS_CREATED_MESSAGE = {"ok": True}

SUCCESS_LOGIN_CODE = 200

SUCCESS_ORDERS_LIST_CODE = 200

ERROR_CONFLICT_CODE = 409
ERROR_LOGIN_ALREADY_EXISTS_MESSAGE = "Этот логин уже используется. Попробуйте другой."

ERROR_BAD_REQUEST_CODE = 400
ERROR_MISSING_FIELD_MESSAGE = "Недостаточно данных для создания учетной записи"
ERROR_MISSING_LOGIN_DATA_MESSAGE = "Недостаточно данных для входа"

ERROR_NOT_FOUND_CODE = 404
ERROR_ACCOUNT_NOT_FOUND_MESSAGE = "Учетная запись не найдена"

