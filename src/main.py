from src.views import main_page_view, OPERATIONS_PATH
from src.services import analyze_cashback_categories
from src.reports import spending_by_category
from src.utils import load_transactions_from_excel
import logging


if __name__ == "__main__":
    # Вывод главной страницы
    print(main_page_view("2023-11-01 10:00:00"))

    file_path = OPERATIONS_PATH
    year = 2021
    month = 11

    # Загружаем данные из Excel
    transactions = load_transactions_from_excel(file_path)

    if not transactions.empty:
        # Выполняем анализ кешбэка по категориям
        result = analyze_cashback_categories(file_path, year, month)
        print("Отчет по кешбэку:", result)

        category = "Продукты"  # Укажите категорию для анализа
        date = "2021-11-01"  # Опциональная дата

        # Генерация и сохранение отчета по тратам по категории
        report = spending_by_category(transactions, category, date)
        print("Отчет успешно сформирован и сохранен.")
    else:
        logging.warning("Не удалось загрузить данные из Excel или файл пуст.")
