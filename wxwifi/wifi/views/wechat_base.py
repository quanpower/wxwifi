# -*- coding: utf-8 -*-
# Author:William Zhang
# Email:quanpower@gmail.com
# Wechat:252527676
# Created:16-11-2 上午10:37

from __future__ import absolute_import, unicode_literals

from wechatpy import WeChatClient
from wechatpy import WeChatOAuth
from wechatpy import WeChatComponent
from wechatpy import WeChatPay
from wechatpy.crypto import WeChatCrypto

from django.conf import settings

APPID = settings.APPID
SECRET = settings.SECRET
ENCODINGAESKEY = settings.ENCODINGAESKEY
TOKEN = settings.TOKEN

REDIRECT_URI = settings.REDIRECT_URI
CHAT_ROOM_LOGIN_REDIRECT_URI = settings.CHAT_ROOM_LOGIN_REDIRECT_URI
OPENID = settings.OPENID
SCOPE = settings.SCOPE
STATE = settings.STATE

WECHAT_PAY_APIKEY = settings.WECHAT_PAY_APIKEY
WECHAT_PAY_MCH_ID = settings.WECHAT_PAY_MCH_ID
WECHAT_PAY_MCH_CERT_PATH = settings.WECHAT_PAY_MCH_CERT_PATH
WECHAT_PAY_MCH_KEY_PATH = settings.WECHAT_PAY_MCH_KEY_PATH

COMPONENT_APPID = settings.COMPONENT_APPID
COMPONENT_APPSECRECT = settings.COMPONENT_APPSECRECT
COMPONENT_TOKEN = settings.COMPONENT_TOKEN

oauth = WeChatOAuth(APPID, SECRET, REDIRECT_URI, SCOPE, STATE)
client = WeChatClient(APPID, SECRET)
crypto = WeChatCrypto(TOKEN, ENCODINGAESKEY, APPID)
wechat_pay = WeChatPay(APPID, WECHAT_PAY_APIKEY, WECHAT_PAY_MCH_ID, '', WECHAT_PAY_MCH_CERT_PATH, WECHAT_PAY_MCH_KEY_PATH)
oauth_chat_room = WeChatOAuth(APPID, SECRET, CHAT_ROOM_LOGIN_REDIRECT_URI, SCOPE, STATE)
wechat_component = WeChatComponent(COMPONENT_APPID, COMPONENT_APPSECRECT, COMPONENT_TOKEN, ENCODINGAESKEY)

