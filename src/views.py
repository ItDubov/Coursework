import json
import os
import pandas as pd
from datetime import datetime
from src.utils import get_greeting, get_card_data, get_top_transactions, load_user_settings
from src.external_api import get_currency_rates, get_stock_prices
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Формируем путь до директории модуля
CURRENT_DIR = os.path.dirname(__file__)
OPERATIONS_PATH = os.path.join(CURRENT_DIR, '..', 'data', 'operations.xlsx')


def convert_timestamps_to_strings(data):
    """Рекурсивно преобразует все объекты Timestamp в строки в переданной структуре данных."""
    if isinstance(data, dict):
        return {key: convert_timestamps_to_strings(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [convert_timestamps_to_strings(item) for item in data]
    elif isinstance(data, pd.Timestamp):
        return data.strftime("%Y-%m-%d %H:%M:%S") if pd.notna(data) else None
    else:
        return data


def filter_transactions(transactions: pd.DataFrame, date_time_str: str) -> pd.DataFrame:
    """Фильтрует транзакции с начала месяца до указанной даты."""
    # Преобразуем строку даты в объект datetime
    end_date = datetime.strptime(date_time_str, "%Y-%m-%d %H:%M:%S")

    # Определяем начало месяца на основе переданной даты
    start_date = end_date.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    # Фильтруем транзакции в заданном временном диапазоне
    filtered_transactions = transactions[
        (transactions["Дата операции"] >= start_date) & (transactions["Дата операции"] <= end_date)
        ]

    return filtered_transactions


def main_page_view() -> str:
    greeting = get_greeting()

    # Чтение данных из файла
    try:
        transactions = pd.read_excel(OPERATIONS_PATH, engine='openpyxl')
        # Преобразуем строки в объекты datetime для корректной фильтрации
        transactions["Дата операции"] = pd.to_datetime(
            transactions["Дата операции"], format="%d.%m.%Y %H:%M:%S", errors='coerce', dayfirst=True
        )
    except FileNotFoundError:
        logging.error(f"Файл '{OPERATIONS_PATH}' не найден.")
        transactions = pd.DataFrame()

    # Пример использования фильтрации: передаем конкретную дату и время
    date_time_str = "2021-11-15 12:34:56"
    transactions = filter_transactions(transactions, date_time_str)

    # Получение данных о картах и топ транзакций
    cards_data = get_card_data(transactions)
    top_transactions = get_top_transactions(transactions)

    # Загрузка настроек пользователя из JSON-файла
    user_settings_path = os.path.join(CURRENT_DIR, '..', 'data', 'user_settings.json')
    user_settings = load_user_settings(user_settings_path)

    # Получение списков валют и акций из настроек
    currencies = user_settings.get("currencies", [])
    stocks = user_settings.get("stocks", [])

    # Загрузка курсов валют и цен акций из локальных JSON-файлов
    currency_rates = get_currency_rates(currencies)
    stock_prices = get_stock_prices(stocks)

    result = {
        "greeting": greeting,
        "cards": cards_data,
        "top_transactions": top_transactions,
        "currency_rates": currency_rates,
        "stock_prices": stock_prices,
    }
    result = convert_timestamps_to_strings(result)
    return json.dumps(result, ensure_ascii=False, indent=2)
