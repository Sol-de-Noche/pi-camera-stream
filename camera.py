# Modified by smartbuilds.io
# Date: 27.09.20
# Desc: This scrtipt script..

import cv2
from imutils.video import VideoStream
import imutils
import time
import numpy as np


class VideoCamera(object):
    def __init__(self, flip=False):
        source = None
        for camera_idx in range(20):
            cap = cv2.VideoCapture(camera_idx)
            if cap.isOpened():
                if(camera_idx != 0):
                    print(f'Camera index available: {camera_idx}')
                    source = camera_idx
                cap.release()

        if(source != None):
            self.vs = VideoStream(source).start()
        self.flip = flip
        time.sleep(2.0)

    def __del__(self):
        self.vs.stop()

    def flip_if_needed(self, frame):
        if self.flip:
            return np.flip(frame, 0)
        return frame

    def get_frame(self):
        frame = self.flip_if_needed(self.vs.read())
        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()
