# CCI Rebalancer

Проект DRF CCI Rebalancer предназначен для хранения и обновления состава индекса CCI30. Состав обновляется автоматически
через GET-запрос к API, после чего данные сохраняются в базе данных, работающей в Docker-контейнере.

## Основные технологии

- **Django** — фреймворк для разработки веб-приложений.
- **Django REST Framework** — для создания REST API.
- **PostgreSQL** — база данных, работающая в Docker-контейнере.
- **Poetry** — менеджер зависимостей Python.
- **requests** - библиотека для отправки запросов
- **Docker Compose**  - для контейниризации

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
      poetry run python manage.py fetch_cc_top
   ```

5. Получение списка с ценами 200 монет в USD от CoinMarketCap:

   ```commandline
      poetry run python manage.py fetch_cc_prices
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
