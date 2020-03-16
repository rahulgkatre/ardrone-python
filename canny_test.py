import time, sys
import numpy as np
import cv2
import ps_drone

def auto_canny(frame, delta = 0.33):
    # Compute the median of the single channel pixel intensities
    intensity = np.median(frame)
    
    # Apply automatic Canny edge detection using the computed median
    lower = int(max(0, (1.0 - delta) * intensity))
    upper = int(max(255, (1.0 + delta) * intensity))
    edged = cv2.Canny(frame, lower, upper)

    # Return the edged image
    return edged

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

while(True):
    # Capture frame-by-frame
    return1, frame = capture.read()

    # Prepare the image for edge detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (3, 3), 0)

    # Apply Canny edge detection with auto threshold
    edged = auto_canny(blurred)
    manual = cv2.Canny(blurred, -255, 255)

    # Display the two frames
    cv2.imshow('Original Frame', frame)
    cv2.imshow('Manual Canny Edge', manual)
    cv2.imshow('Canny Edge Detection', edged)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
# When everything is done, release the capture
capture.release()
cv2.destroyAllWindows()