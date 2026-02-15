import random
import string
from datetime import datetime, timedelta


def generate_random_string(length):
    """Генерирует случайную строку из английских букв"""
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for _ in range(length))

def generate_phone():
    """Генерирует случайный телефон"""
    return f"+7 {random.randint(1111111111, 9999999999)}"

def random_future_date():
    """Возвращает случайную дату в будущем"""
    days = random.randint(1, 10)
    return (datetime.now() + timedelta(days=days)).strftime("%Y-%m-%d")

def generate_order_data():
    """Генерирует уникальные данные для заказа"""
    return {
        "firstName": f"FirstName_{generate_random_string(6)}",
        "lastName": f"LastName_{generate_random_string(6)}",
        "address": f"City_{generate_random_string(8)}, {random.randint(1, 999)}",
        "metroStation": random.randint(1, 15),
        "phone": generate_phone(),
        "rentTime": random.randint(1, 7),
        "deliveryDate": random_future_date(),
        "comment": f"Comment_{generate_random_string(10)}"
    }
