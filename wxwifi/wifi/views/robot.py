# -*- coding: utf-8 -*-
# Author:William Zhang
# Email:quanpower@gmail.com
# Wechat:252527676
# Created:16-11-2 下午11:06

from django.shortcuts import render

from wechat.views.WechatWeb import TulingWXBot
from django.contrib.auth.decorators import login_required


@login_required(login_url="/wechat/public/login/")
def index(request):
    if request.method == 'GET':
        wechat_robot = TulingWXBot()
        wechat_robot.start()
        return render(request, 'wechat/robot/robot_index.html')