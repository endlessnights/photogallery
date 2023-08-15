# custom_filters.py

from django import template
from django.template.defaultfilters import stringfilter
from django.utils.translation import get_language, trans_real

register = template.Library()

@register.filter
@stringfilter
def replace_commas_with_periods(value):
    return value.replace(',', '.')


register.filter('replace_commas_with_periods', replace_commas_with_periods)


@register.simple_tag
def get_translation(text):
    current_language = get_language()
    return trans_real.translation(current_language).gettext(text)