#!/usr/bin/env python
# -*- coding: utf-8 -*-
import itchat
import time
from itchat.content import *
import os, sys
from std_msgs.msg import String
import thread
import rospy
from std_msgs.msg import String

rec_tmp_dir = os.path.join(os.getcwd(), 'tmp/')

rec_msg_dict = {}

rospy.init_node('message_pub', anonymous=True)
control_command_pub = rospy.Publisher("/control_command", String, queue_size=10)
wechat2total_pub = rospy.Publisher("/wechat2total", String, queue_size=10)
rate = rospy.Rate(10)

@itchat.msg_register([TEXT, PICTURE, RECORDING, ATTACHMENT, VIDEO], isFriendChat=True)
def handle_friend_msg(msg):
    msg_id = msg['MsgId']
    msg_from_user = msg['User']['NickName']
    msg_content = ''
    
    msg_time_rec = time.strftime("%Y-%m-%d %H:%M%S", time.localtime())
    msg_create_time = msg['CreateTime']
    msg_type = msg['Type']

    if msg['Type'] == 'Text':
        control_command_pub.publish("get wechat")
        wechat2total_pub.publish(str(msg['Content']))
    elif msg['Type'] == 'Picture' \
            or msg['Type'] == 'Recording' \
            or msg['Type'] == 'Video' \
            or msg['Type'] == 'Attachment':
        msg_content = r"" + msg['FileName']
        msg['Text'](rec_tmp_dir + msg['FileName'])
    rec_msg_dict.update(
        {
            msg_id: {
                'msg_from_user': msg_from_user,
                'msg_time_rec': msg_time_rec,
                'msg_create_time': msg_create_time,
                'msg_type': msg_type,
                'msg_content': msg_content
            }
        }
    )
    print(msg)


if __name__ == '__main__':
    if not os.path.exists(rec_tmp_dir):
        os.mkdir(rec_tmp_dir)
    itchat.auto_login()
    friends_list = itchat.get_friends(update=True)
    arg=tuple([1])
    thread.start_new_thread(pub_message,arg)
    itchat.run()


