# custom_filters.py

from django import template
from django.template import Template, Context
from django.template.defaultfilters import stringfilter
from django.utils.translation import get_language, trans_real

from ..models import MenuItem

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


@register.simple_tag
def render_content(content, context):
    template = Template(content)
    render_content = template.render(Context(context))
    return render_content


# class AllMenuItemsNode(template.Node):
#     def __init__(self, nodelist):
#         self.nodelist = nodelist
#
#     def render(self, context):
#         menu_items = MenuItem.objects.all()
#         rendered_items = []
#
#         for menu_item in menu_items:
#             context['menu_item'] = menu_item
#             rendered_items.append(self.nodelist.render(context))
#
#         return ''.join(rendered_items)
#
#
# @register.tag
# def all_menu_items(parser, token):
#     nodelist = parser.parse(('end_all_menu_items',))
#     parser.delete_first_token()
#     return AllMenuItemsNode(nodelist)
