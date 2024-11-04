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

def load_transactions_from_excel(file_path: str) -> list:
    """Загружает транзакции из Excel файла."""
    try:
        data = pd.read_excel(file_path, engine='openpyxl')
        return data.to_dict(orient="records")  # Преобразуем в список словарей
    except Exception as e:
        logging.error(f"Ошибка при загрузке транзакций из Excel: {e}")
        return []

def get_card_data(transactions: list) -> list:
    """Возвращает информацию о картах на основе данных транзакций."""
    cards = {}
    for transaction in transactions:
        card_number = transaction.get("card_number")
        amount = transaction.get("amount", 0)

        if card_number not in cards:
            cards[card_number] = {"total_spent": 0, "transactions": []}

        cards[card_number]["total_spent"] += amount
        cards[card_number]["transactions"].append(amount)

    card_data = []
    for card_number, data in cards.items():
        cashback = round(data["total_spent"] * 0.01, 2)  # 1% кэшбэк
        card_data.append({
            "last_digits": str(card_number)[-4:],  # Последние 4 цифры номера карты
            "total_spent": round(data["total_spent"], 2),  # Общая сумма
            "cashback": cashback  # Кэшбек
        })
    return card_data

def get_top_transactions(transactions: list) -> list:
    """Возвращает топ-5 транзакций по сумме."""
    top_transactions = sorted(transactions, key=lambda x: x["amount"], reverse=True)[:5]
    return [{"date": t["date"], "amount": t["amount"], "description": t["description"]} for t in top_transactions]
