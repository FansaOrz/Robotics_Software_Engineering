#! /usr/bin/env python
# -*- encoding: UTF-8 -*-
import qi
import os
import time
import rospy
import atexit
from turtlebot_msgs.srv import SetFollowState
import thread
from threading import Thread


class follower_ser():

    def __init__(self):
        rospy.init_node("control_follower")
        self.keyboard_control()

    def control_follow(self, msg):
        print "in======"
        rospy.wait_for_service('/turtlebot_follower/change_state')
        change_state = rospy.ServiceProxy('/turtlebot_follower/change_state', SetFollowState)
        response = change_state(msg)
        print "succe"

    def keyboard_control(self):
        print('\033[0;32m [Kamerider I] Start keyboard control \033[0m')
        command = ''
        while command != 'c':
            try:
                command = raw_input('next command : ')
                if command == 'r':
                    self.control_follow(1)
                elif command == 's':
                    self.control_follow(0)
                elif command == 'x':
                    break
                else:
                    print("Invalid Command!")
            except EOFError:
                print "Error!!"



if __name__ == "__main__":
    follower_ser()
