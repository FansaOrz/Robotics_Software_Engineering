#! /usr/bin/env python
# -*- encoding: UTF-8 -*-
import cv2
import dlib
import time
import rospy
from std_msgs.msg import String


class follower_ser():
    def __init__(self):
        rospy.init_node("find_people")
        self.pub = rospy.Publisher('/xfwords', String, queue_size=15)
        self.detector = dlib.get_frontal_face_detector()
        self.people_num = 0
        self.keyboard_control()

    def find_people(self):
        cap = cv2.VideoCapture(0)
        # cap.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 1000)
        # cap.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 600)
        success, frame = cap.read()
        while success:
            cv2.imshow("aaa", frame)
            img_np = frame.copy()
            rects = self.detector(img_np, 0)
            # print len(rects)
            if len(rects) != 0:
                if self.people_num != len(rects):
                    self.people_num = len(rects)
                    if len(rects) == 1:
                        result = "一"
                    elif len(rects) == 2:
                        result = "两"
                    elif len(rects) == 3:
                        result = "三"
                    elif len(rects) == 4:
                        result = "四"
                    elif len(rects) == 5:
                        result = "五"
                    self.pub.publish("我看到" + result + "个人")
                    time.sleep(1)
            if cv2.waitKey(1) >= 0:
                break
            success, frame = cap.read()
        cv2.destroyAllWindows()
        cap.release()

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
    follower_ser()
