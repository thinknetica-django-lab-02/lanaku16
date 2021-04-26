import os
import django

from django.core.exceptions import ObjectDoesNotExist

from main.models import Good


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'marketplace.settings')
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
django.setup()


def receive_message_from_bot(message: str) -> str:
    message = message[1:]
    if message == 'start':
        return send_start_message()
    else:
        if len(message) == 0:
            return 'Заполните в сообщении #<название товара>'

        return send_in_stock_message(message)

def send_start_message() -> str:
    return 'Приветствую на сайте Marketplace. Чтобы узнать количество товара на складе, введите #<название товара>'

def send_in_stock_message(name):
    try:
        good_get = Good.objects.get(good_name=name)
        good_in_stock = good_get.get_in_stock()
        if good_in_stock == 0:
            return 'Товар закончился'
        return 'Товара на складе: %s' % (good_in_stock)
    except Good.DoesNotExist:
        return 'Ничего не найдено'


