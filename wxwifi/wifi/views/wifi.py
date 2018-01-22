
from django.conf import settings
from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import HttpResponse


def index(request):
    if request.method == 'GET':
        extend = request.GET.get('extend')
        openId = request.GET.get('openId')
        tid = request.GET.get('tid')
        print('extend is: {0}, openId is: {1}, tid is: {2}'.format(extend, openId, tid))
        return HttpResponse('extend is: {0}, openId is: {1}, tid is: {2}'.format(extend, openId, tid))

