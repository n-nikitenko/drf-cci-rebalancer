import csv
from datetime import datetime
from decimal import Decimal
from typing import Tuple

import requests
from django.conf import settings

from cryptocurrencies.models import Constituent, CryptoCurrency, CCPrice


def update_constituents() -> Tuple[bool, str]:
    url = getattr(settings, 'CONSTITUENTS_URL', None)
    if not url:
        return False, "Ошибка: URL для получения данных не указан в настройках."

    try:
        response = requests.get(url, verify=True, timeout=(3, 30), stream=True)

    except requests.exceptions.RequestException as e:
        return False, f'Ошибка получения данных: {e}'
    if response.status_code == 200:

        lines = response.iter_lines(decode_unicode=True)
        next(lines)  # first line contains headers, so skip it

        csv_reader = csv.reader(lines, delimiter=',')

        for row in csv_reader:
            date_str, name, weight_str = row
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
            weight = Decimal(weight_str.rstrip('%'))

            cryptocurrency, created = CryptoCurrency.objects.get_or_create(name=name)
            Constituent.objects.update_or_create(date=date, cryptocurrency=cryptocurrency, weight=weight)

        return True, 'Данные успешно обновлены'
    return False, f'Ошибка получения данных: код ответа {response.status_code}'


def update_cryptocurrencies_top():
    url = getattr(settings, 'COINMARKETCAP_API_MAP_URL', None)
    if not url:
        return False, "Ошибка: URL для получения данных c coinmarketcap не указан в настройках."
    key = getattr(settings, 'COINMARKETCAP_API_KEY', None)
    if not key:
        return False, "Ошибка: API KEY для получения данных c coinmarketcap не указан в настройках."
    headers = {
        "Accepts": "application/json",
        "X-CMC_PRO_API_KEY": key,
    }
    params = {
        "start": 1,
        "limit": 200,
        "sort": "cmc_rank",
    }

    try:
        response = requests.get(url, headers=headers, params=params)
    except requests.exceptions.RequestException as e:
        return False, f'Ошибка получения данных от coinmarketcap: {e}'

    if response.status_code == 200:
        data = response.json().get("data", [])
        for coin_data in data:
            cmc_id = coin_data.get('id')
            name = coin_data.get('name')
            cmc_rank = coin_data.get('rank')
            symbol = coin_data.get('symbol')

            CryptoCurrency.objects.update_or_create(
                name=name,
                defaults={
                    'cmc_id': cmc_id,
                    'symbol': symbol,
                    'cmc_rank': cmc_rank,
                }
            )
        return True, 'Данные криптовалют успешно обновлены'
    return False, f'Ошибка получения данных: код ответа {response.status_code}'


def update_cryptocurrency_prices():
    url = getattr(settings, 'COINMARKETCAP_API_PRICES_URL', None)
    if not url:
        return False, "Ошибка: URL для получения данных c coinmarketcap не указан в настройках."
    key = getattr(settings, 'COINMARKETCAP_API_KEY', None)
    if not key:
        return False, "Ошибка: API KEY для получения данных c coinmarketcap не указан в настройках."
    headers = {
        "Accepts": "application/json",
        "X-CMC_PRO_API_KEY": key,
    }
    params = {
        "start": 1,
        "limit": 200,
        "convert": "USD",
    }
    try:
        response = requests.get(url, headers=headers, params=params)
    except requests.exceptions.RequestException as e:
        return False, f'Ошибка получения данных от coinmarketcap: {e}'

    if response.status_code == 200:
        data = response.json().get("data", [])
        for coin_data in data:
            cryptocurrency, created = CryptoCurrency.objects.update_or_create(
                name=coin_data["name"],
                defaults={
                    'cmc_id': coin_data["id"],
                    'symbol': coin_data["symbol"],
                    'cmc_rank': coin_data["cmc_rank"],
                }
            )

            CCPrice.objects.update_or_create(
                cryptocurrency=cryptocurrency,
                defaults={
                    'price_usd': coin_data["quote"]["USD"]["price"],
                    'last_updated': coin_data["quote"]["USD"]["last_updated"]
                }
            )
        return True, 'Данные о ценах успешно обновлены'
    return False, f'Ошибка получения данных: код ответа {response.status_code}'
