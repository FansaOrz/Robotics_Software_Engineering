#! /usr/bin/env python
# -*- encoding: UTF-8 -*-
import cv2
import dlib
import time
import rospy
import actionlib
from std_srvs.srv import Empty
from std_msgs.msg import String
from sound_play.msg import SoundRequest
from sound_play.libsoundplay import SoundClient
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from geometry_msgs.msg import Twist, PoseStamped


class navigation_node():
    def __init__(self):
        rospy.init_node("navigation_node")
        self.sound_client = SoundClient()
        self.point_dataset = self.load_waypoint("/home/fansa/Src/normal/catkin_ws/src/Robotics_Software_Engineering/scripts/waypoints_help.txt")
        self.nav_as = actionlib.SimpleActionClient("/move_base", MoveBaseAction)
        self.map_clear_srv = rospy.ServiceProxy('/move_base/clear_costmaps', Empty)
        self.content_sub = rospy.Subscriber("/task_content", String, self.content_cb)
        self.finished_sub = rospy.Subscriber("/finished", String, self.speech_cb)
        self.num_sub = rospy.Subscriber("/task_num", String, self.num_cb)
        self.reach_pub = rospy.Publisher("/patient_reach", String, queue_size=15)

        rospy.spin()

    def load_waypoint(self, file_name):
        curr_pos = PoseStamped()
        f = open(file_name, 'r')
        sourceInLines = f.readlines()
        dataset_points = {}
        for line in sourceInLines:
            temp1 = line.strip('\n')
            temp2 = temp1.split(',')
            point_temp = MoveBaseGoal()
            point_temp.target_pose.header.frame_id = '/map'
            point_temp.target_pose.header.stamp = curr_pos.header.stamp
            point_temp.target_pose.header.seq = curr_pos.header.seq
            point_temp.target_pose.pose.position.x = float(temp2[1])
            point_temp.target_pose.pose.position.y = float(temp2[2])
            point_temp.target_pose.pose.position.z = float(temp2[3])
            point_temp.target_pose.pose.orientation.x = float(temp2[4])
            point_temp.target_pose.pose.orientation.y = float(temp2[5])
            point_temp.target_pose.pose.orientation.z = float(temp2[6])
            point_temp.target_pose.pose.orientation.w = float(temp2[7])
            dataset_points[temp2[0]] = point_temp
        print ("↓↓↓↓↓↓↓↓↓↓↓↓point↓↓↓↓↓↓↓↓↓↓↓↓")
        print (dataset_points)
        print ("↑↑↑↑↑↑↑↑↑↑↑↑point↑↑↑↑↑↑↑↑↑↑↑↑")
        print ('\033[0;32m [Kamerider I] Points Loaded! \033[0m')
        return dataset_points

    def speech_cb(self, msg):
        self.go_to_waypoint(self.point_dataset["start"], "start", "start")
        self.sound_client.say("over.")

    def content_cb(self, msg):
        if msg.data == "medicine":
            self.go_to_waypoint(self.point_dataset["medicine"], "point1", "first")
            self.sound_client.say("please, give me the medicine.")
            time.sleep(5)
            self.go_to_waypoint(self.point_dataset["patient"], "point2", "first")
            self.reach_pub.publish("yes")
        elif msg.data == "check":
            self.go_to_waypoint(self.point_dataset["patient"], "point1", "first")
        else:
            print("\033[0;33m\t[Kamerider W]: Invalid content!!!\033[0m")

    def num_cb(self, msg):
        if msg.data == "1":
            self.go_to_waypoint(self.point_dataset["point1"], "point1", "first")
        elif msg.data == "stop":
            self.go_to_waypoint(self.point_dataset["point2"], "point1", "first")
        else:
            print("\033[0;33m\t[Kamerider W]: Invalid content!!!\033[0m")

    def go_to_waypoint(self, Point, destination, label="none"): # Point代表目标点 destination代表目标点的文本 label
        self.nav_as.send_goal(Point)
        self.map_clear_srv()
        count_time = 0
        # 等于3的时候就是到达目的地了
        while self.nav_as.get_state() != 3:
            count_time += 1
            time.sleep(1)
            if count_time == 8:
                self.map_clear_srv()
                count_time = 0
        # self.TextToSpe.say("I have arrived at " + destination)
        if label == "none":
            return

if __name__ == "__main__":
    navigation_node()
