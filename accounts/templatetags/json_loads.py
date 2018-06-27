# coding: utf-8
import json

from django import template


register = template.Library()


@register.filter
def json_loads(value):
    """
    """
    return json.loads(value)
