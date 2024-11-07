import logging

from celery import shared_task

from cryptocurrencies.services import update_cryptocurrency_prices, update_cryptocurrencies_top

logger = logging.getLogger('celery')


@shared_task
def update_cc_prices():
    logger.info("Начало обновления данных о криптовалютах")
    success, result = update_cryptocurrency_prices()
    if success:
        logger.info(result)
    else:
        logger.error(result)
    logger.info("Завершено обновление данных о криптовалютах")


@shared_task
def update_cc_top():
    update_cryptocurrencies_top()
