import numpy as np
import rosbag
import os
from cv_bridge import CvBridge
from sensor_msgs.msg import CompressedImage
from IPython import embed
import glob
import cv2
import time
import pickle


base_path = './distribution1.pkl'
count=0
name=0

episodes = []
episodes_new = []
episodes_test = []


if __name__ == '__main__':

    # for episode_path in glob.glob('/lab/html/kiran/beonav/*.bag'):
    #     bridge = CvBridge()
    #     bag = rosbag.Bag(episode_path)

    #     start_time = None
    #     end_time = None
    #     episode_length = None

    #     for _, msg, t in bag.read_messages(topics=['/cam1/color/image_raw/compressed']):               
    #         # img = None
    #         #print(df['header.seq'][i], msg.header.seq)
    #         # i = msg.header.seq
    #         # img = bridge.compressed_imgmsg_to_cv2(msg)
    #         # img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    #         # cv2.imwrite(base_path +episode_path.split('/')[-1][:-4]+'_'+ str(t) + '.jpg', img)
    #         # count+=1
    #         # name+=1
    #         if start_time is None:
    #             start_time = t
    #         # Always update end time to the current message timestamp
    #         end_time = t

    #     # Calculate the duration of the episode
    #     if start_time is not None and end_time is not None:
    #         episode_length = end_time - start_time
            
    #     if episode_length is not None:
    #         episodes.append(episode_length)

    # with open('./distribution.pkl', 'wb') as f:  # 'wb' stands for write binary mode
    #     pickle.dump(episodes, f)

    for episode_path in glob.glob('/lab/html/kiran/beonav/newtest/*.bag'):
        bridge = CvBridge()
        bag = rosbag.Bag(episode_path)


        episode_length = 0

        for _, msg, t in bag.read_messages(topics=['/cam1/color/image_raw/compressed']):               
            # img = None
            #print(df['header.seq'][i], msg.header.seq)
            # i = msg.header.seq
            # img = bridge.compressed_imgmsg_to_cv2(msg)
            # img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
            # cv2.imwrite(base_path +episode_path.split('/')[-1][:-4]+'_'+ str(t) + '.jpg', img)
            # count+=1
            # name+=1
            episode_length+=1

        # Calculate the duration of the episode
            
        if episode_length != 0:
            episodes_new.append(episode_length)

    with open('./length_new.pkl', 'wb') as f:  # 'wb' stands for write binary mode
        pickle.dump(episodes_new, f)


    for episode_path in glob.glob('/lab/html/kiran/beonav/*.bag'):
        bridge = CvBridge()
        bag = rosbag.Bag(episode_path)


        episode_length = 0

        for _, msg, t in bag.read_messages(topics=['/cam1/color/image_raw/compressed']):               
            episode_length+=1

        # Calculate the duration of the episode
            
        if episode_length != 0:
            episodes.append(episode_length)

    with open('./length.pkl', 'wb') as f:  # 'wb' stands for write binary mode
        pickle.dump(episodes, f)

    for episode_path in glob.glob('/lab/html/kiran/beonav/test/*.bag'):
        bridge = CvBridge()
        bag = rosbag.Bag(episode_path)


        episode_length = 0

        for _, msg, t in bag.read_messages(topics=['/cam1/color/image_raw/compressed']):               
            episode_length+=1

        # Calculate the duration of the episode
            
        if episode_length != 0:
            episodes_test.append(episode_length)

    with open('./length_test.pkl', 'wb') as f:  # 'wb' stands for write binary mode
        pickle.dump(episodes_test, f)
