#! /usr/bin/env python
# -*- encoding: UTF-8 -*-

import rospy, os, sys
from sound_play.msg import SoundRequest
from sound_play.libsoundplay import SoundClient
from std_msgs.msg import String


def sound_translator(data):
    soundhandle.say(data.data)


def sound_say_init():
    rospy.init_node('say_node', anonymous = True)
    rospy.Subscriber('sound_say', String, sound_translator)
    rospy.spin()


if __name__ == '__main__':
    soundhandle = SoundClient()
    rospy.sleep(1)
    sound_say_init()
