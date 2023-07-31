# custom_filters.py

from django import template

register = template.Library()

@register.filter
def lower(value):
    return value.lower()