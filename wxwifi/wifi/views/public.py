# -*- coding: utf-8 -*-
# Author:William Zhang
# Email:quanpower@gmail.com
# Wechat:252527676
# Created:16-10-31 下午1:35

from __future__ import absolute_import, unicode_literals

import time
import os
import json

from wechat.utils import check_signature
from wechat.utils import tuling_auto_reply

from wechatpy import parse_message
from wechatpy import create_reply
from wechatpy.exceptions import InvalidSignatureException
from wechatpy.exceptions import InvalidAppIdException

from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from wagtail.wagtailadmin.site_summary import SiteSummaryPanel
from wagtail.wagtailcore import hooks

from .wechat_base import client, oauth, wechat_pay, crypto, wechat_component



def home(request):

    panels = [
        SiteSummaryPanel(request),
    ]

    for fn in hooks.get_hooks('construct_homepage_panels'):
        fn(request, panels)

    return render(request, "wagtailadmin/home.html", {
        'site_name': settings.WAGTAIL_SITE_NAME,
        'panels': sorted(panels, key=lambda p: p.order),
        'user': request.user
    })

def index(request):
    return render(request, 'wechat/public/index.html')

def login(request):
    return HttpResponseRedirect('/wechat/public/oauth1')

@login_required(login_url="/admin/login/")
def logout(request):
    return HttpResponse('logged out')

@login_required(login_url="/admin/login/")
def user(request):
    return render(request, 'wechat/public/user.html')

@csrf_exempt
def messages(request):

    """
        处理/wechat/public,解决跟微信公众号平台交互问题
    """
    if request.method == 'GET':
        """
        验证服务器有效
        """
        signature = request.GET.get('signature')
        timestamp = request.GET.get('timestamp')
        nonce = request.GET.get('nonce')
        echostr = request.GET.get('echostr')

        if check_signature(settings.TOKEN, signature, timestamp, nonce):
            print("Accept")
            return HttpResponse(echostr)
        else:
            print('Wrong')
            return HttpResponse("validate error")

    if request.method == 'POST':
        """
        响应微信服务器转发过来的消息

        首先取得arguments与body值，
        根据解析出收到的字符回复内容。

        """

        print('--------------go into post------------')

        signature = request.GET.get('signature')
        timestamp = request.GET.get('timestamp')
        nonce = request.GET.get('nonce')
        msg_signature = request.GET.get('msg_signature')
        encrypt_type = request.GET.get('encrypt_type')
        openid = request.GET.get('openid')

        body_text = request.body

        print('-----body_text-------' * 3)
        print('Raw message: \n%s' % body_text)
        print('------request--------' * 3)
        print(request)

        try:
            check_signature(settings.TOKEN, signature, timestamp, nonce)
        except InvalidSignatureException:
            return HttpResponse(status=403)

        # safe mode

        try:
            msg = crypto.decrypt_message(
                body_text,
                msg_signature,
                timestamp,
                nonce
            )
            print('Descypted message: \n%s' % msg)
        except (InvalidSignatureException, InvalidAppIdException):
            return HttpResponse(status=403)
        msg = parse_message(msg)

        print('--------------msg-----------', msg)

        # global reply :UnboundLocalError: local variable 'reply' referenced before assignment
        reply = create_reply('Reply test', msg)
        if msg.type == 'text':
            print ('--------msg.type-----', msg.type)
            tuling_reply = tuling_auto_reply(msg.source, msg.content)
            reply = create_reply(tuling_reply, msg)
            # english or chinese? use two diffrent robot to response
            # if english_or_chinese(msg.content) == 'chinese':
            #     tuling_reply = tuling_auto_reply(msg.source, msg.content)
            #     reply = create_reply(tuling_reply, msg)
            # else:
            #     aiml_reply = aiml_robot_reply(msg.content)
            #     reply = create_reply(aiml_reply, msg)
        elif msg.type == 'image':
            print ('--------msg.type-----', msg.type)
        elif msg.type == 'voice':
            print ('--------msg.type-----', msg.type)
        elif msg.type == 'shortvideo':
            print ('--------msg.type-----', msg.type)
        elif msg.type == 'video':
            print ('--------msg.type-----', msg.type)
        elif msg.type == 'location':
            print ('--------msg.type-----', msg.type)
        elif msg.type == 'link':
            print ('--------msg.type-----', msg.type)
        elif msg.type == 'event':
            print ('--------msg.type-----', msg.type)
            if msg.event == 'subscribe':
                reply = create_reply(u'欢迎关注智联云，enjoy it!', msg)
                if settings.DEBUG:
                    print ('--------msg.event-----', msg.event)
                    print ('------source openid------', msg.source)
                    print ('------target openid------', msg.target)
                # get the user_info by the openid == msg.source
                user_info = client.user.get(msg.source)
                if settings.debug:
                    print (user_info)

                # openid_count = self.db.get('SELECT * FROM followers WHERE openid = \"%s\" ', msg.source)
                # # if the database has this openid?if yes,update it,otherwise update it.
                # if openid_count:
                #     if settings.debug:
                #         print('Already has this openid,update it now!')
                #     # self.db.execute(
                #     #     'UPDATE followers SET subscribe = \"%s\", openid = \"%s\", nickname= \"%s\", sex= \"%s\", language= \"%s\", city= \"%s\", province= \"%s\", country= \"%s\", headimgurl= \"%s\", subscribe_time= \"%s\", unionid= \"%s\", remark= \"%s\", groupid= \"%s\", tagid_list= \"%s\" WHERE openid = \"%s\" ',
                #     #     user_info['subscribe'], user_info['openid'], user_info['nickname'],
                #     #     user_info['sex'], user_info['language'],
                #     #     user_info['city'], user_info['province'], user_info['country'],
                #     #     user_info['headimgurl'], user_info['subscribe_time'],
                #     #     user_info['unionid'], user_info['remark'], user_info['groupid'],
                #     #     user_info['tagid_list'], user_info['openid']
                #     #     )
                # else:
                #     if settings.debug:
                #         print('Insert this new openid!')
                    # self.db.execute(
                    #     'INSERT INTO followers (subscribe,openid,nickname,sex,language,city,province,country,headimgurl,subscribe_time,unionid,remark,groupid,tagid_list) '
                    #     'VALUES (\"%s\", "\%s\", "\%s\", "\%s\", "\%s\", "\%s\","\%s\", "\%s\", "\%s\", "\%s\", "\%s\","\%s\", "\%s\", "\%s\")',
                    #     user_info['subscribe'], user_info['openid'], user_info['nickname'], user_info['sex'],
                    #     user_info['language'],
                    #     user_info['city'], user_info['province'], user_info['country'], user_info['headimgurl'],
                    #     user_info['subscribe_time'],
                    #     user_info['unionid'], user_info['remark'], user_info['groupid'], user_info['tagid_list'])
                    # self.wechat_pay.redpack.send_group(user_info['openid'], 500, u'智联云', u'裂变红包测试', u'多谢各位兄弟们帮忙测试！', u'推荐好友，赢取更多惊喜！', 5)
                    # self.wechat_pay.redpack.send(user_info['openid'], 100, u'泉哥', u'普通红包测试', u'多谢各位兄弟们帮忙测试!', u'也请帮忙推荐其他好友测试！')

            elif msg.event == 'unsubscribe':
                # when unsubscribe ,update the subscribe from 1 to 0
                if settings.debug:
                    print ('--------msg.event-----', msg.event)
                    print ('------source openid------', msg.source)
                    print ('------target openid------', msg.target)
                # self.db.execute(
                #     'UPDATE followers SET subscribe = 0 WHERE openid = \"%s\" ', msg.source
                # )

            elif msg.event == 'subscribe_scan':
                if settings.debug:
                    print ('--------msg.event-----', msg.event)
                    print ('------source openid------', msg.source)
                    print ('------target openid------', msg.target)
                    print ('------subscribe_scan_scene_id------', msg.scene_id)
                reply = create_reply(u'欢迎关注智联云，enjoy it!', msg)
                # self.db.execute(
                #     'INSERT INTO subscribe_scan (openid,scene_id,scan_time) VALUES (\"%s\", "\%s\", "\%s\")',
                #     msg.source, msg.scene_id, int(time.time()))

            elif msg.event == 'scan':
                print ('--------msg.event-----', msg.event)
            elif msg.event == 'location':
                print ('--------msg.event-----', msg.event)
            elif msg.event == 'click':
                print ('--------msg.event-----', msg.event)
            elif msg.event == 'view':
                print ('--------msg.event-----', msg.event)
            elif msg.event == 'masssendjobfinish':
                print ('--------msg.event-----', msg.event)
            elif msg.event == 'templatesendjobfinish':
                print ('--------msg.event-----', msg.event)
            elif msg.event == 'scancode_push':
                print ('--------msg.event-----', msg.event)
            elif msg.event == 'scancode_waitmsg':
                print ('--------msg.event-----', msg.event)
            elif msg.event == 'pic_sysphoto':
                print ('--------msg.event-----', msg.event)
            elif msg.event == 'pic_photo_or_album':
                print ('--------msg.event-----', msg.event)
            elif msg.event == 'pic_weixin':
                print ('--------msg.event-----', msg.event)
            elif msg.event == 'location_select':
                print ('--------msg.event-----', msg.event)
            elif msg.event == 'card_pass_check':
                print ('--------msg.event-----', msg.event)
            elif msg.event == 'card_not_pass_check':
                print ('--------msg.event-----', msg.event)
            elif msg.event == 'user_get_card':
                print ('--------msg.event-----', msg.event)
            elif msg.event == 'user_del_card':
                print ('--------msg.event-----', msg.event)
            elif msg.event == 'merchant_order':
                print ('--------msg.event-----', msg.event)
            elif msg.event == 'kf_create_session':
                print ('--------msg.event-----', msg.event)
            elif msg.event == 'kf_close_session':
                print ('--------msg.event-----', msg.event)
            elif msg.event == 'kf_switch_session':
                print ('--------msg.event-----', msg.event)
            elif msg.event == 'device_text':
                print ('--------msg.event-----', msg.event)
            elif msg.event == 'bind':
                print ('--------msg.event-----', msg.event)
            elif msg.event == 'unbind':
                print ('--------msg.event-----', msg.event)
            elif msg.event == 'subscribe_status':
                print ('--------msg.event-----', msg.event)
            elif msg.event == 'unsubscribe_status':
                print ('--------msg.event-----', msg.event)
            elif msg.event == 'shakearound_user_shake':
                print ('--------msg.event-----', msg.event)
            elif msg.event == 'poi_check_notify':
                print ('--------msg.event-----', msg.event)
            elif msg.event == 'wificconnected':
                print ('--------msg.event-----', msg.event)
            elif msg.event == 'qualification_verify_success':
                print ('--------msg.event-----', msg.event)
            elif msg.event == 'qualification_verify_fail':
                print ('--------msg.event-----', msg.event)
            elif msg.event == 'naming_verify_success':
                print ('--------msg.event-----', msg.event)
            elif msg.event == 'naming_verify_fail':
                print ('--------msg.event-----', msg.event)
            elif msg.event == 'annual_renew':
                print ('--------msg.event-----', msg.event)
            elif msg.event == 'verify_expired':
                print ('--------msg.event-----', msg.event)
            elif msg.event == 'user_scan_product':
                print ('--------msg.event-----', msg.event)
            elif msg.event == 'user_scan_product_enter_session':
                print ('--------msg.event-----', msg.event)
            elif msg.event == 'user_scan_product_async':
                print ('--------msg.event-----', msg.event)
            elif msg.event == 'user_scan_product_verify_action':
                print ('--------msg.event-----', msg.event)
            elif msg.event == 'subscribe_scan_product':
                print ('--------msg.event-----', msg.event)
        else:
            reply = create_reply('Sorry, can not handle this for now', msg)
            print ('unknown type!!')
        encrypt_message = crypto.encrypt_message(reply.render(), nonce, timestamp)
        return HttpResponse(encrypt_message)

def menu_update(request):
    """
        处理/wechat/menu_update,解决微信公众号平台菜单更新问题
    """
    if request.method == 'GET':
        menu_data = {
            'button': [
                {
                    'type': 'view',
                    'name': '中储粮福州直属库',
                    'url': 'http://www.loraiiot.com:8000'
                },
                {
                    'name': '测试',
                    'sub_button': [
                        {
                            'type': 'view',
                            'name': 'Web auth测试',
                            'url': 'http://www.smartlinkcloud.com/wechat/public/oauth'
                        },
                        {
                            'type': 'view',
                            'name': '微信小店测试',
                            'url': 'http://mp.weixin.qq.com/bizmall/mallshelf?id=&t=mall/list&biz=MzIzNzI1MTk3Mg==&shelf_id=1&showwxpaytitle=1#wechat_redirect'
                        },
                        {
                            'type': 'view',
                            'name': '第三方授权测试',
                            'url': 'http://www.smartlinkcloud.com/wechat/component/authorize'
                        },
                        {
                            'type': 'view',
                            'name': '语音聊天室测试',
                            'url': 'http://www.smartlinkcloud.com/wechat/chat_room'
                        },
                        {
                            'type': 'view',
                            'name': '微信群直播机器人',
                            'url': 'http://www.smartlinkcloud.com/wechat/robot/index'
                        }
                    ]
                },
                {
                    'name': '我',
                    'sub_button': [
                        {
                            'type': 'view',
                            'name': '我的收益',
                            'url': 'http://www.smartlinkcloud.com/'
                        },
                        {
                            'type': 'view',
                            'name': '用户信息',
                            'url': 'http://www.smartlinkcloud.com/wechat/public/user/'
                        },
                        {
                            'type': 'view',
                            'name': '公众号支付测试',
                            'url': 'http://www.smartlinkcloud.com/wechat/pay/public/'
                        },
                        {
                            'type': 'view',
                            'name': '带我赚钱',
                            'url': 'http://www.smartlinkcloud.com/'
                        },
                        {
                            'type': 'click',
                            'name': '联系我们',
                            'key': 'V2000_contact_us'
                        }
                    ]
                }
            ]
        }

        try:
            client.menu.delete()
            res = client.menu.create(menu_data)
        except Exception as e:
            print(e)
            return HttpResponse(str(e))
        else:
            return HttpResponse(json.dumps(res))

def media_upload(request):
    """
        处理/wechat/media_load,解决微信公众号平台文件上传问题
    """
    if request.method == 'GET':
        img_path = os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            'doge.jpeg'
        )


        try:
            with open(img_path) as media_file:
                res = client.media.upload('image', media_file)
        except Exception as e:
            print(e)
            return HttpResponse(str(e))
        else:
            return HttpResponse(json.dumps(res))


def oauth1(request):
    if request.method == 'GET':
        print (oauth.authorize_url)
        return HttpResponseRedirect(oauth.authorize_url)


def oauth2(request):
    if request.method == 'GET':
        code = request.GET.get('code')
        state = request.GET.get('state')
        print ('------code--------', code)

        oauth.fetch_access_token(code)
        openid = oauth.open_id
        access_token = oauth.access_token
        refresh_token = oauth.refresh_token

        # self.wechat_pay.redpack.send(openid, 100, u'泉哥', u'普通红包测试', u'多谢各位兄弟们帮忙测试!', u'也请帮忙推荐其他好友测试！')
        # self.wechat_pay.redpack.send_group(openid, 500, u'智联云', u'裂变红包测试', u'多谢各位兄弟们帮忙测试！', u'推荐好友，赢取更多惊喜！', 5)

        print ('-------openid------', openid)
        print ('-------access_token------', access_token)
        if oauth.check_access_token():
            print ("access_token is valid now!")
            user_info = oauth.get_user_info()
        else:
            oauth.refresh_access_token(refresh_token)
            user_info = oauth.get_user_info()
        print (user_info)

        # web_authed_openid = self.db.get('SELECT * FROM web_authed_users WHERE openid = \"%s\" ', user_info['openid'])
        # print (web_authed_openid)
        # if web_authed_openid:
        #     if self.settings.get('debug'):
        #         print('Already has this openid,update it now!')
        #     self.db.execute(
        #         'UPDATE web_authed_users SET openid = \"%s\", nickname= \"%s\", sex= \"%s\", province= \"%s\", city= \"%s\", country= \"%s\", headimgurl= \"%s\", privilege= \"%s\", unionid= \"%s\" WHERE openid = \"%s\" ',
        #         user_info['openid'], user_info['nickname'], user_info['sex'], user_info['province'], user_info['city'],
        #         user_info['country'], user_info['headimgurl'], user_info['privilege'], user_info['unionid'],
        #         user_info['openid'])
        # else:
        #     self.db.execute(
        #         'INSERT INTO web_authed_users (openid,nickname,sex,province,city,country,headimgurl,privilege,unionid) '
        #         'VALUES (\"%s\", "\%s\", "\%s\", "\%s\", "\%s\", "\%s\","\%s\", "\%s\", "\%s\")',
        #         user_info['openid'], user_info['nickname'], user_info['sex'], user_info['province'], user_info['city'],
        #         user_info['country'], user_info['headimgurl'], user_info['privilege'], user_info['unionid'])
        #
        # self.set_secure_cookie("user_id", openid)
        # return HttpResponseRedirect(request.GET.get('next'), "/wechat/public/index/")
        return HttpResponseRedirect("/wechat/public/index/")


def wifi(request):
    if request.method == 'GET':
        extend = request.GET.get('extend')
        openId = request.GET.get('openId')
        tid = request.GET.get('tid')
        print('extend is: {0}, openId is: {1}, tid is: {2}'.format(extend, openId, tid))
        return HttpResponse('extend is: {0}, openId is: {1}, tid is: {2}'.format(extend, openId, tid))


def qrcode(request):
    if request.method == 'GET':
        # action_name = self.get_argument('action_name', strip=True)
        # action_info = self.get_argument('action_info', strip=True)
        # scene_str = self.get_argument('scene_str', strip=True)
        qrcode_data = {
            "action_name": "QR_LIMIT_STR_SCENE",
            "action_info": {
            "scene": {
                "scene_str": "yanzhou_train_station"
                }
            }
        }

        r = client.qrcode.create(qrcode_data)
        print(r)
        ticket = r['ticket']
        # qrcode = client.qrcode.show(ticket)
        # print(qrcode)
        return HttpResponseRedirect(client.qrcode.get_url(ticket))



def error_test(request):
    raise Exception("This is a test of the emergency broadcast system.")

#
# (r'/wechat/public/index', PublicIndexHandler),
# (r'/wechat/public/user/redpack', PublicGetRedpackHandler),
# (r'/wechat/public/redpack/info', PublicGetRedpackInfoHandler),
# (r'/wechat/public/user/info', PublicUserInfoHandler),
# (r'/wechat/public/user/followers', PublicGetFollowersHandler),
# (r'/wechat/public/user/group', PublicUserGroupHandler),
# (r'/wechat/public/messages', PublicMessagesHandler),
# (r'/wechat/public/media/upload', PublicMediaUploadHandler),
# (r'/wechat/public/menu/update', PublicMenuUpdateHandler),
# (r'/wechat/public/oauth', PublicOAuthHandler),
# (r'/wechat/public/oauth2', PublicOAuth2Handler),
# (r'/wechat/public/wifi', PublicWiFiHandler),
# (r'/wechat/public/qrcode', PublicQRcodeHandler),
