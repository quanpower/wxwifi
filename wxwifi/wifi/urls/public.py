# -*- coding: utf-8 -*-
# Author:William Zhang
# Email:quanpower@gmail.com
# Wechat:252527676
# Created:16-10-31

from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

from wechat.views import public

urlpatterns = [
    url(r'^index/$', public.index, name='wechat_public_index'),
    url(r'^messages', public.messages, name='wechat_public_messages'),
    url(r'^user/$', public.user, name='wechat_public_user'),
    url(r'^menu_update/$', public.menu_update, name='wechat_public_menu_update'),
    url(r'^media_upload/$', public.media_upload, name='wechat_public_media_upload'),
    url(r'^oauth1/$', public.oauth1, name='wechat_public_oauth1'),
    url(r'^oauth2/$', public.oauth2, name='wechat_public_oauth2'),
    url(r'^wifi/$', public.wifi, name='wechat_public_wifi'),
    url(r'^qrcode/$', public.qrcode, name='wechat_public_qrcode'),
    url(r'^login/$', public.login, name='wechat_public_login'),
    url(r'^logout/$', public.logout, name='wechat_public_logout'),
]

