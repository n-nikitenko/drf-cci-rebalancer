# CCI Rebalancer

DRF CCI Rebalancer  - приложение для хранения и автоматического обновления данных о составе индекса CCI30 и актуальных ценах на криптовалюты. Проект поддерживает консолидацию данных из нескольких источников: CCI30 и CoinMarketCap. Это позволяет получать и обновлять информацию о топовых криптовалютах и их ценах, обеспечивая точность и полноту данных.

Приложение интегрировано с внешними API и использует периодические задачи с помощью Celery и Redis для автоматического обновления данных. Ежедневно обновляется список криптовалют, входящих в индекс, а почасовые задачи поддерживают актуальные данные о ценах.

## Основные особенности
- Команда для обновления состава индекса CCI30: Данные обновляются через запросы к API и сохраняются в базе данных.
- Актуальные цены на криптовалюты: 
  - обновление данных о криптовалютах из CoinMarketCap API каждые сутки.
  - обновление цен на криптовалюты из CoinMarketCap API каждый час.
- Консолидация данных из нескольких источников (CoinMarketCap и CCI30): совмещение информации о криптовалютах по id и названию.
- Docker-контейнеризация: приложение развёрнуто в изолированных контейнерах, что упрощает развертывание.

## Основные технологии

- **Django** — фреймворк для разработки веб-приложений.
- **Django REST Framework** — для создания REST API.
- **PostgreSQL** — база данных для хранения информации о криптовалютах и их ценах.
- **Poetry** — менеджер зависимостей Python.
- **requests** — библиотека для HTTP-запросов, используется для работы с внешними API
- **Docker** — контейнеризация приложения
- **Gunicorn** — WSGI сервер для запуска Django-приложения 
- **Nginx** — прокси-сервер для обработки запросов к приложению и статики
- **Docker Compose**  - оркестрация контейнеров, обеспечивает совместный запуск сервисов (база данных, брокер сообщений, веб-сервер)
- **Celery** — асинхронный планировщик задач (используется для периодических обновлений данных).
- **Celery Beat** — расширение для Celery, предназначенное для планирования и запуска периодических задач
- **Redis** — брокер сообщений для Celery, обеспечивает хранение задач в очереди
- **pytest** — библиотека для тестирования

## Установка и запуск проекта

1. **Клонируйте репозиторий**:
   ```bash
   git clone <URL репозитория>
   cd <название проекта>
2. Создайте файл .env в корне проекта, где укажите переменные окружения
3. Установите зависимости с помощью Poetry:
   ```poetry install```
4. Запустите контейнеры Docker:
    ```
    docker compose up -d
    ```
5. Сервис доступен по адресу: http://localhost:8080/

## Основные команды

1. Для создания суперпользователя выполните команду:
   ```commandline
   poetry run python manage.py createsuperuser
   ```
   После выполнения команды следуйте инструкциям для задания email и пароля суперпользователя.
2. Чтобы обновить состав индекса вручную, выполните команду:
   ```commandline
   poetry run python manage.py update_constituents
   ```
   Эта команда отправляет запрос к API (ссi30.com) и обновляет данные о составе индекса CCI30 в базе данных.
3. Запуск сервера:
   ```commandline
   poetry run python manage.py runserver localhost:8080
   ```
4. Проверка степени покрытия тестами (linux):
   ```commandline
           coverage run --source='.' manage.py test 
           coverage html  
   ```
5. Получение списка из 200 монет, отсортированных по cmc_rank от CoinMarketCap:

   ```commandline
      poetry run python manage.py update_cc_top
   ```

5. Получение списка с ценами 200 монет в USD от CoinMarketCap:

   ```commandline
      poetry run python manage.py update_cc_prices
     ```

## Документация

Документация сгенерирована автоматически и доступна по адресу:
http://localhost:8080/

## Админ-панель

http://localhost:8080/admin/

## Модели

### CryptoCurrency

<table>
    <thead>
    <tr>
        <th><strong>Поле</strong></th>
        <th><strong>Тип</strong></th>
        <th><strong>Описание</strong></th>
    </tr>
    </thead>
    <tbody>
    <tr>
        <td><code>name</code></td>
        <td><code>CharField</code></td>
        <td>Уникальное название криптовалюты</td>
    </tr>  
    <tr>
        <td><code>cmc_id</code></td>
        <td><code>IntegerField</code></td>
        <td>Id криптовалюты на CoinMarketCap</td>
    </tr>
    <tr>
        <td><code>cmc_rank</code></td>
        <td><code>IntegerField</code></td>
        <td>Ранг криптовалюты на CoinMarketCap</td>
    </tr>
    <tr>
        <td><code>symbol</code></td>
        <td><code>CharField</code></td>
        <td>Символ криптовалюты на CoinMarketCap</td>
    </tr>
    <tr>
        <td><code>symbol</code></td>
        <td><code>CharField</code></td>
        <td>Символ криптовалюты на CoinMarketCap</td>
    </tr>
    </tbody>
</table>

### СС_Price

<table>
    <thead>
    <tr>
        <th><strong>Поле</strong></th>
        <th><strong>Тип</strong></th>
        <th><strong>Описание</strong></th>
    </tr>
    </thead>
    <tbody>
    <tr>
        <td><code>last_updated</code></td>
        <td><code>DateTimeField</code></td>
        <td>Время последнего обновления</td>
    </tr>
    <tr>
        <td><code>cryptocurrency</code></td>
        <td><code>OneToOneField</code></td>
        <td>Ссылка на криптовалюту (<code>CryptoCurrency</code>)</td>
    </tr>
    <tr>
        <td><code>price_usd</code></td>
        <td><code>DecimalField</code></td>
        <td>Цена криптовалюты в USD</td>
    </tr>
    </tbody>
</table>

### Constituent

<table>
    <thead>
    <tr>
        <th><strong>Поле</strong></th>
        <th><strong>Тип</strong></th>
        <th><strong>Описание</strong></th>
    </tr>
    </thead>
    <tbody>
    <tr>
        <td><code>date</code></td>
        <td><code>DateField</code></td>
        <td>Дата</td>
    </tr>
    <tr>
        <td><code>cryptocurrency</code></td>
        <td><code>ForeignKey</code></td>
        <td>Ссылка на криптовалюту (<code>CryptoCurrency</code>)</td>
    </tr>
    <tr>
        <td><code>weight</code></td>
        <td><code>DecimalField</code></td>
        <td>Вес криптовалюты в индексе (в процентах)</td>
    </tr>
    </tbody>
</table>
