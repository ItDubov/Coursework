import pytest
import requests
from unittest import mock
from src.external_api import get_currency_rates, get_stock_prices


# Тестирование функции get_currency_rates
@pytest.fixture
def mock_currency_response():
    """Фикстура для мокирования ответа API для курсов валют."""
    return {
        "USD": {"currency": "USD", "rate_in_rub": 75.5},
        "EUR": {"currency": "EUR", "rate_in_rub": 85.0}
    }


def test_get_currency_rates_success():
    """Тестирование успешного получения курсов валют."""
    currencies = ["USD", "EUR"]

    with mock.patch('requests.get') as mock_get:
        # Создаем ответ для mock
        mock_response = mock.Mock()
        mock_response.raise_for_status = mock.Mock()
        mock_response.json.return_value = {
            "conversion_rates": {"RUB": 75.5}
        }
        mock_get.return_value = mock_response

        result = get_currency_rates(currencies)

        assert len(result) == len(currencies)
        assert result[0]["currency"] == "USD"
        assert result[0]["rate_in_rub"] is not None
        assert result[1]["currency"] == "EUR"
        assert result[1]["rate_in_rub"] is not None


def test_get_currency_rates_api_error():
    """Тестирование ошибки при получении данных с API для курсов валют."""
    currencies = ["USD", "EUR"]

    with mock.patch('requests.get') as mock_get:
        # Симулируем ошибку при запросе (например, 404 или сеть недоступна)
        mock_get.side_effect = requests.exceptions.RequestException("API error")

        result = get_currency_rates(currencies)

        assert len(result) == len(currencies)
        assert result[0]["currency"] == "USD"
        assert result[0]["rate_in_rub"] is None
        assert result[1]["currency"] == "EUR"
        assert result[1]["rate_in_rub"] is None


def test_get_currency_rates_missing_rub_rate():
    """Тестирование случая, когда в API нет курса RUB для валюты."""
    currencies = ["USD", "EUR"]

    with mock.patch('requests.get') as mock_get:
        mock_response = mock.Mock()
        mock_response.raise_for_status = mock.Mock()
        mock_response.json.return_value = {
            "conversion_rates": {}  # Нет курса RUB
        }
        mock_get.return_value = mock_response

        result = get_currency_rates(currencies)

        assert len(result) == len(currencies)
        assert result[0]["currency"] == "USD"
        assert result[0]["rate_in_rub"] is None
        assert result[1]["currency"] == "EUR"
        assert result[1]["rate_in_rub"] is None


# Тестирование функции get_stock_prices
@pytest.fixture
def mock_stock_response():
    """Фикстура для мокирования ответа API для цен акций."""
    return {
        "AAPL": {"stock": "AAPL", "price": 150.25},
        "GOOG": {"stock": "GOOG", "price": 2800.75}
    }


def test_get_stock_prices_success():
    """Тестирование успешного получения цен акций."""
    stocks = ["AAPL", "GOOG"]

    with mock.patch('requests.get') as mock_get:
        # Создаем ответ для mock
        mock_response = mock.Mock()
        mock_response.raise_for_status = mock.Mock()
        mock_response.json.return_value = {
            "c": 150.25  # Цена акции для одного из тестов
        }
        mock_get.return_value = mock_response

        result = get_stock_prices(stocks)

        assert len(result) == len(stocks)
        assert result[0]["stock"] == "AAPL"
        assert result[0]["price"] is not None
        assert result[1]["stock"] == "GOOG"
        assert result[1]["price"] is not None


def test_get_stock_prices_api_error():
    """Тестирование ошибки при получении данных с API для цен акций."""
    stocks = ["AAPL", "GOOG"]

    with mock.patch('requests.get') as mock_get:
        # Симулируем ошибку при запросе (например, 404 или сеть недоступна)
        mock_get.side_effect = requests.exceptions.RequestException("API error")

        result = get_stock_prices(stocks)

        assert len(result) == len(stocks)
        assert result[0]["stock"] == "AAPL"
        assert result[0]["price"] is None
        assert result[1]["stock"] == "GOOG"
        assert result[1]["price"] is None


def test_get_stock_prices_missing_price():
    """Тестирование случая, когда в API нет цены для акции."""
    stocks = ["AAPL", "GOOG"]

    with mock.patch('requests.get') as mock_get:
        mock_response = mock.Mock()
        mock_response.raise_for_status = mock.Mock()
        mock_response.json.return_value = {}  # Нет цены
        mock_get.return_value = mock_response

        result = get_stock_prices(stocks)

        assert len(result) == len(stocks)
        assert result[0]["stock"] == "AAPL"
        assert result[0]["price"] is None
        assert result[1]["stock"] == "GOOG"
        assert result[1]["price"] is None
