# -*- coding: utf-8 -*-
# Author:William Zhang
# Email:quanpower@gmail.com
# Wechat:252527676
# Created:17-1-3 下午9:13

command = '/root/ENV/wxwifipy3/bin/gunicorn'
pythonpath = '/root/ENV/wxwifipy3/bin'
bind = 'unix:/tmp/gunicorn.sock'
# bind = '0.0.0.0:8000'
workers = 5
user = 'root'