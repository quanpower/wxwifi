# -*- coding: utf-8 -*-
# Author:William Zhang
# Email:quanpower@gmail.com
# Wechat:252527676
# Created:18-01-22

from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

from wifi.views import wifi

urlpatterns = [
    url(r'^index', wifi.index, name='wifi_index'),
    url(r'^list_shops', wifi.list_shops, name='wifi_list_shops'),
    url(r'^get_shop', wifi.get_shop, name='wifi_get_shop'),
    url(r'^add_pwd_device', wifi.add_pwd_device, name='wifi_add_pwd_device'),
]