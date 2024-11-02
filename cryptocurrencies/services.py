import csv
from datetime import datetime
from decimal import Decimal
from typing import Tuple

import requests

from django.conf import settings
from cryptocurrencies.models import Constituent, CryptoCurrency


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
