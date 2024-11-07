from django.contrib import admin

from cryptocurrencies.models import CryptoCurrency, Constituent


@admin.register(CryptoCurrency)
class CryptoCurrencyAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "cmc_id", "cmc_rank", "price", "price_last_updated")
    list_filter = ("name",)
    search_fields = ("name",)

    def price_last_updated(self, obj):
        return obj.price.last_updated

    price_last_updated.short_description = "Последнее обновление цены"


@admin.register(Constituent)
class ConstituentAdmin(admin.ModelAdmin):
    list_display = ("id", "cryptocurrency_name", "date")
    search_fields = ("cryptocurrency__name", "date", "weight")
    ordering = ("cryptocurrency__name", "date", "weight")

    def cryptocurrency_name(self, obj):
        return obj.cryptocurrency.name

    cryptocurrency_name.short_description = CryptoCurrency._meta.get_field('name').verbose_name.title()
