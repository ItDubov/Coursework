import pytest
import os
import pandas as pd
from datetime import datetime
from src.reports import save_report, spending_by_category  # Замените main_module на имя вашего модуля


# Создание фикстуры с примерными данными транзакций
@pytest.fixture
def sample_transactions():
    data = {
        "Дата операции": [
            "2023-01-10", "2023-02-15", "2023-03-20", "2023-04-05"
        ],
        "Сумма операции": [100, -50, 200, -300],
        "Категория": ["Еда", "Еда", "Транспорт", "Еда"]
    }
    transactions = pd.DataFrame(data)
    transactions["Дата операции"] = pd.to_datetime(transactions["Дата операции"])
    return transactions


# Тест функции spending_by_category
def test_spending_by_category(sample_transactions):
    category = "Еда"
    date = "2023-04-05"
    result = spending_by_category(sample_transactions, category, date)

    # Проверяем, что результат является DataFrame
    assert isinstance(result, pd.DataFrame)

    # Проверяем, что возвращаемые транзакции соответствуют категории "Еда"
    assert all(result["Категория"] == category)

    # Проверяем, что дата операций попадает в заданный диапазон
    end_date = datetime.strptime(date, "%Y-%m-%d")
    start_date = end_date - pd.Timedelta(days=90)
    assert all((result["Дата операции"] >= start_date) & (result["Дата операции"] <= end_date))


# Тест работы декоратора save_report
def test_save_report_decorator(sample_transactions):
    output_filename = "test_output.json"

    # Убедимся, что файл не существует перед тестом
    if os.path.exists(output_filename):
        os.remove(output_filename)

    # Тест функции с декоратором
    @save_report(output_filename)
    def test_function(transactions):
        return transactions

    test_function(sample_transactions)

    # Проверяем, что файл был создан
    assert os.path.exists(output_filename)

    # Загружаем данные из файла и проверяем их корректность
    saved_data = pd.read_json(output_filename)
    pd.testing.assert_frame_equal(saved_data, sample_transactions)

    # Удаляем тестовый файл после проверки
    os.remove(output_filename)
