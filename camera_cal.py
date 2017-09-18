import os
import numpy as np
import argparse
import cv2
import pickle
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


parser = argparse.ArgumentParser(
    description='utility to calculate camera calibration values. Saved to pickle file.')
parser.add_argument('path', help='Name of directory containing images.')
parser.add_argument('-f', '--fast', 
                    help='use cv2.CALIB_CB_FAST_CHECK to find corners.', 
                    action='store_true')
parser.add_argument('-p', '--preview', 
                    help='display preview of detected checkerboard corners.',
                    action='store_true')

args = parser.parse_args()

plt.ion() #Turn on matplotlib interactive mode. Allows plt.close() to work.

def get_image_list(img_dir):
    filename_list = os.listdir(img_dir)
    filepath_list = []
    for i in filename_list:
        filepath_list.append(os.getcwd() + '/' + args.path + '/' + i)
    #print(filepath_list)
    return filepath_list

def create_points(checkerboard_rows=7, checkerboard_cols=10):
    # Prepare object points, (0,0,0), (1,0,0), (2,0,0)...
    row_points = checkerboard_rows - 1
    col_points = checkerboard_cols - 1

    objp = np.zeros((row_points*col_points,3), np.float32)
    objp[:,:2] = np.mgrid[0:col_points, 0:row_points].T.reshape(-1,2)
    return objp

def preview_found_corners(img, corners, corners_found):
    # img is converted to RGB so pyplot preview is correct.
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    cv2.drawChessboardCorners(img, (9,6), corners, corners_found)
    plt.close()
    plt.imshow(img)
    plt.show()
    plt.pause(1) # Pause in seconds

def gen_cal_data(cal_image_list, objp, fast, preview):
    # Arrays to store object and image points.
    objpoints = [] # 3D points
    imgpoints = [] # 2D points.

    # Iterate though the list and look for chessboard corners.
    for filename in cal_image_list:
        img = cv2.imread(filename)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        if fast == True:
            corners_found, corners = cv2.findChessboardCorners(gray, (9,6), flags=cv2.CALIB_CB_FAST_CHECK)
        else:
            corners_found, corners = cv2.findChessboardCorners(gray, (9,6) )

        if corners_found == True:
            objpoints.append(objp)
            imgpoints.append(corners)
            print('   Corners found:', filename)
            if preview == True:
                preview_found_corners(img, corners, corners_found)
            
        elif corners_found != True:
            print('No corners found:', filename)

    # Create flipped image size.
    img_size = (img.shape[1], img.shape[0])

    # Calibrate camera with object and image points. 
    rms_error, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, img_size,None,None)
    return rms_error, mtx, dist, rvecs, tvecs

def pickle_cal_values(error, mtx, dist, rvecs, tvecs):
    # Save calibration values as a pickle file.
    calibration_pickle = {}
    calibration_pickle['error'] = error
    calibration_pickle['mtx'] = mtx
    calibration_pickle['dist'] = dist
    calibration_pickle['rvecs'] = rvecs
    calibration_pickle['tvecs'] = tvecs
    pickle.dump(calibration_pickle, open('calibration_pickle.p', 'wb'))



cal_image_list = get_image_list(args.path)

objp = create_points()

rms_error, mtx, dist, rvecs, tvecs = gen_cal_data(cal_image_list, objp, 
                                                    args.fast, args.preview)
# Display the rms re-projection error in pixels.
print('Average re-projection error:', round(rms_error, 5))

pickle_cal_values(rms_error, mtx, dist, rvecs, tvecs)