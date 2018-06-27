# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import datetime

from django.conf import settings
from django.utils import timezone


def is_token_valid(expiration, margin=None):
    """Timezone-aware checking of the auth token's expiration timestamp.

    Returns ``True`` if the token has not yet expired, otherwise ``False``.

    :param token: The openstack_auth.user.Token instance to check

    :param margin:
       A time margin in seconds to subtract from the real token's validity.
       An example usage is that the token can be valid once the middleware
       passed, and invalid (timed-out) during a view rendering and this
       generates authorization errors during the view rendering.
       A default margin can be set by the TOKEN_TIMEOUT_MARGIN in the
       django settings.
    """
    # expiration = token.expires
    # In case we get an unparseable expiration timestamp, return False
    # so you can't have a "forever" token just by breaking the expires param.
    if expiration is None:
        return False
    if margin is None:
        margin = getattr(settings, 'TOKEN_TIMEOUT_MARGIN', 0)
    expiration = expiration - datetime.timedelta(seconds=margin)
    if settings.USE_TZ and timezone.is_naive(expiration):
        # Presumes that the Keystone is using UTC.
        expiration = timezone.make_aware(expiration, timezone.utc)
    return expiration > timezone.now()


suffixes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']


def humansize(size, unit=None, has_unit=True):
    """ 将容量单位格式化
    unit 为默认单位，不填为B
    has_unit 是否带单位
    """
    i = suffixes.index(unit or 'B')
    while size >= 1024 and i < len(suffixes)-1:
        size /= 1024.
        i += 1
    f = ('%.2f' % size).rstrip('0').rstrip('.')
    return '{} {}'.format(f, suffixes[i]) if has_unit else '{}'.format(f)
