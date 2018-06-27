# coding: utf-8
from django import template


register = template.Library()


@register.simple_tag
def error_str(error_dict, flag=1):
    if flag:
        return ''.join([(item.data)[0].message for item in error_dict.values()])

