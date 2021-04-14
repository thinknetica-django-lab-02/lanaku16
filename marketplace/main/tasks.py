from datetime import datetime, timedelta

from celery import shared_task

from django.contrib.auth.models import User
from django.utils import timezone

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


@app.task
def monday_mail_about_new_goods():
    logger.info("Отправка email в понедельник:Запуск таски")
    date_minus_7days = timezone.now() - timedelta(days=7)
    goods_per_week = Good.objects.filter(date_create__gte=date_minus_7days)
    from_email = 'admin@marketplace.ru'
    subject = 'Новые товары на сайте с %s' % date_minus_7days
    html_content = '<p><i>Здравствуйте</i></p>'
    html_content += 'Новые товары:'

    for goodone in goods_per_week:
        title = goodone.good_name
        html_content += '<a href="http://127.0.0.1:8000/main/goods/%s">%s</a>' % (goodone.id, title)

    for subscrib_user in Subscriber.objects.all():
        user = User.objects.get(id=subscrib_user.user_id)
        to_email = user.email
        email = EmailMessage(subject, html_content, from_email, [to_email])
        email.content_subtype = "html"
        email.send()
        logger.warning("Email отправлен")

    logger.info("Отправка email в понедельник:Окончание таски")
    return True