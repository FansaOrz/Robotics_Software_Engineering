#! /usr/bin/env python
# -*- encoding: UTF-8 -*-
import cv2
import dlib
import time
import rospy
from opencv_apps.msg import RotatedRectStamped
from std_msgs.msg import String
from geometry_msgs.msg import Twist


class object_track():
    def __init__(self):
        rospy.init_node("object_track")
        self.pub_vel = rospy.Publisher('/cmd_vel_mux/input/navi', Twist, queue_size=15)
        self.sub_size = rospy.Subscriber("/camshift/track_box", RotatedRectStamped, self.size_callback)
        self.x = self.y = 0
        self.cam_width = 640
        self.cam_height = 480
        self.total_time = 0
        self.dir = "none"
        self.left = (self.cam_width / 2) - (self.cam_width / 12)
        self.right = (self.cam_width / 2) + (self.cam_width / 12)
        self.top = (self.cam_height / 2) - (self.cam_height / 4)
        self.bottom = (self.cam_height / 2) + (self.cam_height / 4)
        self.size_old = 0
        self.keyboard_control()

    def size_callback(self, msg):
        twi = Twist()
        # print twi
        x = msg.rect.center.x
        y = msg.rect.center.y
        # print self.left, self.right, self.top, self.bottom
        # print "---------", x, y
        # print y, self.bottom, self.top
        if x < self.left:
            twi.angular.z = (self.cam_width / 2 - x) * .003
        elif x > self.right:
            twi.angular.z = -(x - self.cam_width / 2) * .003
            # self.pub_vel.publish(twi)
            # print "222222"
            # time.sleep(.5)
            # return
        if y < self.top:
            twi.linear.x = (self.cam_height / 2 - y) * .0005
            # self.pub_vel.publish(twi)
            # print "333333"
            # time.sleep(.5)
            # return
        elif y > self.bottom:
            twi.linear.x = -(y - self.cam_height / 2) * .0005
            # self.pub_vel.publish(twi)
            # print "444444"
            # time.sleep(.5)
            # return
        self.total_time += 1
        if self.total_time == 3:
            # print "pubpub"
            self.total_time = 0
            print twi
            self.pub_vel.publish(twi)

    def keyboard_control(self):
        print('\033[0;32m [Kamerider I] Start keyboard control \033[0m')
        command = ''
        while command != 'c':
            try:
                command = raw_input('next command : ')
                if command == 'r':
                    self.find_people()
                else:
                    print("Invalid Command!")
            except Exception as e:
                print e


if __name__ == "__main__":
    object_track()
