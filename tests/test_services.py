import pytest
import json
import pandas as pd
from src.services import filter_transactions_by_date, calculate_cashback, summarize_cashback_by_category, \
    analyze_cashback_categories


# Пример данных для использования в тестах
@pytest.fixture
def sample_transactions():
    data = {
        "Дата операции": [
            "2023-01-10", "2023-02-15", "2023-02-20", "2023-03-05"
        ],
        "Сумма операции": [100.0, -50.0, 200.0, -150.0],
        "Категория": ["Еда", "Еда", "Транспорт", "Еда"]
    }
    transactions = pd.DataFrame(data)
    transactions["Дата операции"] = pd.to_datetime(transactions["Дата операции"])
    return transactions


# Тест для filter_transactions_by_date
def test_filter_transactions_by_date(sample_transactions):
    year = 2023
    month = 2
    filtered = filter_transactions_by_date(sample_transactions, year, month)

    # Проверяем, что результат является DataFrame
    assert isinstance(filtered, pd.DataFrame)

    # Проверяем, что возвращены только транзакции за февраль 2023 года
    assert len(filtered) == 2
    assert all(filtered["Дата операции"].dt.year == year)
    assert all(filtered["Дата операции"].dt.month == month)


# Тест для calculate_cashback
def test_calculate_cashback():
    amount = 100.0
    rate = 0.01
    cashback = calculate_cashback(amount, rate)

    # Проверяем, что кешбэк рассчитан правильно
    assert cashback == 1.0


# Тест для summarize_cashback_by_category
def test_summarize_cashback_by_category(sample_transactions):
    summary = summarize_cashback_by_category(sample_transactions)

    # Проверяем, что результат является словарем
    assert isinstance(summary, dict)

    # Проверяем, что суммы кешбэка правильные
    expected_summary = {
        "Еда": (calculate_cashback(100.0) + calculate_cashback(-50.0) + calculate_cashback(-150.0)),
        "Транспорт": calculate_cashback(200.0)
    }
    assert summary == expected_summary


def test_analyze_cashback_categories(tmpdir, sample_transactions, mocker):
    # Мокаем функцию load_transactions_from_excel с правильным путем
    mock_load = mocker.patch('src.services.load_transactions_from_excel', return_value=sample_transactions)

    # Печать, чтобы увидеть, был ли вызов
    print("Mock called before function call:", mock_load.called)

    # Создаем временный путь к файлу
    file_path = tmpdir.join("dummy.xlsx")
    file_path.write("")

    # Вызываем функцию analyze_cashback_categories
    result_json = analyze_cashback_categories(str(file_path), 2023, 2)

    # Печать, чтобы увидеть, был ли вызов после выполнения функции
    print("Mock called after function call:", mock_load.called)

    # Преобразуем результат в словарь
    result = json.loads(result_json)

    # Проверяем, что результат является словарем и содержит ожидаемые ключи
    assert isinstance(result, dict)
    assert "Еда" in result
    assert "Транспорт" in result
