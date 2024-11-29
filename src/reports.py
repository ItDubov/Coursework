import logging
from datetime import datetime, timedelta
from functools import wraps
from typing import Optional, Callable
import pandas as pd

# Настройка логирования
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def save_report(filename: Optional[str] = None) -> Callable:
    """Декоратор для сохранения отчета в файл.

    :param filename: Имя файла для сохранения отчета (опционально)
    :return: Декорированная функция
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)

            # Используем имя файла по умолчанию, если не указано
            report_filename = filename or f"report_{func.__name__}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

            # Сохранение результата в файл
            result.to_json(report_filename, orient="records", force_ascii=False, indent=4)
            logger.info(f"Отчет сохранен в файл: {report_filename}")

            return result

        return wrapper

    # Если декоратор вызывается без скобок
    if callable(filename):
        return decorator(filename)

    return decorator


# Пример использования с указанным именем файла
@save_report("output.json")
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
        (transactions["Категория"] == category)
        & (transactions["Дата операции"] >= start_date)
        & (transactions["Дата операции"] <= date)
    ]

    # Логирование информации
    logger.info(
        f"Формирование отчета по категории '{category}' "
        f"за период с {start_date.strftime('%Y-%m-%d')} по {date.strftime('%Y-%m-%d')}"
    )

    return filtered_transactions
