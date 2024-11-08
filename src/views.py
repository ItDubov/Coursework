import json
import os
import pandas as pd
from datetime import datetime
from src.utils import get_greeting, get_card_data, get_top_transactions
from src.external_api import get_currency_rates, get_stock_prices
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Формируем путь до директории модуля
CURRENT_DIR = os.path.dirname(__file__)
# Из этого пути прописываем конкретный путь до файла xlsx, выходим из src, заходим в data и далее к файлу
OPERATIONS_PATH = os.path.join(CURRENT_DIR, '..', 'data', 'operations.xlsx')


def main_page_view(date_time_str: str) -> str:
    date_time = datetime.strptime(date_time_str, "%Y-%m-%d %H:%M:%S")
    greeting = get_greeting(date_time)

    # Чтение данных из файла
    try:
        transactions = pd.read_excel(OPERATIONS_PATH)
    except FileNotFoundError:
        logging.error(f"Файл '{OPERATIONS_PATH}' не найден.")
        transactions = pd.DataFrame()

    # Получение данных о картах и топ транзакций
    cards_data = get_card_data(transactions)
    top_transactions = get_top_transactions(transactions)

    # Курсы валют и цены акций
    currency_rates = get_currency_rates(["USD", "EUR"])
    stock_prices = get_stock_prices(["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"])

    result = {
        "greeting": greeting,
        "cards": cards_data,
        "top_transactions": top_transactions,
        "currency_rates": currency_rates,
        "stock_prices": stock_prices,
    }
    return json.dumps(result, ensure_ascii=False, indent=2)
