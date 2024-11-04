import datetime

from src.main import get_data_json, get_greeting


def test_get_greeting():
    assert get_greeting(datetime.datetime(2021, 12, 21, 8)) == "Доброе утро"
    assert get_greeting(datetime.datetime(2021, 12, 21, 13)) == "Добрый день"
    assert get_greeting(datetime.datetime(2021, 12, 21, 19)) == "Добрый вечер"
    assert get_greeting(datetime.datetime(2021, 12, 21, 23)) == "Доброй ночи"


def test_get_data_json():
    result = get_data_json("2021-12-21 13:45:00")
    assert "greeting" in result
    assert "cards" in result
    assert "top_transactions" in result
    assert "currency_rates" in result
    assert "stock_prices" in result
