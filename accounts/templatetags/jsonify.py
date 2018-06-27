# coding: utf-8
import json
import decimal

from django import template


register = template.Library()


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        super(DecimalEncoder, self).default(o)


@register.filter
def jsonify(value):
    """ value to json """
    return json.dumps(value, cls=DecimalEncoder)
