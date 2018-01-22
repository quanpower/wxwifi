# -*- coding: utf-8 -*-
# Author:William Zhang
# Email:quanpower@gmail.com
# Created:16-3-29 上午8:55

import ConfigParser
import json
import re

from BaiduRecognitionAndTTS import baidu_asr
from wechat.views.wxbot import *


class TulingWXBot(WXBot):
    def __init__(self):
        WXBot.__init__(self)

        self.tuling_key = ""
        self.robot_switch = True

        try:
            cf = ConfigParser.ConfigParser()
            cf.read('conf.ini')
            self.tuling_key = cf.get('main', 'key')
            self.live_speaker = cf.get('live', 'speaker')
            self.live_major_group = cf.get('live', 'major_group')
        except Exception:
            pass
        print 'tuling_key:', self.tuling_key

    def tuling_auto_reply(self, uid, msg):
        if self.tuling_key:
            url = "http://www.tuling123.com/openapi/api"
            user_id = uid.replace('@', '')[:30]
            body = {'key': self.tuling_key, 'info': msg.encode('utf8'), 'userid': user_id}
            r = requests.post(url, data=body, verify=False)
            respond = json.loads(r.text)
            print respond
            result = ''
            if respond['code'] == 100000:
                tuling_result = respond['text'].replace('<br>', '  ')


                print '------------tuling_result------', tuling_result
                result = re.sub(u'图灵机器人', u'牛顿机器人', tuling_result)
                print '--------------result-----------', result
            elif respond['code'] == 200000:
                result = respond['url']
            elif respond['code'] == 302000:
                result = respond['text']
            elif respond['code'] == 308000:
                result = respond['text']
            else:
                result = respond['text'].replace('<br>', '  ')

            print '    ROBOT:', result
            return result
        else:
            return u"知道啦"


    def auto_switch(self, msg):
        msg_data = msg['content']['data']
        stop_cmd = [u'退下', u'走开', u'关闭', u'关掉', u'休息', u'滚开', u'闭嘴', u'去死']
        start_cmd = [u'出来', u'启动', u'工作',u'接客', u'干活']
        if self.robot_switch:
            for i in stop_cmd:
                if i == msg_data:
                    self.robot_switch = False
                    self.send_msg_by_uid(u'[Robot]' + u'机器人已挂！阿门~~~', msg['to_user_id'])
        else:
            for i in start_cmd:
                if i == msg_data:
                    self.robot_switch = True
                    self.send_msg_by_uid(u'[Robot]' + u'哇擦！孩儿们，我胡汉三又回来了！', msg['to_user_id'])

    def handle_msg_all(self, msg):
        if not self.robot_switch and msg['msg_type_id'] != 1:
            return
        if msg['msg_type_id'] == 1 and msg['content']['type'] == 0:  # reply to self
            if msg['content']['data'] == 'quit':
                return 'break'
            self.auto_switch(msg)
        elif msg['msg_type_id'] == 4 and msg['content']['type'] == 0:  # text message from contact
            self.send_msg_by_uid(self.tuling_auto_reply(msg['user']['id'], msg['content']['data']), msg['user']['id'])
        elif msg['msg_type_id'] == 4 and msg['content']['type'] == 4:  # voice message from contact
            print 'voice message'
            msg_id = msg['msg_id']
            self.get_voice(msg_id)
            mp3_data = 'voice_' + msg_id + '.mp3'
            tuling_respond_text = self.tuling_auto_reply(msg['user']['id'], baidu_asr(mp3_data))
            respond_text = re.sub(r'图灵机器人', '牛顿机器人', tuling_respond_text)
            self.send_msg_by_uid(respond_text, msg['user']['id'])

            #respond_voice = baidu_tts(baidu_asr(respond_text))
        elif msg['msg_type_id'] == 3 and msg['content']['type'] == 0:  # group text message
            print '---------msg----------', msg
            if 'detail' in msg['content']:
                my_names = self.get_group_member_name(self.my_account['UserName'], msg['user']['id'])
                print '----------my_names-----------', my_names
                if my_names is None:
                    my_names = {}
                if 'NickName' in self.my_account and self.my_account['NickName']:
                    my_names['nickname2'] = self.my_account['NickName']
                if 'RemarkName' in self.my_account and self.my_account['RemarkName']:
                    my_names['remark_name2'] = self.my_account['RemarkName']
                print '----------my_names2-----------', my_names


                is_at_me = False
                for detail in msg['content']['detail']:
                    if detail['type'] == 'at':
                        for k in my_names:
                            if my_names[k] and my_names[k] == detail['value']:
                                is_at_me = True
                                break
                if is_at_me:
                    src_name = msg['content']['user']['name']
                    print '--------src_name-----------', src_name
                    reply = '@' + src_name + ' '
                    if msg['content']['type'] == 0:  # text message
                        reply += self.tuling_auto_reply(msg['content']['user']['id'], msg['content']['desc'])
                    elif msg['content']['type'] == 4: # voice message
                        pass
                    else:
                        reply += u"对不起，只认字，其他杂七杂八的我都不认识，,,Ծ‸Ծ,,"
                    print '-----------reply------------', reply
                    print 'msg[user][id]', msg['user']['id']
                    self.send_msg_by_uid(reply, msg['user']['id'])
                else:
                    src_name = msg['content']['user']['name']
                    print '--------not at me ---src_name-----------', src_name
                    #reply = '@' + src_name + ' '
                    print type(src_name)
                    print type(self.live_speaker)
                    print '----------live_speaker----------', self.live_speaker
                    #live_speaker = self.live_speaker.decode('utf-8')
                    live_speaker = unicode(self.live_speaker, 'utf-8')
                    print type(live_speaker)
                    print live_speaker
                    if src_name == live_speaker:
                        print 'ready'
                        reply = u'自动群转播：'
                        if msg['content']['type'] == 0:  # text message
                            #reply += self.tuling_auto_reply(msg['content']['user']['id'], msg['content']['desc'])
                            print type(msg['content']['desc'])
                            reply += msg['content']['desc']

                        elif msg['content']['type'] == 4:  # voice message
                            pass
                        else:
                            reply += u"对不起，只认字，其他杂七杂八的我都不认识，,,Ծ‸Ծ,,"
                        print '-----------reply------------', reply
                        print 'msg[user][id]', msg['user']['id']

                        #self.send_msg_by_uid(reply, msg['user']['id'])
                        print 'group_list', self.group_list

                        for group in self.group_list:

                            if group['NickName'] == unicode(self.live_major_group, 'utf-8'):
                                major_group_user_name = group['UserName']

                        print 'major_group_user_name', major_group_user_name

                        for msg_usr_id in self.group_list:
                            print msg_usr_id['UserName']
                            print msg_usr_id['UserName'] != major_group_user_name
                            if msg_usr_id['UserName'] != major_group_user_name:

                                self.send_msg_by_uid(reply, msg_usr_id['UserName'])

                    # self.send_msg_by_uid(reply, '@@7e035828a3879caac2e52315d110e81371082bb8b5d35c23878e6c9455c06299')

    # def schedule(self):
    #     self.send_msg(u'张三', u'测试')
    #     time.sleep(1)



def main():
    bot = TulingWXBot()
    bot.DEBUG = True
    bot.conf['qr'] = 'png'

    bot.run()


if __name__ == '__main__':
    main()

