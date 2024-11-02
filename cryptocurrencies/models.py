from django.db import models

from cryptocurrencies.validators import validate_percentage


class CryptoCurrency(models.Model):
    """Модель для хранения данных криптовалюты."""
    name = models.CharField(max_length=100, unique=True, verbose_name="название",
                            help_text="Укажите название криптовалюты")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Криптовалюта"
        verbose_name_plural = "Криптовалюты"


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
