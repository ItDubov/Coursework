def get_card_data():
    """Возвращает данные по картам:
    последние 4 цифры, сумма расходов и кешбэк.
    """
    # Пример данных
    cards = [
        {"card_number": "1234567812345814",
         "transactions": [-500, -200, -300, 1000]},
        {"card_number": "1234567812347512",
         "transactions": [-50, -20, -10, 100]}
    ]

    card_data = []
    for card in cards:
        last_digits = card["card_number"][-4:]
        total_spent = sum(t for t in card["transactions"] if t < 0)
        cashback = abs(total_spent) * 0.01
        card_data.append({
            "last_digits": last_digits,
            "total_spent": round(total_spent, 2),
            "cashback": round(cashback, 2)
        })
    return card_data


def get_top_transactions():

    """Возвращает топ-5 транзакций по сумме."""

    # Пример транзакций

    transactions = [
        {"date": "2021-12-21",
         "amount": 1198.23,
         "category": "Переводы",
         "description": "Перевод Кредитная карта"},
        {"date": "2021-12-20",
         "amount": 829.00,
         "category": "Супермаркеты",
         "description": "Лента"},
        {"date": "2021-12-20",
         "amount": 421.00,
         "category": "Различные товары",
         "description": "Ozon.ru"},
        {"date": "2021-12-16",
         "amount": -14216.42,
         "category": "ЖКХ",
         "description": "ЖКУ Квартира"},
        {"date": "2021-12-16",
         "amount": 453.00,
         "category": "Бонусы",
         "description": "Кешбэк за обычные покупки"}
    ]
    # Сортировка по убыванию суммы и выбор топ-5
    sorted_transactions = sorted(transactions, key=lambda x: abs(x["amount"]), reverse=True)[:5]
    return sorted_transactions
