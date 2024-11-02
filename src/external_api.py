import requests


def get_currency_rates(currencies):
    """Получает курсы валют из внешнего API."""
    response = requests.get("https://api.exchangerate-api.com/v4/latest/RUB")
    if response.status_code == 200:
        data = response.json()
        rates = [{"currency": curr, "rate": data["rates"].get(curr, None)} for curr in currencies]
        return rates
    else:
        return [{"currency": curr, "rate": None} for curr in currencies]


def get_stock_prices(stocks):
    """Получает цены акций из внешнего API."""
    stock_data = []
    for stock in stocks:
        response = requests.get(f"https://finnhub.io/api/v1/quote?symbol={stock}&token=API_KEY")
        if response.status_code == 200:
            data = response.json()
            stock_data.append({"stock": stock, "price": data["c"]})
        else:
            stock_data.append({"stock": stock, "price": None})
    return stock_data
