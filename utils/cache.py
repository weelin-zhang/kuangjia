# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import redis

from django.conf import settings


cache = redis.StrictRedis(host=settings.REDIS['host'], port=settings.REDIS['port'], db=0)
