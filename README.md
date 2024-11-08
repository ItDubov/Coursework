# Финансовый Анализатор

## Описание проекта

Финансовый Анализатор — это веб-приложение, разработанное для анализа и управления личными финансами. Оно предоставляет пользователям информацию о расходах, доходах, кешбэке и текущих курсах валют и ценах на акции. Основные функции приложения реализованы в виде API, который возвращает данные в формате JSON.

## Основные компоненты

### Страница «Главная»

Главная страница приложения отвечает за отображение ключевой информации о финансовом состоянии пользователя. Она включает в себя следующие элементы:

- **Приветствие**: В зависимости от времени суток отображается соответствующее приветствие:
  - "Доброе утро"
  - "Добрый день"
  - "Добрый вечер"
  - "Доброй ночи"

- **Данные по картам**:
  - Последние 4 цифры карты
  - Общая сумма расходов по каждой карте
  - Кешбэк, начисленный за расходы (1 рубль на каждые 100 рублей)

- **Топ-5 транзакций**: Представляет собой список самых крупных транзакций по сумме, включая дату, сумму, категорию и описание.

- **Курс валют**: Отображает текущие курсы популярных валют (например, USD и EUR).

- **Цены на акции**: Предоставляет информацию о текущих ценах на акции из индекса S&P500 (например, AAPL, AMZN, GOOGL и др.).

### Пример структуры JSON-ответа

Запрос к API главной страницы возвращает данные в следующем формате:

```json
{
  "greeting": "Добрый день",
  "cards": [
    {
      "last_digits": "5814",
      "total_spent": 1262.00,
      "cashback": 12.62
    },
    {
      "last_digits": "7512",
      "total_spent": 7.94,
      "cashback": 0.08
    }
  ],
  "top_transactions": [
    {
      "date": "21.12.2021",
      "amount": 1198.23,
      "category": "Переводы",
      "description": "Перевод Кредитная карта. ТП 10.2 RUR"
    },
    {
      "date": "20.12.2021",
      "amount": 829.00,
      "category": "Супермаркеты",
      "description": "Лента"
    },
    {
      "date": "20.12.2021",
      "amount": 421.00,
      "category": "Различные товары",
      "description": "Ozon.ru"
    },
    {
      "date": "16.12.2021",
      "amount": -14216.42,
      "category": "ЖКХ",
      "description": "ЖКУ Квартира"
    },
    {
      "date": "16.12.2021",
      "amount": 453.00,
      "category": "Бонусы",
      "description": "Кешбэк за обычные покупки"
    }
  ],
  "currency_rates": [
    {
      "currency": "USD",
      "rate": 73.21
    },
    {
      "currency": "EUR",
      "rate": 87.08
    }
  ],
  "stock_prices": [
    {
      "stock": "AAPL",
      "price": 150.12
    },
    {
      "stock": "AMZN",
      "price": 3173.18
    },
    {
      "stock": "GOOGL",
      "price": 2742.39
    },
    {
      "stock": "MSFT",
      "price": 296.71
    },
    {
      "stock": "TSLA",
      "price": 1007.08
    }
  ]
}
```
# Сервисы

В рамках проекта также реализованы сервисы, предназначенные для анализа финансовых данных и повышения эффективности использования кешбэка. Сервисы находятся в отдельном модуле `services.py` и используют элементы функционального программирования для более лаконичного и понятного кода.

### Анализ выгодных категорий повышенного кешбэка

Сервис предоставляет возможность анализа категорий расходов с точки зрения их выгодности для кешбэка. Основная функция сервиса позволяет оценить, какие категории могут принести наибольшую выгоду в виде кешбэка за определенный месяц и год.

#### Входные параметры функции

- `data`: Данные с транзакциями в формате JSON или в виде структуры, удобной для обработки.
- `year`: Год, за который проводится анализ (целое число).
- `month`: Месяц, за который проводится анализ (целое число).

#### Выходные параметры

Функция возвращает JSON-ответ, в котором перечислены категории расходов и соответствующие суммы кешбэка, которые можно заработать в указанный месяц:

```json
{
    "Категория 1": 1000,
    "Категория 2": 2000,
    "Категория 3": 500
}
```
### Отчеты

В рамках проекта реализованы функции для создания отчетов, которые находятся в отдельном модуле `reports.py`. Эти функции помогают пользователям отслеживать свои финансовые показатели и анализировать расходы по категориям.

#### Декоратор для функций-отчетов

Каждая функция-отчет обернута в декоратор, который автоматически записывает результаты в файл. Это позволяет сохранять результаты отчетов для последующего анализа.

- **Декоратор без параметра**: записывает данные отчета в файл с названием по умолчанию. Формат имени файла можно настроить, например, используя текущую дату и время.
  
- **Декоратор с параметром**: принимает имя файла в качестве параметра, что позволяет пользователю самостоятельно выбирать, куда сохранить отчет.

#### Траты по категории

Функция, отвечающая за анализ расходов по категориям, принимает следующие параметры:

- **transactions**: Датафрейм с транзакциями (например, созданный с помощью библиотеки pandas).
- **category**: Название категории, по которой нужно провести анализ.
- **date** (опционально): Дата, от которой начинается анализ. Если дата не передана, используется текущая дата.

##### Пример интерфейса функции

```python
def spending_by_category(transactions: pd.DataFrame,
                         category: str,
                         date: Optional[str] = None) -> pd.DataFrame:
    pass
```