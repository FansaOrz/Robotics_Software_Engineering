#!/usr/bin/env python
# -*- coding: utf-8 -*-
import itchat
import time
from itchat.content import *
import os, sys
from std_msgs.msg import String
import  thread
import gender_predict



rec_tmp_dir = os.path.join(os.getcwd(), 'tmp/')

rec_msg_dict = {}



@itchat.msg_register([TEXT, PICTURE, RECORDING, ATTACHMENT, VIDEO], isFriendChat=True)
def handle_friend_msg(msg):
    msg_id = msg['MsgId']
    msg_from_user = msg['User']['NickName']
    msg_content = ''
    
    msg_time_rec = time.strftime("%Y-%m-%d %H:%M%S", time.localtime())
    msg_create_time = msg['CreateTime']
    msg_type = msg['Type']

    if msg['Type'] == 'Text':
        message=open("weichat_message.txt","w")
        msg_content = str(msg['Content'])
        message.write(msg_content)
        message.close()
    elif msg['Type'] == 'Picture' \
            or msg['Type'] == 'Recording' \
            or msg['Type'] == 'Video' \
            or msg['Type'] == 'Attachment':
        msg_content = r"" + msg['FileName']
        msg['Text'](rec_tmp_dir + msg['FileName'])
    rec_msg_dict.update({
        msg_id: {
            'msg_from_user': msg_from_user,
            'msg_time_rec': msg_time_rec,
            'msg_create_time': msg_create_time,
            'msg_type': msg_type,
            'msg_content': msg_content
        }
    })
    print(msg)

def pub_message(msg):
    while not os.path.exists("./capture.jpg"):
        tem=0
    message = gender_predict.gender("./capture.jpg")
    name = itchat.search_friends(name=u'胡子琦')
    jack = name[0]["UserName"]

    message_list = [u'Hey,dude', u'Are you ok?', u'Bye~']
    itchat.send(message, jack)

    picture = "./capture.jpg"
    itchat.send_image(picture, jack)
        
        


    

if __name__ == '__main__':
    if not os.path.exists(rec_tmp_dir):
        os.mkdir(rec_tmp_dir)
    itchat.auto_login()
    friends_list = itchat.get_friends(update=True)
    arg=tuple([1])
    thread.start_new_thread(pub_message,arg)

    itchat.run()




# @itchat.msg_register(itchat.content.TEXT)
# def reply_msg(msg):
#     print("recive a message: ",msg.text)
#     print>>message,(msg.text)

# if __name__=='__main__':
#     itchat.auto_login()
#     time.sleep(5)
#     itchat.send("send the message",toUserName="filehelper")
#     itchat.run()

# principal=1000
# rate=0.05
# numyears=5
# year=1
# f=open("out.txt","w") 
# while year<=numyears:
#     principal=principal*(1+rate)
#     print>>f,"%3d %0.2f"%(year,principal)
#     year+=1
# f.close()


