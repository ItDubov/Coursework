import os
import requests
from dotenv import load_dotenv
import logging

# Загрузка переменных окружения
load_dotenv()

# Настройка логгирования
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def get_currency_rates(currencies: list) -> list:
    """Получает курсы валют и переводит их сразу в российские рубли."""
    api_key_currency = os.getenv("API_KEY_RATES")
    result = []

    # Цикл по каждой валюте из списка currencies
    for curr in currencies:
        url = f"https://v6.exchangerate-api.com/v6/{api_key_currency}/latest/{curr}"

        try:
            response = requests.get(url)
            response.raise_for_status()  # Проверка на ошибки ответа
            data = response.json()

            # Проверка на наличие ключа 'conversion_rates' и курса RUB
            if 'conversion_rates' not in data or 'RUB' not in data['conversion_rates']:
                logging.error(f"Курс RUB отсутствует в данных API для валюты {curr}.")
                result.append({"currency": curr, "rate_in_rub": None})
                continue

            # Получение курса RUB и добавление в результат
            rub_rate = data['conversion_rates']['RUB']
            result.append({"currency": curr, "rate_in_rub": rub_rate})

        except requests.RequestException as e:
            logging.error(f"Ошибка при получении курса валюты {curr}: {e}")
            result.append({"currency": curr, "rate_in_rub": None})

    return result


def get_stock_prices(stocks: list) -> list:
    """Получает цены акций из внешнего API."""
    api_key_prices = os.getenv("API_KEY_PRICES")
    stock_data = []

    for stock in stocks:
        url = f"https://finnhub.io/api/v1/quote?symbol={stock}&token={api_key_prices}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            # Добавление цены или None, если ответ не содержит нужных данных
            stock_data.append({"stock": stock, "price": data.get("c")})

        except requests.RequestException as e:
            logging.error(f"Ошибка при получении цены для {stock}: {e}")
            stock_data.append({"stock": stock, "price": None})

    return stock_data
