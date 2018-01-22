# -*- coding: utf-8 -*-
# Author:William Zhang
# Email:quanpower@gmail.com
# Wechat:252527676
# Created:16-10-31

from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

from wechat.views import component

urlpatterns = [
    url(r'^receive', component.receive, name='wechat_component_receive'),
    url(r'^callback', component.callback, name='wechat_component_callback'),
    url(r'^authorize', component.authorize, name='wechat_component_authorize'),
    url(r'^authorization_code', component.authorization_code, name='wechat_component_authorization_code'),
]