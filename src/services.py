import json
import logging
from datetime import datetime
from itertools import groupby

# Настройка логгирования
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


# Фильтрация транзакций по дате
def filter_transactions_by_date(transactions, year, month):
    """Фильтрует транзакции по указанному году и месяцу."""
    return filter(lambda t: datetime.fromisoformat(t["date"]).year == year
        and datetime.fromisoformat(t["date"]).month == month,transactions,
    )


# Рассчёт кешбэка
def calculate_cashback(amount, rate=0.01):
    """Вычисляет кешбэк по сумме и проценту."""
    return amount * rate


# Группировка и суммирование кешбэка по категориям
def summarize_cashback_by_category(transactions):
    """Возвращает словарь с суммой кешбэка для каждой категории."""
    grouped_transactions = groupby(
        sorted(transactions, key=lambda x: x["category"]), key=lambda x: x["category"]
    )
    return {
        category: sum(calculate_cashback(t["amount"]) for t in trans)
        for category, trans in grouped_transactions
    }


def analyze_cashback_categories(data, year, month):
    """
    Анализирует транзакции и возвращает сумму кешбэка по категориям за указанный месяц и год.

    :param data: список транзакций (словарь с ключами date, category, amount)
    :param year: год для анализа
    :param month: месяц для анализа
    :return: JSON с анализом кешбэка по категориям
    """
    logger.info(f"Начало анализа кешбэка за {year}-{month}")

    # Отфильтровать транзакции за указанный месяц и год
    filtered_transactions = filter_transactions_by_date(data, year, month)

    # Подсчитать кешбэк по категориям
    cashback_summary = summarize_cashback_by_category(filtered_transactions)

    logger.info("Анализ завершён")
    return json.dumps(cashback_summary, ensure_ascii=False, indent=4)

