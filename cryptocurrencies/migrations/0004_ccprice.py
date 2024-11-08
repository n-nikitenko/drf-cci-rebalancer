# Generated by Django 4.2.9 on 2024-11-06 12:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        (
            "cryptocurrencies",
            "0003_cryptocurrency_cmc_id_cryptocurrency_cmc_rank_and_more",
        ),
    ]

    operations = [
        migrations.CreateModel(
            name="CCPrice",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "price_usd",
                    models.DecimalField(
                        decimal_places=8, max_digits=20, verbose_name="Цена в USD"
                    ),
                ),
                (
                    "last_updated",
                    models.DateTimeField(
                        auto_now=True, verbose_name="Время последнего обновления"
                    ),
                ),
                (
                    "cryptocurrency",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="price",
                        to="cryptocurrencies.cryptocurrency",
                        verbose_name="Криптовалюта",
                    ),
                ),
            ],
            options={
                "verbose_name": "Цена криптовалюты",
                "verbose_name_plural": "Цены криптовалют",
                "ordering": ["-last_updated"],
            },
        ),
    ]
