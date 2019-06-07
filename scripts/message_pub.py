#!/usr/bin/env python
# -*- coding: utf-8 -*-
import rospy, os, sys 
from sound_play.msg import SoundRequest
from sound_play.libsoundplay import SoundClient
from std_msgs.msg import String
import re
reload(sys)
sys.setdefaultencoding("utf-8")

def task(msg):
    line=msg
    pattern=r"medicine"
    if re.search(pattern,line)!=None:
        print "take medicine"
        if re.search(r"1",line)!=None or re.search(r"one",line)!=None:
            return "medicine", "1"
        if re.search(r"2",line)!=None or re.search(r"two",line)!=None:
            return "medicine", "2"
        
    pattern=r"check"
    if re.search(pattern,line)!=None:
        print "check patient's condition"
        if re.search(r"1",line)!=None or re.search(r"one",line)!=None:
            return "check", "1"
        if re.search(r"2",line)!=None or re.search(r"two",line)!=None:
            return "check", "2"
    return "none", "none"


def sleep(t):
    try:
        rospy.sleep(t)
    except:
        pass


if __name__=='__main__':
    rospy.init_node('message_pub',anonymous=True)
    taskcontent_pub = rospy.Publisher('/task_content', String, queue_size=10)
    tasknum_pub=rospy.Publisher("/task_num",String,queue_size=10)
    pub=rospy.Publisher("/weichat",String,queue_size=10)
    rate=rospy.Rate(10)
    
    while not rospy.is_shutdown():
        if os.path.exists("weichat_message.txt"):
            #print "into process"
            message=open("weichat_message.txt","r")
            str=message.readline()
            order_content,order_num=task(str)
            if str!="":
                rospy.loginfo(str)
                taskcontent_pub.publish(order_content)
                tasknum_pub.publish(order_num)
                pub.publish(str)
            message.close()
            message=open("weichat_message.txt","w")
            message.truncate()
            message.close()
            rate.sleep()
    rospy.sleep(1)