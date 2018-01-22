# -*- coding: utf-8 -*-
# Author:William Zhang
# Email:quanpower@gmail.com
# Wechat:252527676
# Created:18-01-22

from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

from wechat.views import wifi

urlpatterns = [
    url(r'^index', wifi.index, name='wifi_index'),
]