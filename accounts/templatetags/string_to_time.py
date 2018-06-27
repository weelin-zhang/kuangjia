# coding: utf-8
import pytz
from django import template
from django.utils import timezone
from django.utils.dateparse import parse_datetime


register = template.Library()


@register.filter
def string_to_time(value, utc=False):
    """ string time to python datetime
    utc: 手动utc, 有的字符串不是utc格式的用这个参数
    """
    if not utc:
        return parse_datetime(value)
    else:
        utc = pytz.utc
        current_tz = timezone.get_current_timezone()

        return utc.localize(parse_datetime(value)).astimezone(current_tz)
