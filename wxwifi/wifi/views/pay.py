# -*- coding: utf-8 -*-
# Author:William Zhang
# Email:quanpower@gmail.com
# Wechat:252527676
# Created:16-10-31 下午1:35

from __future__ import absolute_import, unicode_literals

import time
from wechatpy.utils import random_string

from django.conf import settings
from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import HttpResponse

from wagtail.wagtailadmin.site_summary import SiteSummaryPanel
from wagtail.wagtailcore import hooks
from wagtail.wagtailcore.models import Page, PageRevision, UserPagePermissionsProxy

from .wechat_base import client, oauth, wechat_pay, crypto, wechat_component

def public(request):
    if request.method == 'GET':

        user_id = self.get_secure_cookie("user_id") #todo:get secure cookie
        body = u'智联云-直播打赏'
        total_fee = 10
        notify_url = 'www.smartlinkcloud.com/wechat/pay/public/callback'
        # find the real ip behind nginx
        if request.META.has_key('HTTP_X_FORWARDED_FOR'):
            client_ip = request.META['HTTP_X_FORWARDED_FOR']
        else:
            client_ip = request.META['REMOTE_ADDR']

        r = wechat_pay.order.create('JSAPI', body, total_fee, notify_url, client_ip=client_ip, user_id=user_id)
        prepay_id = r['prepay_id']
        print('----------r , prepay_id----------', r, prepay_id)


        ticket = client.jsapi.get_jsapi_ticket()
        noncestr = str(random_string(16))
        timestamp = str(int(time.time()))
        url = request.get_full_path() # request.path
        signature = client.jsapi.get_jsapi_signature(noncestr, ticket, timestamp, url)


        jsapi_params = wechat_pay.jsapi.get_jsapi_params(prepay_id, timestamp, noncestr)
        jsapi_params = {key.encode('utf-8'): value.encode('utf-8') for key, value in jsapi_params.items()}
        print('--------jsapi_params--------', jsapi_params)

        return render(request, "jsapi_pay.html", {
            'jsapi_params': jsapi_params,
            'tiemstamp': timestamp,
            'noncestr': noncestr,
            'signature': signature,
            'appid': client.appid
        })

def public_callback(request):
    if request.method == 'GET':
        print('-----------WechatPayPublicCallback------------')
        return HttpResponse('WechatPayPublicCallback')
