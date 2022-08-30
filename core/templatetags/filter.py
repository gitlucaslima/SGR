from atexit import register

from django import template

register = template.Library()


@register.filter(name="teste")
def filter_teste(value):
    return "{} + ola".format(value)
