from __future__ import division
from django import template
from django.template.defaultfilters import stringfilter

import time
from datetime import datetime, timedelta

from django.conf import settings
from django.template.loader import get_template
from django.urls import reverse

from main.models import Category

import random

register = template.Library()

@register.simple_tag
def current_time():
    return time.strftime(r"%d.%m.%Y %H:%M:%S", time.localtime())


@register.simple_tag
def admin_mail():
    return settings.ADMIN_EMAIL


@register.filter(name='reverse_string')
def reverse_string(string_value):
    return "".join(reversed(string_value))


@register.inclusion_tag('main/tags/cats.html')
def show_all_categories():
    """Вывод категорий в рандомном порядке"""
    cats_list = []
    cats = Category.objects.all()
    for cat in cats:
        cats_list.append((cat))

    random_cats = random.sample(cats_list, len(cats_list))

    return {'cats': random_cats}


@register.simple_tag
def new_room():
    now = datetime.utcnow()
    args_or = str(totimestamp(now))
    args = args_or.replace('.','')
    return reverse('room', args=[args])


def totimestamp(dt, epoch=datetime(1970, 1, 1)):
    td = dt - epoch
    # return td.total_seconds()
    return (td.microseconds + (td.seconds + td.days * 86400) * 10 ** 6) / 10 ** 6
