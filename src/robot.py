#!/usr/bin/bash python
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

from geometry_msgs.msg import PoseWithCovarianceStamped
from geometry_msgs.msg import PointStamped
from geometry_msgs.msg import PoseStamped
from nav_msgs.msg import Path, OccupancyGrid, MapMetaData
from astar import AStar
from tf import TransformListener
from astar import Cell

def init_pose(msg):
    global robot
    print ("initial pose received")
    angle = quant_to_degrees(msg.pose.pose.orientation)
    varX = int(round(msg.pose.pose.position.x*20))
    varY = int(round(msg.pose.pose.position.y*20))
    robot.start = [varX,varY]
    print robot.curAngle

# def callback_pose(current_pose):
#     x = current_pose.pose.pose.position.x
#     y = current_pose.pose.pose.position.y
#     roll,pitch,yaw = euler_from_quaternion([current_pose,pose,pose.orientation.x,
#                                             current_pose,pose,pose.orientation.y,
#                                             current_pose,pose,pose.orientation.z,
#                                             current_pose,pose,pose.orientation.w])
#
#/initialpose
#/move_base_simple/goal
#/clicked_point


def goal(msg):
	global robot
	print "new goal received"
	print msg.pose.position.x

	varX = int(round(msg.pose.position.x*20))
	varY = int(round(msg.pose.position.y*20))
	pos=[varX,varY]
	robot.goal=pos
	print("robot goal is ",robot.goal)
	robot.goalAngle = quant_to_degrees(msg.pose.orientation)
	if len(robot.current):
		start_nav()


def clicked_point(msg):
    global robot
    print "new point in rviz was clicked"
    print msg
    varX = int(round(msg.point.x*20))
    varY = int(round(msg.point.y*20))
    pos=[varX,varY]
    robot.current = pos
    print ("robot current is", robot.current)

def map_callback(msg):
		global robot
		cells = []
		i=0
		tmp=[]
		rows = msg.info.height
		#rows = 26
		cols = msg.info.width
		robot.rows=rows
		robot.cols=cols
		#cols = 27
		for row in range(0,rows):
			for col in range (0,cols):
				data= msg.data[i]
				if data == -1 or data == 100:
					wall = True
				else:
					wall = False
				cell = Cell([row,col],wall)
				cells.append(cell)
				i+=1
		print "done building 2d grid"
		robot.cells = cells

		print(rows, cols)
		print"done building 2d grid"


		# start = [77, 33]
		# goal = [111, 57]
		# cells = []
		# tmp = []
		# # rows = msg.info.height
		# cells = []
		# cols = 0
		# with open('robo_map.txt') as file:
		# 	reader = csv.reader(file, delimiter=' ')
		# 	rows = 0;
		# 	for line in reader:
		# 		if len(line) > cols:
		# 			cols = len(line)
		# 		for col in range(len(line)):
		# 			data = int(line[col])
		# 			if data == -1 or data == 1:
		# 				wall = True
		# 			else:
		# 				wall = False
		# 			cell = Cell([rows, col], wall)
		# 			cells.append(cell)

		# 		rows += 1
		# rows -= 1

def start_nav():
	print"in nav"
	global robot
	start = robot.current
	goal = robot.goal
	a = AStar(robot.cells)
	a.init_world(start, goal, robot.rows, robot.cols)
	directions = []
	if a.init:
		print "getting directions"
		directions = a.main()
		print(directions)
		for direction in directions:
			print direction[0],direction[1],
		robot.travel(directions)
	else:
		print "no init"
def tf_callback(t):
	print "in tf callback"

class Robot(object):
	def __init__(self):
		self.linear_v = 0.5
		self.angular_v = 0.2
		self.pi = 3.14
		self.curX=0
		self.curY=0
		self.current=[self.curX,self.curY]
		self.orgX = 0 
		self.orgY=0
		self.start = []
		self.curAngle=0
		self.twist=Twist()
		self.publisher = rospy.Publisher('/mobile_base/commands/velocity',Twist,queue_size=10)
		self.counter=1
		self.reset = rospy.Publisher('/mobile_base/commands/reset_odometry',Empty,queue_size=1)
		self.goal = []
		self.goalAngle=0
		self.cells = []
		self.rows = 0
		self.cols=0

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
				print "goal orientation: ", self.goalAngle
				angle = self.get_angle(self.goal)
				if angle>self.curAngle:
					angle = angle - self.curAngle
				else:
					angle = self.curAngle - angle
				self.move_turn(angle)

				self.twist.angular.z = 0
				self.publisher.publish(self.twist)
				self.move_forward(.05/self.linear_v)
				#self.move_distance(.005)

				self.twist.linear.x = 0
				self.publisher.publish(self.twist)

				print "finished moving"

	def move_turn(self,angle):
		self.twist.linear.x = 0 
		if angle > 180:
			self.twist.angular.z = -self.angular_v
		else:
			self.twist.angular.z = self.angular_v

		rate = rospy.Duration(.02)
		while  (int((self.curAngle)) <= int(abs(angle))):
			if int(abs(angle))-int((self.curAngle))<10:
				self.twist.angular.z=.01

			print (int(round((self.curAngle))))
			print int(round(angle))
			self.publisher.publish(self.twist)
			rospy.sleep(rate)

		self.twist.angular.z = 0
		self.publisher.publish(self.twist)
		
		

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
			self.publisher.publish(twist)

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
		return math.sqrt(math.pow(goal[0]-current[0],2)+math.pow(goal[1]-current[1],2))/.05
	def get_time(self,current,goal):
		return self.get_distance(current,goal)/float(self.get_linearSpeed())

	def get_linearSpeed(self):
		return float(self.linear_v)
	def get_agularSpeed(self):
		return float(self.angular_v)
def quant_to_degrees(msg):
	quaternion = (
		msg.x,
		msg.y,
		msg.z,
		msg.w)
	a, b, yaw = euler_from_quaternion(quaternion)
	degrees = yaw * 180 / robot.pi
	if degrees < 0:
		degrees = degrees + 360
	return degrees
def amcl_callback(msg):
		
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
	robot.curX = int(round(msg.pose.pose.position.x * 20))
	robot.curY = int(round(msg.pose.pose.position.y * 20))
	robot.current = [robot.curX,robot.curY]

if __name__ == '__main__':
	try:
		print "in main"
		robot = Robot()
		flag = 0
		print "init node"
		rospy.init_node('bot_node')
		# tf_conv = TransformListener()
		# t= 0
		# position, quaternion = tf_conv.lookupTransform("/map", "/base_link", rospy.get_rostime())
		# print position, quaternion
		rospy.Subscriber("/initialpose", PoseWithCovarianceStamped, init_pose)
		rospy.Subscriber("/goal", PoseStamped, goal)
		rospy.Subscriber("/clicked_point", PointStamped, clicked_point)
		#rospy.Subscriber("/map_metadata", MapMetaData, map_callback)

		rospy.Subscriber('/amcl_pose',PoseWithCovarianceStamped,amcl_callback)
		print "sub to map"
		rospy.Subscriber("/map", OccupancyGrid, map_callback)
		print "spin"
		rospy.spin()

		
	except rospy.ROSInterruptException:
		pass

