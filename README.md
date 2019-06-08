# Robotics_Software_Engineering
Turtlebot's navigation will be used to walk from the starting point to the pharmacy to get what the patient needs, then walk to the patient's bedside and hand it to the patient. After that, it starts to recognize the patient's current state through vision and acquire the patient's daily situation through human-robot interaction through voice.
To realize Turtlebot navigation, map_server should be used to load a pre-built map. Gmapping is the most commonly used mapping method in ROS. Gmapping is an open source SLAM algorithm based on the filtering SLAM framework, which combines laser information with odometer information. At the same time, Gmapping is based on RBpf particle filter algorithm, which means the process of positioning and map building is separated, and the positioning is followed by the map building. With the map, we used the AMCL (adaptive Monte Carlo Localization) algorithm for autonomous Localization of the robot. In the process of moving, the robot compared the data of the laser sensor with the existing map, and calculated the possible position of the robot based on the information of the odometer. In terms of robot path planning and controller, we mainly used the move_base Package. Move_base used dijkstra algorithm for path planning. In order to make the robot travel with maximum efficiency, it fitted the path into Bessel curve, and finally used the controller to control Turtlebot for autonomous navigation.
Since our robot is used in a hospital, the safety of the robot is the most important. In the autonomous navigation process of the robot, move_base USES DWA (dynamic window approach) to realize real-time obstacle avoidance function, while Turtlebot has bumper sensors that can immediately return when it touches obstacles.
