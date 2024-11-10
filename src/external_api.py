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
    url = f"https://v6.exchangerate-api.com/v6/{api_key_currency}/latest/USD"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Проверка на ошибки ответа
        data = response.json()

        # Проверка на наличие ключа 'conversion_rates'
        if 'conversion_rates' not in data:
            logging.error("Ответ API не содержит ключ 'conversion_rates'.")
            return [{"currency": curr, "rate_in_rub": None} for curr in currencies]

        conversion_rates = data['conversion_rates']

        # Проверка наличия курса RUB
        if 'RUB' not in conversion_rates:
            logging.error("Курс RUB отсутствует в данных API.")
            return [{"currency": curr, "rate_in_rub": None} for curr in currencies]

        rub_rate = conversion_rates['RUB']

        # Преобразование курсов валют в RUB
        result = []
        for curr in currencies:
            if curr in conversion_rates:
                rate_in_rub = conversion_rates[curr] * rub_rate
                result.append({"currency": curr, "rate_in_rub": rate_in_rub})
            else:
                result.append({"currency": curr, "rate_in_rub": None})

        return result

    except requests.RequestException as e:
        logging.error(f"Ошибка при получении курсов валют: {e}")
        return [{"currency": curr, "rate_in_rub": None} for curr in currencies]


def get_stock_prices(stocks: list) -> list:
    """Получает цены акций из внешнего API."""
    api_key_prices = os.getenv("API_KEY_prices")
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
