import pandas as pd
from datetime import datetime
import logging
import json
import os

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def get_greeting() -> str:
    """Возвращает приветствие в зависимости от текущего времени суток."""
    # Получаем текущее время
    current_time = datetime.now()
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

# Формируем путь до директории модуля
CURRENT_DIR = os.path.dirname(__file__)

def load_user_settings(file_path: str) -> dict:
    """Загружает настройки пользователя из JSON файла."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        logging.error(f"Файл '{file_path}' не найден.")
        return {}
    except json.JSONDecodeError:
        logging.error(f"Ошибка декодирования JSON в файле '{file_path}'.")
        return {}


def get_card_data(transactions: pd.DataFrame) -> list:
    """Возвращает аккумулированные данные о картах на основе данных транзакций."""
    # Удаляем все операции, не являющиеся расходами (только отрицательные суммы)
    transactions = transactions[transactions["Сумма операции"] < 0]

    # Фильтруем транзакции, у которых нет номера карты
    transactions = transactions[transactions["Номер карты"].notna()].copy()

    # Преобразуем номер карты в строку и извлекаем последние 4 цифры
    transactions.loc[:, "last_digits"] = transactions["Номер карты"].astype(str).str[-4:]

    # Группируем транзакции по последним 4 цифрам номера карты
    grouped = transactions.groupby("last_digits").agg(
        amount=('Сумма операции', 'sum'),  # Суммируем сумму операции
        cashback=('Кэшбэк', 'sum')  # Суммируем кешбэк
    ).reset_index()

    # Преобразуем данные в список словарей
    card_data = grouped.to_dict(orient="records")

    return card_data


def get_top_transactions(transactions: pd.DataFrame) -> list:
    """Возвращает топ-5 транзакций по сумме."""
    # Сортируем транзакции по сумме в порядке убывания и берем первые 5
    top_transactions = transactions.sort_values(by="Сумма операции", ascending=False).head(5)

    # Формируем список словарей для вывода с преобразованием даты в строку
    return [
        {
            "date": row["Дата операции"].strftime("%Y-%m-%d %H:%M:%S") if pd.notna(row["Дата операции"]) else None,
            "amount": row["Сумма операции"],
            "description": row.get("Описание", "")
        }
        for _, row in top_transactions.iterrows()
    ]