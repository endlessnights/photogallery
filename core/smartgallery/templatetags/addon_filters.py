# custom_filters.py

from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
@stringfilter
def replace_commas_with_periods(value):
    return value.replace(',', '.')


register.filter('replace_commas_with_periods', replace_commas_with_periods)