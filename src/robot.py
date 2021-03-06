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
from astar import AStar
from astar import Cell

def map_callback(msg):
		# start = [3,3]
		# goal = [8,6]
		# global robot
		# print msg.info
		# cells = []
		# i=0
		# tmp=[]
		# # rows = msg.info.height
		# rows = 26
		# # cols = msg.info.width
		# cols = 27
		# for row in range(0,rows):
		# 	for col in range (0,cols):
		# 		data= msg.data[i]
		# 		if data == -1 or data == 100:
		# 			wall = True
		# 		else:
		# 			wall = False
		# 		cell = Cell([row,col],wall)
		# 		cells.append(cell)
		# 		i+=1
		# print "done building 2d grid"
		# a = AStar(cells)
		# a.init_world(start,goal,rows,cols)
		# print len(a.cells)
		# print len(msg.data)
		# directions = a.main()
		# print directions

		start = [77, 33]
		goal = [111, 57]
		cells = []
		tmp = []
		# rows = msg.info.height
		cells = []
		cols = 0
		with open('robo_map.txt') as file:
			reader = csv.reader(file, delimiter=' ')
			rows = 0;
			for line in reader:
				if len(line) > cols:
					cols = len(line)
				for col in range(len(line)):
					data = int(line[col])
					if data == -1 or data == 1:
						wall = True
					else:
						wall = False
					cell = Cell([rows, col], wall)
					cells.append(cell)

				rows += 1
		rows -= 1

		print(rows, cols)
		print
		"done building 2d grid"
		print
		time.localtime(time.time()), "started finding path"
		a = AStar(cells)
		a.init_world(start, goal, rows, cols)
		directions = []
		if a.init:
			directions = a.main()
		print(directions)


	
class Robot(object):
	def __init__(self):
		self.linear_v = 0.5
		self.angular_v = 0.4
		self.pi = 3.14
		self.curX=0
		self.curY=0
		self.orgX = 0 
		self.orgY=0
		self.curAngle=0
		self.twist=Twist()
		self.publisher = rospy.Publisher('/mobile_base/commands/velocity',Twist,queue_size=10)
		self.counter=1
		self.reset = rospy.Publisher('/mobile_base/commands/reset_odometry',Empty,queue_size=1)

	def travel(self,points):
			global flag
			message = Empty()
			self.reset.publish(message)
			self.twist.linear.x=0
			self.twist.linear.y=0
			self.twist.linear.z=0
			self.twist.angular.x=0
			self.twist.angular.y=0
			self.twist.angular.z=0
			if flag == 0: 
					self.orgX = self.curX
					self.orgY = self.curY
					print robot.orgX
					print robot.orgY
					flag = 1

			for i in range(0, len(points)):
				current = [self.curX,self.curY]
				next = [points[i][0],points[i][1]]
				distance = self.get_distance(current,next)
				print "current ", current
				print "next", next
				print "Distance ",distance
				print "current orientation: ",self.curAngle	
				angle = self.get_angle(next)
				self.move_turn(angle)
				self.twist.angular.z = 0
				self.publisher.publish(self.twist)


				self.move_distance(distance)

				self.twist.linear.x = 0
				self.publisher.publish(self.twist)

				print "finished moving"

	def move_turn(self,angle):
		self.twist.linear.x = 0 
		if angle > 180:
			self.twist.angular.z = -self.angular_v
		else:
			self.twist.angular.z = self.angular_v


		


		rate = rospy.Rate(100)
		while  (not(int(self.curAngle)== int(angle))):				
			self.publisher.publish(self.twist)
			#rate.sleep()

		self.twist.angular.z = 0
		self.publisher.publish(self.twist)
		rospy.Rate(10).sleep()
		
		

	def move_forward(self,seconds):
		self.twist.linear.x = self.linear_v
		self.twist.angular.z = 0

		
		t0 = rospy.Duration.from_sec(seconds)
		s = rospy.Time.now()
		rate = rospy.Rate(10)
		while ((rospy.Time.now() - s).to_sec() < t0.to_sec()):
			self.publisher.publish(self.twist)
			rate.sleep()
	def move_distance(self,distance):
		self.twist.angular.z = 0
		startX = self.curX
		startY = self.curY
		traveled = 0 
		self.twist.linear.x = self.linear_v
		rate = rospy.Rate(10)
		while traveled < distance:
			self.publisher.publish(self.twist)	
			traveled = self.get_distance([self.curX,self.curY],[startX,startY])
			rate.sleep()
		self.twist.linear.x = 0
		self.publisher.publish(self.twist)

	def move_back(self,seconds):
		self.twist.linear.x = -self.linear_v
		self.twist.linear.y = 0
		self.twist.linear.z = 0
		self.twist.angular.x = 0
		self.twist.angular.y = 0
		self.twist.angular.z = 0

		t0 = rospy.Duration(seconds)
		s = rospy.Time.now()
		while rospy.Time.now().to_sec() - s.to_sec() < t0.to_sec():
			publisher.publish(twist)

	def set_velocity(self,linear_v,angular_v):
			self.linear_v= linear_v
			self.angular_v = angular_v

	def get_angle(self, goal):
		
		angle = math.atan2(goal[1]-self.curY,goal[0]-self.curX)
		angle = math.degrees(angle)
		if angle < 0:
			angle = angle + 360
		print "angel from get angle ; " , angle	
		return angle

	def get_distance(self,current,goal):
	
		return math.sqrt(math.pow(goal[0]-current[0],2)+math.pow(goal[1]-current[1],2))
	def get_time(self,current,goal):
		return self.get_distance(current,goal)/float(self.get_linearSpeed())

	def get_linearSpeed(self):
		return float(self.linear_v)
	def get_agularSpeed(self):
		return float(self.angular_v)
		
def odom_callback(msg):
		
	global robot
	quaternion = (
	msg.pose.pose.orientation.x,
	msg.pose.pose.orientation.y,
	msg.pose.pose.orientation.z,
	msg.pose.pose.orientation.w)
	a,b,yaw = euler_from_quaternion(quaternion)
	degrees = yaw * 180 / robot.pi
	if degrees < 0:
		degrees = degrees + 360
	robot.curAngle = degrees
	robot.curX = msg.pose.pose.position.x
	robot.curY = msg.pose.pose.position.y

if __name__ == '__main__':
	try:
		print "in main"
		robot = Robot()
		flag = 0
		print "init node"
		rospy.init_node('bot_node')
		#rospy.Subscriber('odom',Odometry,odom_callback)
		print "sub to map"
		rospy.Subscriber("/map", OccupancyGrid, map_callback)
		print "spin"
		rospy.spin()
		
	except rospy.ROSInterruptException:
		pass

