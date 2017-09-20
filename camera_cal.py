import os
import numpy as np
import argparse
import cv2
import pickle


parser = argparse.ArgumentParser(
    description='utility to calculate camera calibration values. Saved to pickle file.')
parser.add_argument('path', help='Name of directory containing images.')
parser.add_argument('-f', '--fast', 
                    help='use cv2.CALIB_CB_FAST_CHECK to find corners.', 
                    action='store_true')
parser.add_argument('-p', '--preview', 
                    help='display preview of detected checkerboard corners.',
                    action='store_true')
parser.add_argument('-c', '--cover', 
                    help='display coverage of checkerboards found.',
                    action='store_true')

args = parser.parse_args()

def get_image_list(img_dir):
    filename_list = os.listdir(img_dir)
    filepath_list = []
    for i in filename_list:
        filepath_list.append(os.getcwd() + '/' + args.path + i)
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
    cv2.drawChessboardCorners(img, (9,6), corners, corners_found)
    cv2.namedWindow('Preview', flags=cv2.WINDOW_NORMAL)
    cv2.imshow('Preview', img)
    cv2.waitKey(5000)


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
    return rms_error, mtx, dist, rvecs, tvecs, imgpoints, objpoints

def pickle_cal_values(error, mtx, dist, rvecs, tvecs):
    # Save calibration values as a pickle file.
    calibration_pickle = {}
    calibration_pickle['error'] = error
    calibration_pickle['mtx'] = mtx
    calibration_pickle['dist'] = dist
    calibration_pickle['rvecs'] = rvecs
    calibration_pickle['tvecs'] = tvecs
    pickle.dump(calibration_pickle, open('calibration_pickle.p', 'wb'))
    print('Calibration values saved.')

def coverage_map(img, imgpoints):
    overlay = np.zeros_like(img)
    hot_pink = (147,20,255)
    for all_corners in imgpoints:
        origin = tuple(all_corners[0])
        corner1 = tuple(all_corners[8])
        corner2 = tuple(all_corners[53])
        corner3 = tuple(all_corners[45])
        
        main_corners = np.array([[origin, corner1, corner2, corner3]], dtype=np.int32)
        cv2.fillPoly(overlay, main_corners, hot_pink)
    img = cv2.addWeighted(overlay, 1, img, .75, 0)
    return img


cal_image_list = get_image_list(args.path)

objp = create_points()

rms_error, mtx, dist, rvecs, tvecs, imgpoints, objpoints = gen_cal_data(cal_image_list, objp, 
                                                    args.fast, args.preview)

# Display the rms re-projection error in pixels.
print('Average re-projection error:', round(rms_error, 5))

pickle_cal_values(rms_error, mtx, dist, rvecs, tvecs)

if args.cover == True:
    
    img = coverage_map(cv2.imread(cal_image_list[0]), imgpoints)
    
    cv2.namedWindow('Preview', flags=cv2.WINDOW_NORMAL)
    cv2.imshow('Preview', img)
    cv2.waitKey(0)
    
    

else:
    pass

