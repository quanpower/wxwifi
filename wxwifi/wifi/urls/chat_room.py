# -*- coding: utf-8 -*-
# Author:William Zhang
# Email:quanpower@gmail.com
# Wechat:252527676
# Created:16-10-31

from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

from wechat.views import chat_room

urlpatterns = [
    url(r'^index/$', chat_room.index, name='wechat_chat_room_index'),
]