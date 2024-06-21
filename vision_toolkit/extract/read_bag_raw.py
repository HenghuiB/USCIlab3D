#!/usr/bin/env python

import rosbag
import cv2
from cv_bridge import CvBridge
import os

# Path to your ROS bag file
bag_file_path = '/lab/tmpig13d/henghui/new/cam3v.bag'

# Directory where you want to save the images
output_dir = '/lab/tmpig13d/henghui/new/cam3/imgs'
os.makedirs(output_dir, exist_ok=True)

# Initialize the CvBridge class
bridge = CvBridge()

# Open the bag file
with rosbag.Bag(bag_file_path, 'r') as bag:
    for topic, msg, t in bag.read_messages(topics=['/cam1/color/image_raw']):
        # Convert the ROS Image message to a CV image
        cv_image = bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        
        # Construct the output file path
        timestamp = t.to_nsec()
        image_filename = os.path.join(output_dir, f'{timestamp}.png')
        
        # Save the image
        cv2.imwrite(image_filename, cv_image)
        print(f'Saved image: {image_filename}')

print("Done saving all images.")
