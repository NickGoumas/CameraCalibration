# OpenCV Camera Calibration

Following the OpenCV Camera Calibration tutorial found here: http://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_calib3d/py_calibration/py_calibration.html

I'm currently interested in the intrinsic calibration values so I may neglect rotation and translation vectors in my code/comments a bit. The script is fairly straightforward but I may do a small writeup here in the near future.

## camera_cal.py

This script steps through a directory of checkerboard images. For each image it searchs for the checkerboard and if found adds the intersection points to a master list. After all images have been searched it will use the master list of points to generage the camera calibration values using the cv2.calibrateCamera(). The values will then be added to a dictionary object and saved as a pickle file.

### Flags
#### -f --fast
Forces the flag "cv2.CALIB_CB_FAST_CHECK" in the cv2.findChessboardCorners() function. Using this will allow the process to run much faster but it will miss some checkerboards. 

#### -p --preview
Shows a preview on screen of each image where checkerboard corners are found. The image will have the corners highlighted.

#### -c --cover
Generates an image overlay showing all of the detected checkerboards. This is useful to see how much coverage your calibration images are getting. The overlay is placed on the first image in the passed directory. 

## udistort_dir.py

This script steps through a directory of images using a generator function. This should allow it to work with large amounts of images withouh issue. For each image it undistorts using the cv2.undistort() function and the loaded calibration values from the saved pickle file. After the undistort operation it saves the file after appending the filename with the '_UD' marker.

### Flags