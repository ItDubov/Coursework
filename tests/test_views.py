import pytest
import pandas as pd
from unittest.mock import patch
from src.views import convert_timestamps_to_strings, filter_transactions, main_page_view
import json


@pytest.fixture
def sample_transactions():
    """Создаем фикстуру с примерными данными транзакций."""
    data = {
        "Дата операции": [
            "2023-01-10 10:00:00", "2023-02-15 14:30:00", "2023-03-20 16:45:00", "2023-04-05 09:00:00"
        ],
        "Сумма операции": [100, -50, 200, -300],
        "Категория": ["Еда", "Еда", "Транспорт", "Еда"]
    }
    transactions = pd.DataFrame(data)
    transactions["Дата операции"] = pd.to_datetime(transactions["Дата операции"])
    return transactions


def test_convert_timestamps_to_strings():
    """Тестируем функцию convert_timestamps_to_strings."""
    sample_data = {
        "Дата операции": pd.to_datetime("2023-01-10 10:00:00"),
        "Сумма операции": 100,
        "Категория": "Еда"
    }

    result = convert_timestamps_to_strings(sample_data)

    # Проверка, что дата была преобразована в строку
    assert isinstance(result["Дата операции"], str)
    assert result["Дата операции"] == "2023-01-10 10:00:00"


def test_filter_transactions(sample_transactions):
    """Тестируем функцию фильтрации транзакций."""
    date_time_str = "2023-02-15 14:30:00"
    filtered = filter_transactions(sample_transactions, date_time_str)

    # Проверяем, что после фильтрации осталась только одна транзакция
    assert len(filtered) == 1
    assert filtered["Дата операции"].iloc[0] == pd.to_datetime(date_time_str)


@patch("src.views.get_card_data")
@patch("src.views.get_top_transactions")
@patch("src.views.get_currency_rates")
@patch("src.views.get_stock_prices")
@patch("src.views.load_user_settings")
@patch("src.views.get_greeting", return_value="Привет, тестировщик!")
def test_main_page_view(
        mock_get_greeting, mock_load_user_settings, mock_get_stock_prices, mock_get_currency_rates,
        mock_get_top_transactions, mock_get_card_data, sample_transactions
):
    """Тестируем основную логику работы main_page_view."""

    # Мокаем функции для предотвращения реальных внешних вызовов
    mock_get_card_data.return_value = [{"card_name": "Test Card", "balance": 1000}]
    mock_get_top_transactions.return_value = [{"transaction": "Test transaction", "amount": 200}]
    mock_get_currency_rates.return_value = [{"currency": "USD", "rate": 75}]
    mock_get_stock_prices.return_value = [{"stock": "AAPL", "price": 150}]
    mock_load_user_settings.return_value = {
        "currencies": ["USD"],
        "stocks": ["AAPL"]
    }

    # Заменяем sample_transactions на mоки
    with patch("pandas.read_excel", return_value=sample_transactions):
        result = main_page_view()

    # Проверка, что результат является валидным JSON
    result_data = json.loads(result)

    # Проверка, что все ключи присутствуют
    assert "greeting" in result_data
    assert "cards" in result_data
    assert "top_transactions" in result_data
    assert "currency_rates" in result_data
    assert "stock_prices" in result_data

    # Проверка корректности данных карточек
    assert len(result_data["cards"]) == 1
    assert result_data["cards"][0]["card_name"] == "Test Card"

    # Проверка корректности данных топовых транзакций
    assert len(result_data["top_transactions"]) == 1
    assert result_data["top_transactions"][0]["transaction"] == "Test transaction"

    # Проверка корректности данных валют
    assert len(result_data["currency_rates"]) == 1
    assert result_data["currency_rates"][0]["currency"] == "USD"

    # Проверка корректности данных акций
    assert len(result_data["stock_prices"]) == 1
    assert result_data["stock_prices"][0]["stock"] == "AAPL"
