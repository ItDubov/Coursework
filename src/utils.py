import pandas as pd
from datetime import datetime
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def get_greeting(current_time: datetime) -> str:
    """Возвращает приветствие в зависимости от времени суток."""
    hour = current_time.hour
    if 5 <= hour < 12:
        return "Доброе утро"
    elif 12 <= hour < 17:
        return "Добрый день"
    elif 17 <= hour < 23:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def load_transactions_from_excel(file_path: str) -> pd.DataFrame:
    """Загружает транзакции из Excel файла и возвращает DataFrame."""
    try:
        transactions = pd.read_excel(file_path, engine='openpyxl')
        # Преобразуем даты в нужный формат
        transactions["Дата операции"] = pd.to_datetime(
            transactions["Дата операции"], format="%d.%m.%Y %H:%M:%S", errors='coerce', dayfirst=True
        )
        return transactions
    except Exception as e:
        logging.error(f"Ошибка при загрузке транзакций из Excel: {e}")
        return pd.DataFrame()

def get_card_data(transactions: pd.DataFrame) -> list:
    """Возвращает информацию о картах на основе данных транзакций."""
    card_data = []

    # Проходим по строкам DataFrame и собираем информацию о картах
    for _, transaction in transactions.iterrows():
        card_number = transaction["Номер карты"]  # Теперь обращаемся как к столбцу DataFrame
        amount = transaction.get("Сумма операции", 0)  # Получаем сумму транзакции

        # Собираем информацию о карте
        card_info = {
            "last_digits": str(card_number)[-4:],  # Последние 4 цифры карты
            "amount": amount  # Добавляем сумму для примера
        }
        card_data.append(card_info)

    return card_data


def get_top_transactions(transactions: pd.DataFrame) -> list:
    """Возвращает топ-5 транзакций по сумме."""
    # Сортируем транзакции по сумме в порядке убывания и берем первые 5
    top_transactions = transactions.sort_values(by="Сумма операции", ascending=False).head(5)

    # Формируем список словарей для вывода
    return [
        {
            "date": row["Дата операции"],
            "amount": row["Сумма операции"],
            "description": row.get("Описание", "")
        }
        for _, row in top_transactions.iterrows()
    ]
