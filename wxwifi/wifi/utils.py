# -*- coding: utf-8 -*-
# Author:William Zhang
# Email:quanpower@gmail.com
# Created:16-6-3 下午11:55

import json
import requests
import hashlib
import re
# import AimlConfig

TULINGKEY = 'f3e08f037dc484a203ed70bb15fb6e56'

def tuling_auto_reply(uid, msg):
    """
    tuling auto relpy
    :param uid:
    :param msg:
    :return:
    """
    if TULINGKEY:
        url = "http://www.tuling123.com/openapi/api"
        user_id = uid.replace('@', '')[:30]
        body = {'key': TULINGKEY, 'info': msg.encode('utf8'), 'userid': user_id}
        r = requests.post(url, data=body, verify=False)
        respond = json.loads(r.text)
        print (respond)

        if respond['code'] == 100000:
            tuling_result = respond['text'].replace('<br>', '  ')
            print ('------------tuling_result------', tuling_result)
            result = re.sub(u'图灵机器人', u'牛顿机器人', tuling_result)
            print ('--------------result-----------', result)
        elif respond['code'] == 200000:
            result = respond['url']
        elif respond['code'] == 302000:
            result = respond['text']
        elif respond['code'] == 308000:
            result = respond['text']
        else:
            result = respond['text'].replace('<br>', '  ')
        print ('NewTon ROBOT:', result)
        return result
    else:
        return u"知道啦"

def aiml_robot_reply(content):
    """
    aiml robot respond text to wechat

    :return:
    """
    respond = AimlConfig.alice.respond(content)
    if respond == None or len(respond) < 1:
        respond = '''Sorry I can't understand you'''
    return respond

def english_or_chinese(str):
    lang = 'chinese'
    try:
        str.decode('ascii')
        lang = 'english'
    except UnicodeEncodeError:
        pass
    except UnicodeDecodeError:
        pass
    return lang

def disable_urllib3_warning():
    """
    https://urllib3.readthedocs.org/en/latest/security.html#insecurerequestwarning
    InsecurePlatformWarning 警告的临时解决方案
    """
    try:
        import requests.packages.urllib3
        requests.packages.urllib3.disable_warnings()
    except Exception:
        pass

def check_signature(token, signature, timestamp, nonce):
    """
    验证微信消息真实性
    :param signature: 微信加密签名
    :param timestamp: 时间戳
    :param nonce: 随机数
    :return: 通过验证返回 True, 未通过验证返回 False
    """
    if not signature or not timestamp or not nonce:
        return False

    tmp_list = [token, timestamp, nonce]
    tmp_list.sort()
    tmp_str = ''.join(tmp_list)
    if signature != hashlib.sha1(tmp_str.encode('utf-8')).hexdigest():
        return False

    return True

def md5(str):
    """

    :param string:
    :return:
    """
    import hashlib
    import types
    if type(str) is types.StringType:
        m = hashlib.md5()
        m.update(str)
        return m.hexdigest()
    elif type(str) is types.UnicodeType:
        m = hashlib.md5()
        m.update(str)
        return m.hexdigest()
    else:
        return ''