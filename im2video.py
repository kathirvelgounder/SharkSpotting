"""Usage: python3 im2video.py videopath image_delay destinationfolder
image_delay I recommend 1, which means you screenshot every 1 second, you can 
do 0.5 seconds or 3 seconds or anythin except 0 or below. Also Make sure
destination folder exists before running script. Sorry for bad code wrote
it in a hurry"""


import os
import cv2
import glob
import numpy as np 
import sys

def max_label(name, folder):
    '''Look at a folder and check the files with pattern "name_###.jpg" to extract the
    largest label present.'''
    
    path_pattern = os.path.join(folder, name + "_*.jpg")
    existing_files = glob.glob(path_pattern)
    if not existing_files:
        biggest_label = 0
    else:
        existing_labels = map(lambda s: int(s.split('_')[-1].split('.')[0]), existing_files)
        biggest_label = max(existing_labels)
    return biggest_label

def extract_images_from_video(video, folder=None, delay=1, name="file", max_images=250, silent=False):    
    vidcap = cv2.VideoCapture(video)
    count = 0
    num_images = 0
    if not folder:
        folder = os.getcwd()
    label = max_label(name, folder)
    success = True
    fps = int(vidcap.get(cv2.CAP_PROP_FPS))

    while success and num_images < max_images:
        success, image = vidcap.read()
        num_images += 1
        label += 1
        file_name = name + "_" + str(label) + ".jpg"
        path = os.path.join(folder, file_name)
        if image is None:
            continue
        cv2.imwrite(path, image)
        if cv2.imread(path) is None:
            os.remove(path)
        else:
            if not silent:
                print(f'Image successfully written at {path}')

        count += delay*fps
        vidcap.set(1, count)

if __name__ == "__main__":
    videopath = sys.argv[1]
    image_delay = float(sys.argv[2])
    destinationfolder = sys.argv[3]
    extract_images_from_video(videopath, folder=destinationfolder, delay=image_delay, name=destinationfolder, max_images=200, silent=False)
