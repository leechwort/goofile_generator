import cv2
import numpy as np
from glob import glob
from time import sleep
import correction_calculation

devices = glob("/dev/v4l/by-path/pci-0000:00:14.0-usb-*index0")
print(devices)

"""
frame_0 - top left
"""

CAMERA_FRAMES_DIR = '/home/artsin/Dev/goofile_generator/camera_frames/'

while True:
    frames = [None, None, None, None]
    for device in devices:
        camera = cv2.VideoCapture(device)
        camera.set(cv2.CAP_PROP_EXPOSURE, 40) 
        _, frame = camera.read()
        #if frame is not None:
        #    print("Cannot get data from camera", camera)
        #    break
    
        # Sort frames depending on USB path
        if ('1.3' in device):
            frames[0] = frame
        elif ('1.4' in device):
            frames[1] = frame
        elif ('1.5' in device):
            frames[2] = frame
        elif ('1.6' in device):
            frames[3] = frame
    combined_frames = np.vstack((np.hstack((frames[0], frames[1])), np.hstack((frames[2], frames[3]))))
    

    cv2.imshow("Result", combined_frames)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.imwrite(CAMERA_FRAMES_DIR + 'frame_0.jpg', frames[0]) 
        cv2.imwrite(CAMERA_FRAMES_DIR + 'frame_1.jpg', frames[1]) 
        cv2.imwrite(CAMERA_FRAMES_DIR + 'frame_2.jpg', frames[2]) 
        cv2.imwrite(CAMERA_FRAMES_DIR + 'frame_3.jpg', frames[3]) 
        break

cv2.destroyAllWindows()

correction_calculation.run()

