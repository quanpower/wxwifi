# -*- coding: utf-8 -*-
# Author:William Zhang
# Email:quanpower@gmail.com
# Wechat:252527676
# Created:16-10-31

from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

from wechat.views import pay

urlpatterns = [
    url(r'^public', pay.public, name='wechat_pay_public'),
    url(r'^public_callback', pay.public_callback, name='wechat_pay_public_callback'),
]