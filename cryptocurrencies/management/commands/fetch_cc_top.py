from django.core.management import BaseCommand

from cryptocurrencies.services import fetch_cryptocurrencies_top


class Command(BaseCommand):
    help = 'получает от conmarketcap 200 монет с начала списка, отсортированного по cmc_rank'

    def handle(self, *args, **options):
        success, result = fetch_cryptocurrencies_top()
        if success:
            self.stdout.write(self.style.SUCCESS(result))
        else:
            self.stdout.write(self.style.ERROR(result))
