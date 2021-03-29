from django import template
from django.template.defaultfilters import stringfilter
import time


register = template.Library()

@register.simple_tag
def current_time():
    return time.strftime(r"%d.%m.%Y %H:%M:%S", time.localtime())


@register.filter(name='reverse_string')
def reverse_string(string_value):
    return "".join(reversed(string_value))