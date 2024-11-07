import pandas as pd

from src.reports import spending_by_category


def test_spending_by_category():
    data = {
        "date": ["2023-08-15", "2023-07-10", "2023-09-05", "2023-09-20", "2023-06-25"],
        "category": [
            "Супермаркеты",
            "Супермаркеты",
            "Рестораны",
            "Супермаркеты",
            "Рестораны",
        ],
        "amount": [1500, 700, 800, 250, 650],
    }
    df = pd.DataFrame(data)
    df["date"] = pd.to_datetime(df["date"])

    # Проверка фильтрации по категории и дате
    result = spending_by_category(df, "Супермаркеты", "2023-09-30")
    assert len(result) == 3
    assert all(result["category"] == "Супермаркеты")
    assert result["amount"].sum() == 2450
