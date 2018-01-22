# -*- coding: utf-8 -*-
# Author:William Zhang
# Email:quanpower@gmail.com
# Wechat:252527676
# Created:16-10-31 下午1:35

from __future__ import absolute_import, unicode_literals

from django.conf import settings
from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

from wagtail.wagtailadmin.site_summary import SiteSummaryPanel
from wagtail.wagtailcore import hooks
from wagtail.wagtailcore.models import Page, PageRevision, UserPagePermissionsProxy

from .wechat_base import oauth_chat_room

def index(request):
    if request.method == 'GET':
        channel = request.GET.get('channel') or 'default'
        self.set_secure_cookie('channel', channel)# todo: set secure cookie
        if not self.get_secure_cookie('openid'):
            return HttpResponseRedirect(oauth_chat_room.authorize_url)
        return HttpResponseRedirect('/chat_room/channel/{0}'.format(channel))
