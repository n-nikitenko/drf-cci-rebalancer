import textwrap
from decimal import Decimal
from unittest.mock import patch, Mock

import requests
from django.test import TestCase, override_settings

from cryptocurrencies.models import CryptoCurrency, Constituent
from cryptocurrencies.services import update_constituents


class UpdateConstituentsTestCase(TestCase):
    """Тест-кейс для функции обновления состава индекса"""

    def setUp(self):
        # Очистка данных перед каждым тестом
        CryptoCurrency.objects.all().delete()
        Constituent.objects.all().delete()

        # Создаем некоторые криптовалюты для теста
        self.crypto1 = CryptoCurrency.objects.create(name="Bitcoin")
        self.crypto2 = CryptoCurrency.objects.create(name="Ethereum")

    @override_settings(CONSTITUENTS_URL='https://mocked_url.com')
    @patch('cryptocurrencies.services.requests.get')
    def test_update_constituents_success(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.iter_lines = lambda decode_unicode: iter([
            'Date,Coin,Weight in Index',
            '2024-11-01,Bitcoin,12.5331%',
            '2024-11-01,Ethereum,10.2453%'
        ])

        success, message = update_constituents()

        self.assertTrue(success)
        self.assertEqual(CryptoCurrency.objects.count(), 2)
        self.assertEqual(Constituent.objects.count(), 2)

    @patch('cryptocurrencies.services.requests.get')
    def test_update_constituents_no_url(self, mock_get):
        """Тест обновления состава индекса для случая, когда URL для получения данных не указан в настройках"""

        with override_settings(CONSTITUENTS_URL=None):
            success, message = update_constituents()
            self.assertFalse(success)
            self.assertEqual(message, "Ошибка: URL для получения данных не указан в настройках.")
            mock_get.assert_not_called()

    @patch('cryptocurrencies.services.requests.get')
    def test_update_constituents_request_failure(self, mock_get):
        """Тест обновления состава индекса для случая, возникновения исключения при запросе"""

        mock_get.side_effect = requests.exceptions.ConnectionError("Нет соединения")

        success, message = update_constituents()
        self.assertFalse(success)
        self.assertIn("Ошибка получения данных", message)

    @patch('cryptocurrencies.services.requests.get')
    def test_update_constituents_no_duplicate(self, mock_get):
        """Тест обновления состава индекса без сохранения дубликатов"""

        csv_data = textwrap.dedent("""\
            Date,Coin,Weight in Index
            2023-01-01,Bitcoin,50.00%
            2023-01-01,Ethereum,30.00%
            2023-01-01,Bitcoin,50.00%
        """).strip()

        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.iter_lines.return_value = iter(csv_data.splitlines())
        mock_get.return_value = mock_response

        Constituent.objects.create(date="2023-01-01", cryptocurrency=self.crypto1, weight=Decimal('50.00'))

        success, message = update_constituents()

        self.assertTrue(success)
        self.assertEqual(message, 'Данные успешно обновлены')

        self.assertEqual(Constituent.objects.filter(date="2023-01-01").count(), 2)
        self.assertEqual(
            Constituent.objects.filter(date="2023-01-01", cryptocurrency=self.crypto1, weight='50.00').count(),
            1)
        self.assertEqual(Constituent.objects.get(date="2023-01-01", cryptocurrency=self.crypto2).weight,
                         Decimal('30.00'))

    @patch('cryptocurrencies.services.requests.get')
    def test_update_constituents_response_error(self, mock_get):
        """Тест обновления состава для случая, если сервер вернул status_code != 200"""

        # Настройка мокированного ответа с ошибкой
        mock_response = Mock()
        mock_response.status_code = 404  # Имитация ошибки 404
        mock_get.return_value = mock_response

        # Вызов функции обновления
        success, message = update_constituents()

        # Проверка результатов
        self.assertFalse(success)
        self.assertEqual(message, 'Ошибка получения данных: код ответа 404')
