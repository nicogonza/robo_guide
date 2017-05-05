#!/usr/bin/env python
#Implement Localization here
import rospy
from geometry_msgs.msg import PoseWithCovarianceStamped
from geometry_msgs.msg import PointStamped
from geometry_msgs.msg import PoseStamped
from nav_msgs.msg import Path, OccupancyGrid, MapMetaData
# def pub_amcl:

#     init_pose.pose.pose.position.x = -23.4
#     init_pose.pose.pose.position.y = -12.2
#     init_pose.pose.pose.position.z = 0.0

#     init_pose.pose.pose.orientation.x = 0.0
#     init_pose.pose.pose.orientation.y = 0.0
#     init_pose.pose.pose.orientation.z = 0.0
#     init_pose.pose.pose.orientation.w = 0.0

#     init_pose = PoseWithCovarianceStammed()
#     self.publisher = rospy.Publisher("initialpose",PostWithCovarianceStamped,queue_size = 10)
#     init_pose.header.frame_id = "map"
#     init_pose.header.stamp = ropsy.Time.now()

#     self.publisher.publish(init_pose)

# def sub_amcl:

#     rospy.Subscriber("/amcl_pose",PoseWithCovarianceStammed,callback_pose)
height = 0
width  = 0

def map_callback(msg):

    global height
    global width

    rows = msg.height
    cols = msg.width

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

    # print height

def translation(point):
    
    global height
    global width

    # ten_percent_height = height * .10
    # ten_percent_width = width * .10

    var2 = height / 9.5
    var1 = width / 11.5

    actualX = point[0] * var1
    actualY = point[1] * var2

    print actualX
    print actualY


def init_pose(msg):
    print "initial pose received"
    print msg

# def callback_pose(current_pose):
#     x = current_pose.pose.pose.position.x
#     y = current_pose.pose.pose.position.y
#     roll,pitch,yaw = euler_from_quaternion([current_pose,pose,pose.orientation.x,
#                                             current_pose,pose,pose.orientation.y,
#                                             current_pose,pose,pose.orientation.z,
#                                             current_pose,pose,pose.orientation.w])
def goal(msg):
    print "new goal received"
    print msg

def clicked_point(msg):
    print "new point in rviz was clicked"
    print msg
    varX = msg.point.x
    varY = msg.point.y
    translation([varX, varY])

if __name__ == '__main__':
    try:
        print "in the localization node"
        rospy.init_node('loc_node')
        rospy.Subscriber("/initialpose",PoseWithCovarianceStamped,init_pose)
        rospy.Subscriber("/goal",PoseStamped,goal)
        rospy.Subscriber("/clicked_point",PointStamped,clicked_point)
        rospy.Subscriber("/map_metadata", MapMetaData, map_callback)
        rospy.spin()


    except rospy.ROSInterruptException:
        pass
