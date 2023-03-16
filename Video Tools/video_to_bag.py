#!/usr/bin/python3
import rospy
import rosbag
import cv2
from cv_bridge import CvBridge

# Set the video file path and ROS bag file path
video_file = '50p.mp4'
bag_file = 'output.bag'

# Open the video file and read the frames
cap = cv2.VideoCapture(video_file)
if not cap.isOpened():
    print('Error: could not open video file')
    exit()

# Create the ROS bag file
bag = rosbag.Bag(bag_file, 'w')

# Create a CvBridge object
bridge = CvBridge()

# Loop through the frames and add them to the ROS bag file
frame_count = 0
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    print(frame_count)
    # Convert the frame to a ROS image message
    ros_image = bridge.cv2_to_imgmsg(frame, encoding="bgr8")

    # Set the ROS message header timestamp
    ros_image.header.stamp = rospy.Time.from_sec(float(frame_count) / 30.0)

    # Write the ROS image message to the bag file
    bag.write('/camera/image_raw', ros_image, t=ros_image.header.stamp)

    frame_count += 1

cap.release()
bag.close()

print(f'Successfully converted {frame_count} frames to ROS bag format.')
