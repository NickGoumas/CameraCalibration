import pickle
import cv2
import numpy
from time import sleep
import argparse
import os

parser = argparse.ArgumentParser(
    description='utility to calculate camera calibration values. Saved to pickle file.')
parser.add_argument('img_dir', help='Name of directory containing images.')
parser.add_argument('pickle',  help='Name of pickle file with cal values.')
parser.add_argument('-p', '--preview', 
                    help='display preview of detected checkerboard corners.',
                    action='store_true')
args = parser.parse_args()



def img_filepath_gen(img_dir):
    filename_list = os.listdir(img_dir)
    for filename in filename_list:
        next_img_filepath = os.getcwd() + '/' + img_dir + filename
        yield next_img_filepath

def load_cal_values(pickle_file):
    try:
        pickleData = pickle.load( open(pickle_file, 'rb') )
        mtx = pickleData['mtx']
        dist = pickleData['dist']
        print('Cal values loaded from pickle file.')
        return mtx, dist
    except:
        print('Error loading values from pickle file.')

def preview_img(img):
    cv2.namedWindow('Preview', flags=cv2.WINDOW_NORMAL)
    cv2.imshow('Preview', img)
    cv2.waitKey(1)

def save_img(img, filepath):
    filename = filepath.split('.')[0] + '_UD.png'
    cv2.imwrite(filename, img)





mtx, dist = load_cal_values(args.pickle)


for img_filepath in img_filepath_gen(args.img_dir):
    print(img_filepath)
    img = cv2.imread(img_filepath)
    img = cv2.undistort(img, mtx, dist)

    if args.preview == True:
        preview_img(img)

    save_img(img, img_filepath)

    



'''




checkerboard = mpimg.imread(img_filename)

checkerboard = cv2.undistort(checkerboard, mtx, dist)
'''
