import os
import requests
from dotenv import load_dotenv
import logging

# Загрузка переменных окружения
load_dotenv()

# Настройка логгирования
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def get_currency_rates(currencies: list) -> list:
    """Получает курсы валют из внешнего API."""
    api_key = os.getenv("API_KEY_RATES")
    url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/USD"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Проверка на ошибки ответа
        data = response.json()

        # Проверка на наличие ключа 'rates'
        if 'rates' not in data:
            logging.error("Ответ API не содержит ключ 'rates'.")
            return [{"currency": curr, "rate": None} for curr in currencies]

        # Извлечение курсов для запрошенных валют
        return [{"currency": curr, "rate": data["rates"].get(curr)} for curr in currencies]

    except requests.RequestException as e:
        logging.error(f"Ошибка при получении курсов валют: {e}")
        return [{"currency": curr, "rate": None} for curr in currencies]


def get_stock_prices(stocks: list) -> list:
    """Получает цены акций из внешнего API."""
    api_key = os.getenv("API_KEY_PRICES")
    stock_data = []

    for stock in stocks:
        url = f"https://finnhub.io/api/v1/quote?symbol={stock}&token={api_key}"
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
