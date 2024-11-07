import json
import logging
from datetime import datetime
import pandas as pd
from src.utils import load_transactions_from_excel

# Настройка логирования
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Функция для фильтрации транзакций по году и месяцу
def filter_transactions_by_date(transactions: pd.DataFrame, year: int, month: int) -> pd.DataFrame:
    """Фильтрует транзакции по указанному году и месяцу."""
    transactions["Дата операции"] = pd.to_datetime(transactions["Дата операции"], errors='coerce')
    return transactions[(transactions["Дата операции"].dt.year == year) &
                        (transactions["Дата операции"].dt.month == month)]

# Функция для расчёта кешбэка
def calculate_cashback(amount: float, rate: float = 0.01) -> float:
    """Вычисляет кешбэк по сумме и проценту."""
    return amount * rate

# Функция для группировки и суммирования кешбэка по категориям
def summarize_cashback_by_category(transactions: pd.DataFrame) -> dict:
    """
    Группирует транзакции по категориям и суммирует кешбэк.
    :param transactions: отфильтрованные транзакции
    :return: словарь с суммой кешбэка для каждой категории
    """
    cashback_summary = transactions.groupby("Категория")["Сумма операции"].apply(
        lambda x: sum(calculate_cashback(amount) for amount in x)
    ).to_dict()
    return cashback_summary

# Основная функция для анализа категорий кешбэка
def analyze_cashback_categories(file_path: str, year: int, month: int) -> str:
    """
    Анализирует транзакции и возвращает сумму кешбэка по категориям за указанный месяц и год.
    :param file_path: Путь к файлу Excel
    :param year: год для анализа
    :param month: месяц для анализа
    :return: JSON с анализом кешбэка по категориям
    """
    logger.info(f"Начало анализа кешбэка за {year}-{month}")

    # Загружаем данные из файла
    data = load_transactions_from_excel(file_path)

    if data.empty:
        logger.warning("Данные из файла Excel не загружены или файл пуст.")
        return json.dumps({}, ensure_ascii=False, indent=4)

    # Фильтруем транзакции за указанный месяц и год
    filtered_transactions = filter_transactions_by_date(data, year, month)

    if filtered_transactions.empty:
        logger.warning(f"Нет транзакций за {year}-{month}.")
        return json.dumps({}, ensure_ascii=False, indent=4)

    # Суммируем кешбэк по категориям
    cashback_summary = summarize_cashback_by_category(filtered_transactions)

    logger.info("Анализ завершён")
    return json.dumps(cashback_summary, ensure_ascii=False, indent=4)
