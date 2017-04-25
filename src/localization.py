#Implement Localization here
def pub_amcl:

    init_pose.pose.pose.position.x = -23.4
    init_pose.pose.pose.position.y = -12.2
    init_pose.pose.pose.position.z = 0.0

    init_pose.pose.pose.orientation.x = 0.0
    init_pose.pose.pose.orientation.y = 0.0
    init_pose.pose.pose.orientation.z = 0.0
    init_pose.pose.pose.orientation.w = 0.0

    init_pose = PoseWithCovarianceStammed()
    self.publisher = rospy.Publisher("initialpose",PostWithCovarianceStamped,queue_size = 10)
    init_pose.header.frame_id = "map"
    init_pose.header.stamp = ropsy.Time.now()

    self.publisher.publish(init_pose)

def sub_amcl:

    rospy.Subscriber("/amcl_pose",PoseWithCovarianceStammed,callback_pose)


def callback_pose(current_pose):

    x = current_pose.pose.pose.position.x
    y = current_pose.pose.pose.position.y
    roll,pitch,yaw = euler_from_quaternion([current_pose,pose,pose.orientation.x,
                                            current_pose,pose,pose.orientation.y,
                                            current_pose,pose,pose.orientation.z,
                                            current_pose,pose,pose.orientation.w])
if __name__ == '__main__':
    try:
        rospy.init_node('loc_node')

    except rospy.ROSInterruptException:
        pass