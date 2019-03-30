#! /usr/bin/env python
# -*- encoding: UTF-8 -*-

import rospy, os, sys
import time
from sound_play.libsoundplay import SoundClient
from std_msgs.msg import String


if __name__ == '__main__':
    rospy.init_node('say_publish', anonymous = True)
    say_pub = rospy.Publisher('/sound_say', String, queue_size=1)
    x = raw_input("data:=")
    while x != "q":
        say_pub.publish(x)
        rospy.sleep(2)
        x = raw_input("data:=")
    print "quit successfully"
