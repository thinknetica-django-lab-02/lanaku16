from django import template
from django.template.defaultfilters import stringfilter
import time
from django.conf import settings
from django.template.loader import get_template

from main.models import Category

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
    cats = Category.objects.all()[:10]
    return {'cats': cats}