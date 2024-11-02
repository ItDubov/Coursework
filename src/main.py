import datetime
import pandas as pd
import json
from src.data_processing import get_card_data, get_top_transactions
from src.external_api import get_currency_rates, get_stock_prices
from src.services import analyze_cashback_categories
from src.reports import spending_by_category


def get_greeting(current_time):
    """Возвращает приветствие в зависимости от времени суток."""
    hour = current_time.hour
    if 5 <= hour < 12:
        return "Доброе утро"
    elif 12 <= hour < 18:
        return "Добрый день"
    elif 18 <= hour < 22:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def get_data_json(datetime_str):
    """Главная функция для получения данных и формирования JSON-ответа."""
    # Парсинг строки даты и времени
    current_time = datetime.datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
    greeting = get_greeting(current_time)

    # Данные по картам
    card_data = get_card_data()

    # Топ-5 транзакций
    top_transactions = get_top_transactions()

    # Курсы валют и цены акций
    currency_rates = get_currency_rates(["USD", "EUR"])
    stock_prices = get_stock_prices(["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"])

    # Формирование JSON-ответа
    response = {
        "greeting": greeting,
        "cards": card_data,
        "top_transactions": top_transactions,
        "currency_rates": currency_rates,
        "stock_prices": stock_prices
    }

    return json.dumps(response, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    json_data = get_data_json("2021-12-21 13:45:00")

    transactions_data = [
        {"date": "2023-05-01T12:45:00", "category": "Супермаркеты", "amount": 1200},
        {"date": "2023-05-03T08:20:00", "category": "Рестораны", "amount": 500},
        {"date": "2023-05-05T18:30:00", "category": "Супермаркеты", "amount": 1300},
        {"date": "2023-05-07T20:45:00", "category": "Кино", "amount": 200},
        {"date": "2023-04-15T14:00:00", "category": "Рестораны", "amount": 600},
    ]
    result = analyze_cashback_categories(transactions_data, 2023, 5)

    data = {
        'date': ['2023-08-15', '2023-07-10', '2023-09-05', '2023-09-20', '2023-06-25'],
        'category': ['Супермаркеты', 'Супермаркеты', 'Рестораны', 'Супермаркеты', 'Рестораны'],
        'amount': [1500, 700, 800, 250, 650]
    }
    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date'])

    report = spending_by_category(df, 'Супермаркеты', '2023-09-30')

    print(json_data)
    print(result)
    print(report)
