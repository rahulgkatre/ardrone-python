import time, sys
import numpy as np
import cv2
import ps_drone

# Start using drone, connects to drone and starts subprocesses
drone = ps_drone.Drone()
drone.startup()

# Sets drone's status to good (LEDs turn green when red)
drone.reset()

# Waits until drone has done its reset, then display battery information
while (drone.getBattery()[0] == -1):
    time.sleep(0.1)
print 'Battery at ' + str(drone.getBattery()[0]) + '% - ' + str(drone.getBattery()[1])

# Give 15 basic dataset per second (default setting)
drone.useDemoMode(True)

# Go to multiconfiguration mode
drone.setConfigAllID()                                                              

# Choose resolution, view, and get the footage from the drone
drone.sdVideo()                                                                   
drone.frontCam()                                                                    
capture = cv2.VideoCapture('tcp://192.168.1.1:5555')

# Establish termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# Prepare object points like (0, 0, 0), (1, 0, 0), (2, 0, 0), ... (6, 5, 0)
object_point = np.zeros((6 * 7, 3), np.float32)
object_point[:,:2] = np.mgrid[0:7,0:6].T.reshape(-1, 2)

# Array to store 3D object points in real world space
object_points = []

# Array to store 2D frame points in image plane
frame_points = []

while(True):
    # Capture frame-by-frame
    return1, frame = capture.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Find the chess board corners
    return2, corners = cv2.findChessboardCorners(gray, (7, 6), None)

    # If found, add object points and image points after refining them
    if return2 == True:
        object_points.append(object_point)

        cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
        frame_points.append(corners)

        # Draw and display the corners
        cv2.drawChessboardCorners(frame, (7, 6), corners, return2)
        cv2.imshow('Camera Calibration', frame)
        cv2.waitKey(500)

        # Calibrate the camera
        return3, camera_matrix, distortion_coefficients, rotation_vectors, translation_vectors = cv2.calibrateCamera(object_points, frame_points, gray.shape[::-1], None, None)
    
# When everything is done, release the capture
capture.release()
cv2.destroyAllWindows()