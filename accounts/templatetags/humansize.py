# coding: utf-8
from django import template

from utils.base import humansize as hs

register = template.Library()


@register.filter
def humansize(size, unit=None):
    """ 字典get """
    return hs(size, unit)
