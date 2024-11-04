import json

from src.services import analyze_cashback_categories


def test_analyze_cashback_categories():
    transactions_data = [
        {"date": "2023-05-01T12:45:00", "category": "Супермаркеты", "amount": 1200},
        {"date": "2023-05-03T08:20:00", "category": "Рестораны", "amount": 500},
        {"date": "2023-05-05T18:30:00", "category": "Супермаркеты", "amount": 1300},
        {"date": "2023-05-07T20:45:00", "category": "Кино", "amount": 200},
        {"date": "2023-04-15T14:00:00", "category": "Рестораны", "amount": 600},
    ]

    expected_result = {
        "Супермаркеты": 25.0,  # 2500 * 0.01
        "Рестораны": 5.0,  # 500 * 0.01
        "Кино": 2.0,  # 200 * 0.01
    }

    result = analyze_cashback_categories(transactions_data, 2023, 5)
    assert json.loads(result) == expected_result
