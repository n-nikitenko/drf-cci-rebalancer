from django.db import models

from cryptocurrencies.validators import validate_percentage


class CryptoCurrency(models.Model):
    """Модель для хранения данных криптовалюты."""
    name = models.CharField(max_length=100, unique=True, verbose_name="название",
                            help_text="Укажите название криптовалюты")
    symbol = models.CharField(max_length=10, unique=True, null=True, blank=True, verbose_name="CoinMarketCap символ", )
    cmc_id = models.IntegerField(unique=True, null=True, blank=True, verbose_name="CoinMarketCap ID", )
    cmc_rank = models.IntegerField(verbose_name="Ранг на CoinMarketCap", null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Криптовалюта"
        verbose_name_plural = "Криптовалюты"


class CCPrice(models.Model):
    """Модель для хранения информации о цене криптовалюты."""
    cryptocurrency = models.OneToOneField(CryptoCurrency, on_delete=models.CASCADE, related_name='price',
                                          verbose_name="Криптовалюта")
    price_usd = models.DecimalField(max_digits=20, decimal_places=8, verbose_name="Цена в USD")
    last_updated = models.DateTimeField(null=True, blank=True, verbose_name="Время последнего обновления")

    def __str__(self):
        return f"{self.price_usd}"

    class Meta:
        verbose_name = "Цена криптовалюты в USD"
        verbose_name_plural = "Цены криптовалют в USD"
        ordering = ['-last_updated']


class Constituent(models.Model):
    """Модель для хранения состава индекса CCI30."""
    date = models.DateField(verbose_name="дата",
                            help_text="Укажите дату")
    cryptocurrency = models.ForeignKey(CryptoCurrency, on_delete=models.CASCADE, verbose_name="криптовалюта",
                                       help_text="Укажите криптовалюту")
    weight = models.DecimalField(max_digits=10, decimal_places=8, verbose_name="вес в процентах",
                                 help_text="Укажите вес криптовалюты в процентах", validators=[validate_percentage])

    class Meta:
        unique_together = ('date', 'cryptocurrency', 'weight')
        verbose_name = "Состав индекса CCI30"
        verbose_name_plural = "Состав индекса CCI30"

    def __str__(self):
        return f"{self.cryptocurrency.name} - {self.weight}% на {self.date}"
