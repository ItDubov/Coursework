import logging
from datetime import datetime, timedelta
from functools import wraps
from typing import Optional
import pandas as pd

# Настройка логгирования
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def save_report(func):
    """Декоратор для записи отчета в файл."""

    @wraps(func)
    def wrapper(*args, filename: Optional[str] = None, **kwargs):
        result = func(*args, **kwargs)

        # Имя файла по умолчанию
        if filename is None:
            filename = f"report_{func.__name__}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

        # Сохранение результата в файл
        result.to_json(filename, orient="records", force_ascii=False, indent=4)
        logger.info(f"Отчет сохранен в файл: {filename}")

        return result

    return wrapper


@save_report
def spending_by_category(
    transactions: pd.DataFrame, category: str, date: Optional[str] = None
) -> pd.DataFrame:
    """
    Возвращает траты по категории за последние три месяца от переданной даты.

    :param transactions: DataFrame с данными транзакций
    :param category: название категории для анализа
    :param date: опциональная дата (строка в формате 'YYYY-MM-DD')
    :return: DataFrame с тратами за последние три месяца по заданной категории
    """
    # Если дата не передана, берем текущую дату
    if date is None:
        date = datetime.now()
    else:
        date = datetime.strptime(date, "%Y-%m-%d")

    # Определение периода за последние три месяца
    start_date = date - timedelta(days=90)

    # Фильтрация транзакций по дате и категории
    filtered_transactions = transactions[
        (transactions["category"] == category)
        & (transactions["date"] >= start_date)
        & (transactions["date"] <= date)
    ]

    # Логирование информации
    logger.info(
        f"Формирование отчета по категории '{category}' "
        f"за период с {start_date.strftime('%Y-%m-%d')} по {date.strftime('%Y-%m-%d')}"
    )

    return filtered_transactions
