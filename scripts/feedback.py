#!/usr/bin/env python
# -*- coding: utf-8 -*-
import itchat
import time
from itchat.content import *
import rospy, os, sys
from std_msgs.msg import String
import re
reload(sys)
sys.setdefaultencoding("utf-8")

status_message=0

itchat.auto_login(hotReload=True)

friends_list = itchat.get_friends(update=True)
name = itchat.search_friends(name=u'jack')
jack = name[0]["UserName"]

message_list = [u'Hey,dude',u'Are you ok?',u'Bye~']
itchat.send("message_concent",jack)

picture="/home/huziqi/catkin_ws/src/WechatApp/src/161109134009-1.jpg"
itchat.send_image(picture,jack)
#itchat.run()

def sleep(t):
    try:
        rospy.sleep(t)
    except:
        pass

def callback(data):
    status_message=data.data
    print status_message



if __name__=='__main__':
    rospy.init_node('message_pub',anonymous=True)
    rospy.Subscriber("/status", String, callback)
    rate=rospy.Rate(10)
    
    while not rospy.is_shutdown():
        
        rate.sleep()
    rospy.sleep(1)