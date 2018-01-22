# -*- coding: utf-8 -*-
# Author:William Zhang
# Email:quanpower@gmail.com
# Wechat:252527676
# Created:16-10-31 下午1:35

from __future__ import absolute_import, unicode_literals

from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

from .wechat_base import wechat_component

def authorize(request):
    if request.method == 'GET':
        pre_auth_code = wechat_component.create_preauthcode()['pre_auth_code']
        return HttpResponseRedirect('https://mp.weixin.qq.com/cgi-bin/componentloginpage?component_appid={0}&pre_auth_code={1}&redirect_uri={2}'.format(settings.COMPONENT_APPID, pre_auth_code, '/wechat/component/authorization_code'))

def authorization_code(request):
    if request.method == 'GET':
        authorization_code = request.GET.get('auth_code')
        wechat_component.get_client_by_authorization_code(authorization_code)

@csrf_exempt
def receive(request):
    if request.method == 'GET':
        print(request)

    if request.method == 'POST':
        print(request)
        print ('-----request_body----')
        print (request.body)

        msg_signature = request.GET.get('msg_signature')
        signature = request.GET.get('signature')
        timestamp = request.GET.get('timestamp')
        nonce = request.GET.get('nonce')
        encrypt_type = request.GET.get('encrypt_type')

        print(msg_signature,'------\n',signature,'-------\n',timestamp,'------\n',nonce,'--------\n',encrypt_type)
        wechat_component.cache_component_verify_ticket(request.body, msg_signature, timestamp, nonce)
        return HttpResponse('success')

def callback(request, *args):
    if request.method == 'GET':
        print (type(args), args)
        return HttpResponse('appid is :{0}'.format(args[0]))
