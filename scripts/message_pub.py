#!/usr/bin/env python
# -*- coding: utf-8 -*-
import rospy, os, sys
from sound_play.msg import SoundRequest
from sound_play.libsoundplay import SoundClient
from std_msgs.msg import String
import re
reload(sys)
sys.setdefaultencoding("utf-8")

def sleep(t):
    try:
        rospy.sleep(t)
    except:
        pass

if __name__=='__main__':
    rospy.init_node('message_pub',anonymous=True)
    # taskcontent_pub = rospy.Publisher('/task_content', String, queue_size=10)
    # tasknum_pub=rospy.Publisher("/task_num",String,queue_size=10)
    pub=rospy.Publisher("/control_command",String,queue_size=10)
    rate=rospy.Rate(10)
    
    while not rospy.is_shutdown():
        if os.path.exists("weichat_message.txt"):
            message=open("weichat_message.txt","r")
            str_=message.readline()
            order_content,order_num=task(str_)
            if str_!="":
                rospy.loginfo(str_)
                order_content = "wechat:" + order_content
                taskcontent_pub.publish(order_content)
                tasknum_pub.publish(order_num)
                pub.publish(str_)
            message.close()
            message=open("weichat_message.txt","w")
            message.truncate()
            message.close()
            rate.sleep()
    rospy.sleep(1)