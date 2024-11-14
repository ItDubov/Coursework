import unittest
import pandas as pd
from datetime import datetime
from unittest.mock import patch
import json
import os
from src.utils import (
    get_greeting,
    load_transactions_from_excel,
    load_user_settings,
    get_card_data,
    get_top_transactions
)


class TestFunctions(unittest.TestCase):

    @patch("src.utils.datetime")
    def test_get_greeting(self, mock_datetime):
        """Тест для функции get_greeting."""
        # Мокаем текущее время: утро
        mock_datetime.now.return_value = datetime(2024, 1, 1, 8, 0, 0)
        self.assertEqual(get_greeting(), "Доброе утро")

        # Мокаем текущее время: день
        mock_datetime.now.return_value = datetime(2024, 1, 1, 14, 0, 0)
        self.assertEqual(get_greeting(), "Добрый день")

        # Мокаем текущее время: вечер
        mock_datetime.now.return_value = datetime(2024, 1, 1, 19, 0, 0)
        self.assertEqual(get_greeting(), "Добрый вечер")

        # Мокаем текущее время: ночь
        mock_datetime.now.return_value = datetime(2024, 1, 1, 2, 0, 0)
        self.assertEqual(get_greeting(), "Доброй ночи")

    def test_load_transactions_from_excel(self):
        """Тест для функции load_transactions_from_excel."""
        # Создаем временный Excel файл с фиктивными данными
        file_path = "test_transactions.xlsx"
        data = {
            "Дата операции": ["01.01.2024 10:00:00", "02.01.2024 11:00:00"],
            "Сумма операции": [-100, -200],
            "Номер карты": ["1234567812345678", "8765432187654321"],
            "Кэшбэк": [1, 2]
        }
        df = pd.DataFrame(data)
        df.to_excel(file_path, index=False, engine="openpyxl")

        # Проверка загрузки данных
        loaded_df = load_transactions_from_excel(file_path)
        self.assertFalse(loaded_df.empty)
        self.assertEqual(len(loaded_df), 2)

        # Удаляем временный файл после теста
        os.remove(file_path)

    def test_load_user_settings(self):
        """Тест для функции load_user_settings."""
        # Создаем временный JSON файл с фиктивными данными
        file_path = "test_user_settings.json"
        settings = {"currency": "USD", "theme": "dark"}
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(settings, f)

        # Проверка загрузки настроек
        loaded_settings = load_user_settings(file_path)
        self.assertEqual(loaded_settings["currency"], "USD")
        self.assertEqual(loaded_settings["theme"], "dark")

        # Удаляем временный файл после теста
        os.remove(file_path)

    def test_get_card_data(self):
        """Тест для функции get_card_data."""
        data = {
            "Дата операции": [datetime(2024, 1, 1), datetime(2024, 1, 2)],
            "Сумма операции": [-100, -200],
            "Номер карты": ["1234567812345678", "8765432187654321"],
            "Кэшбэк": [1, 2]
        }
        df = pd.DataFrame(data)
        card_data = get_card_data(df)

        # Сортируем card_data по последним цифрам карты для сравнения
        card_data_sorted = sorted(card_data, key=lambda x: x["last_digits"])
        expected_data = [
            {"last_digits": "4321", "amount": -200, "cashback": 2},
            {"last_digits": "5678", "amount": -100, "cashback": 1}
        ]
        expected_data_sorted = sorted(expected_data, key=lambda x: x["last_digits"])

        self.assertEqual(card_data_sorted, expected_data_sorted)

    def test_get_top_transactions(self):
        """Тест для функции get_top_transactions."""
        data = {
            "Дата операции": [datetime(2024, 1, 1), datetime(2024, 1, 2), datetime(2024, 1, 3)],
            "Сумма операции": [300, 200, 100],
            "Описание": ["Оплата 1", "Оплата 2", "Оплата 3"]
        }
        df = pd.DataFrame(data)
        top_transactions = get_top_transactions(df)
        self.assertEqual(len(top_transactions), 3)
        self.assertEqual(top_transactions[0]["amount"], 300)
        self.assertEqual(top_transactions[1]["description"], "Оплата 2")
