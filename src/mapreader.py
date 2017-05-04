#!/usr/bin/env python
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Point
from nav_msgs.msg import Odometry,Path,OccupancyGrid
from math import atan
from math import asin
from std_msgs.msg import Empty
from tf.transformations import euler_from_quaternion
import rospy
import time
import math
import csv


def map_callback(msg):
		f=open('map.txt', 'w')
		c=0
		for h in msg.data:
			if c%704==0 and c !=0:
				value=str(h)+('\n')
				f.write(value)
			else:
				value=str(h)+' '
				f.write(value)
			c=c+1
				




if __name__ == '__main__':
	try:
		rospy.init_node('reader_node')
		print ("sub to map")
		rospy.Subscriber("/map", OccupancyGrid, map_callback)
		print ("spin")
		rospy.spin()
		
	except rospy.ROSInterruptException:
		pass




