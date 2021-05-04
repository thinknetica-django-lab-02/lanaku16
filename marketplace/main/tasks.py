from datetime import datetime, timedelta
import random

from celery import shared_task

from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone

from main.models import Good, Subscriber, SMSLog
from marketplace.celery import app

from django.core.mail import EmailMessage

import vonage
from vonage import Sms

import logging


logger = logging.getLogger(__name__)


@shared_task
def send_mail_about_new_good(good_id):
    logger.info("Отправка email:Запуск таски")
    good_new = Good.objects.get(id=good_id)
    from_email = settings.ADMIN_EMAIL
    subject = 'Новый товар на сайте'
    html_content = '<p><i>Здравствуйте</i></p>'
    html_content += 'На сайте появился новый товар:'
    html_content += '<a href="%smain/goods/%s">%s</a>' % (settings.DOMAIN_NAME, good_new.id, good_new.good_name)
    for subscrib_user in Subscriber.objects.all():
        user = User.objects.get(id=subscrib_user.user_id)
        to_email = user.email
        email = EmailMessage(subject, html_content, from_email, [to_email])
        email.content_subtype = "html"
        email.send()
        logger.info("Email отправлен")

    logger.info("Отправка email:Окончание таски")
    return True


@app.task
def monday_mail_about_new_goods():
    logger.info("Отправка email в понедельник:Запуск таски")
    date_minus_7days = timezone.now() - timedelta(days=7)
    goods_per_week = Good.objects.filter(date_create__gte=date_minus_7days)
    from_email = settings.ADMIN_EMAIL
    subject = 'Новые товары на сайте с %s' % date_minus_7days
    html_content = '<p><i>Здравствуйте</i></p>'
    html_content += 'Новые товары:'

    for goodone in goods_per_week:
        title = goodone.good_name
        html_content += '<a href="%smain/goods/%s">%s</a>' % (settings.DOMAIN_NAME, goodone.id, title)

    for subscrib_user in Subscriber.objects.all():
        user = User.objects.get(id=subscrib_user.user_id)
        to_email = user.email
        email = EmailMessage(subject, html_content, from_email, [to_email])
        email.content_subtype = "html"
        email.send()
        logger.info("Email отправлен")

    logger.info("Отправка email в понедельник:Окончание таски")
    return True


@app.task
def send_random_code(to_number):
    from_number = "Vonage APIs"
    client = vonage.Client(key=settings.VONAGE_KEY, secret=settings.VONAGE_SECRET)
    sms = vonage.Sms(client)
    sms_body = random.randrange(1000, 9999, 1)
    responseData = sms.send_message(
        {
            "from": from_number,
            "to": to_number,
            "text": sms_body,
        }
    )

    SMSLog.objects.create(
        body=sms_body,
        from_number=from_number,
        to_number=to_number,
        status_response=responseData["messages"][0]["status"]
    )