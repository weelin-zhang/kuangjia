# coding: utf-8
from django import template


register = template.Library()


@register.filter
def dict_get(_dict, key, default=None):
    """ 字典get """
    return _dict.get(key, default)
