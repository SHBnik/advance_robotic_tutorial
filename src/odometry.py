#!/usr/bin/env python3
import rospy
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion



x = 0.0
y = 0.0 
theta = 0.0

PI = 3.1415926535897

def new_odometry(msg):
    global x
    global y
    global theta
 
    x = msg.pose.pose.position.x
    y = msg.pose.pose.position.y
 
    rot_q = msg.pose.pose.orientation
    (roll, pitch, theta) = euler_from_quaternion([rot_q.x, rot_q.y, rot_q.z, rot_q.w])
 


rospy.init_node("odometry_data_capture")
 
sub = rospy.Subscriber("/odom", Odometry, new_odometry)


r = rospy.Rate(5) #5 Hz
 
 

while not rospy.is_shutdown():
	rospy.loginfo("X=%f Y=%f theta=%f"%(x,y,theta*180/PI))

	r.sleep()    