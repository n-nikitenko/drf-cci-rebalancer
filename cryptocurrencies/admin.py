from django.contrib import admin

from cryptocurrencies.models import CryptoCurrency, Constituent


@admin.register(CryptoCurrency)
class CryptoCurrencyAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    list_filter = ("name",)
    search_fields = ("name",)


@admin.register(Constituent)
class ConstituentAdmin(admin.ModelAdmin):
    list_display = ("id", "cryptocurrency_name", "date")
    search_fields = ("cryptocurrency__name", "date", "weight")
    ordering = ("cryptocurrency__name", "date", "weight")

    def cryptocurrency_name(self, obj):
        return obj.cryptocurrency.name

    cryptocurrency_name.short_description = CryptoCurrency._meta.get_field('name').verbose_name.title()
