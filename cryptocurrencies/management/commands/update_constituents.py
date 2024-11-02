from django.core.management.base import BaseCommand

from cryptocurrencies.services import update_constituents


class Command(BaseCommand):
    help = 'Обновляет состав индекса CCI30'

    def handle(self, *args, **options):
        confirmation = input("Вы уверены, что хотите обновить данные составов индекса CCI30? (yes/no): ")
        if confirmation.lower() == 'yes':
            success, message = update_constituents()
            if success:
                self.stdout.write(self.style.SUCCESS(message))
            else:
                self.stdout.write(self.style.ERROR(message))
        else:
            self.stdout.write(self.style.WARNING('Обновление данных отменено.'))
