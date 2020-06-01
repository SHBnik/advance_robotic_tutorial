#! /usr/bin/env python
 
import rospy
from sensor_msgs.msg import Range
 
def callback(msg):
    print(msg.range)
 
rospy.init_node('laser_data_capture')
sub = rospy.Subscriber('/vector/laser', Range, callback)
rospy.spin()