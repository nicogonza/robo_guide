#!/usr/bin/env python
from geometry_msgs.msg import Twist 
import rospy
import csv
from nav_msgs.msg import Path
from geometry_msgs.msg import Point,PoseStamped,Pose
import std_msgs.msg


def path():
	rospy.init_node('pub_node')
	path = Path()
	count = 1
	rate = rospy.Rate(10)

	publisher = rospy.Publisher('pathTopic',Path,queue_size=1, latch=True)

	with open("./input2.txt") as file: 
	      		reader = csv.reader(file, delimiter=' ')
	    		for row in reader:
				x1=int(row[0])
				y1=int(row[1])
				print(x1)
				print(y1)
				pose = PoseStamped()
				pose.header.frame_id = "odom messsage"
				pose.pose.position.x = x1
				pose.pose.position.y = y1
				
				pose.header.seq = path.header.seq+1
				pose.header.stamp = path.header.stamp
				path.poses.append(pose)
				print "end of loop"

	publisher.publish(path)	



if __name__ == '__main__':
	try:
		path()
		rospy.spin()
		
	except rospy.ROSInterruptException:pass
