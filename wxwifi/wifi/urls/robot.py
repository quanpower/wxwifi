# -*- coding: utf-8 -*-
# Author:William Zhang
# Email:quanpower@gmail.com
# Wechat:252527676
# Created:16-11-2 下午11:06

from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

from wechat.views import robot

urlpatterns = [
    url(r'^index', robot.index, name='wechat_robot_index'),
]