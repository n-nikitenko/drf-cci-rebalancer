from django.core.management import BaseCommand

from cryptocurrencies.services import fetch_cryptocurrencies_top, fetch_cryptocurrency_prices


class Command(BaseCommand):
    help = 'получает от conmarketcap данные с ценами 200 монет'

    def handle(self, *args, **options):
        success, result = fetch_cryptocurrency_prices()
        if success:
            self.stdout.write(self.style.SUCCESS(result))
        else:
            self.stdout.write(self.style.ERROR(result))
