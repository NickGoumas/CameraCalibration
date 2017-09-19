# OpenCV Camera Calibration

Following the OpenCV Camera Calibration tutorial found here: http://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_calib3d/py_calibration/py_calibration.html

I'm currently interested in the intrinsic calibration values so I may neglect rotation and translation vectors in my code/comments a bit. The script is fairly straightforward but I may do a small writeup here in the near future.

### Flags
#### -f --fast
Forces the flag "cv2.CALIB_CB_FAST_CHECK" in the cv2.findChessboardCorners() function. Using this will allow the process to run much faster but it will miss some checkerboards. 

#### -p --preview
Shows a preview on screen of each image where checkerboard corners are found. The image will have the corners highlighted.

#### -c --cover
Generates an image overlay showing all of the detected checkerboards. This is useful to see how much coverage your calibration images are getting. The overlay is placed on the first image in the passed directory. 