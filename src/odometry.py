#!/usr/bin/env python
import rospy
import time
import math
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion
from geometry_msgs.msg import Point, Twist



x = 0.0
y = 0.0 
theta = 0.0
 
def new_odometry(msg):
    global x
    global y
    global theta
 
    x = msg.pose.pose.position.x
    y = msg.pose.pose.position.y
 
    rot_q = msg.pose.pose.orientation
    (roll, pitch, theta) = euler_from_quaternion([rot_q.x, rot_q.y, rot_q.z, rot_q.w])
 


rospy.init_node("vector_controller")
 
sub = rospy.Subscriber("/odom", Odometry, new_odometry)
pub = rospy.Publisher("/vector/cmd_vel", Twist, queue_size = 1)
 
speed = Twist()
 
r = rospy.Rate(50) #50 Hz
 
 
 
last_x=0
last_y=0

r_max_p_term = 0.3

get_last_loc_flag = True
input_state = True
yaw_setpoint = 0
r_setpoint = 0
pi = 3.14

while not rospy.is_shutdown():


 
    if input_state :
        yaw_setpoint = input("YAW?(deg)")
        r_setpoint = input("R?(m)")
        yaw_setpoint = yaw_setpoint * pi / 180
        input_state = False
    else:

        yaw_error = yaw_setpoint - theta
        speed.angular.z = yaw_error * 10
        if yaw_error < 0.01 and yaw_error > -0.01:
            if get_last_loc_flag :
                last_x = x
                last_y = y
                get_last_loc_flag = False
            r_error = r_setpoint - math.sqrt((x-last_x)**2 + (y-last_y)**2)
            r_p_term = r_error * 2
            if r_p_term > r_max_p_term :   
                r_p_term = r_max_p_term
            speed.linear.x = r_p_term
            if r_error < 0.001 and r_error > -0.001:
                speed.linear.x = 0
                get_last_loc_flag = True
                input_state = True
                print("done!")

 
        pub.publish(speed)

    r.sleep()    