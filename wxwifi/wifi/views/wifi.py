
from django.conf import settings
from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import HttpResponse


from .wechat_base import client, oauth, wechat_pay, crypto, wechat_component


def index(request):
    if request.method == 'GET':
        extend = request.GET.get('extend')
        openId = request.GET.get('openId')
        tid = request.GET.get('tid')
        print('extend is: {0}, openId is: {1}, tid is: {2}'.format(extend, openId, tid))
        return HttpResponse('extend is: {0}, openId is: {1}, tid is: {2}'.format(extend, openId, tid))
        # return HttpResponse('wifi!')


def list_shops(request):
    if request.method == 'GET':
        shops = client.wifi.list_shops()
        print('shops is: {0}'.format(shops))
        return HttpResponse('shops is: {0}'.format(shops))


def get_shop(request):
    if request.method == 'GET':
        shops = client.wifi.list_shops()
        print(shops)
        shop_id = shops['records'][0]['shop_id']
        shop_name = shops['records'][0]['shop_name']
        ssid = shops['records'][0]['ssid']
        ssid_list = shops['records'][0]['ssid_list']
        protocol_type = shops['records'][0]['protocol_type']
        sid = shops['records'][0]['sid']
        poi_id = shops['records'][0]['poi_id']


        print(shop_id)
        print(shop_name)
        print(ssid)
        print(ssid_list)
        print(protocol_type)

        print('shops is: {0}'.format(shops))

        shop_info = client.wifi.get_shop(shop_id)
        print('-----------************shopinfo************-----------')
        print(shop_info)
        return HttpResponse('shop_info is: {0}'.format(shop_info))



def add_pwd_device(request):
    if request.method == 'GET':
        shops = client.wifi.list_shops()
        print(shops)
        shop_id = shops['records'][0]['shop_id']
        print(shop_id)
        ssid = 'ChinaNet-9JYM'
        password = 'WXshshuhang'

        client.wifi.add_device(shop_id, ssid, password)
        return HttpResponse('device added successfully!')


