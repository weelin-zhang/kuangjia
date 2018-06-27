# coding: utf-8
from django import template


register = template.Library()


@register.simple_tag
def get_url_args(request_full_path):
    return request_full_path.split('?')[1] if len(request_full_path.split('?'))>1 else ''