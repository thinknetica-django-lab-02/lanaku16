from celery import shared_task
from celery.decorators import task
from django.contrib.auth.models import User

from main.models import Good, Subscriber
from marketplace.celery import app

from django.core.mail import EmailMessage

import logging


logger = logging.getLogger(__name__)


@shared_task
def send_mail_about_new_good(good_id):
    logger.info("Отправка email:Запуск таски")
    good_new = Good.objects.get(id=good_id)
    from_email = 'admin@marketplace.ru'
    subject = 'Новый товар на сайте'
    html_content = '<p><i>Здравствуйте</i></p>'
    html_content += 'На сайте появился новый товар:'
    html_content += '<a href="http://127.0.0.1:8000/main/goods/%s">%s</a>' % (good_new.id, good_new.good_name)
    for subscrib_user in Subscriber.objects.all():
        user = User.objects.get(id=subscrib_user.user_id)
        to_email = user.email
        email = EmailMessage(subject, html_content, from_email, [to_email])
        email.content_subtype = "html"
        email.send()
        logger.warning("Email отправлен")

    logger.info("Отправка email:Окончание таски")
    return True