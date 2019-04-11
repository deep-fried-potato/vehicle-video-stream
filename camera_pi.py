from time import time
import numpy as np
import picamera
import cv2
import io

class Camera(object):
    def __init__(self):
        # cv2.VideoCapture.set(cv2.CV_CAP_PROP_FRAME_WIDTH,300)
        # cv2.VideoCapture.set(cv2.CV_CAP_PROP_FRAME_HEIGHT,300)
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 300)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 300)
        # self.cap.set(cv2.CV_CAP_PROP_FRAME_WIDTH,300)
        # self.cap.set(cv2.CV_CAP_PROP_FRAME_HEIGHT,300)

    def get_frame(self):
        ret, frame = self.cap.read()
        return cv2.imencode('.jpg', frame)[1].tostring()
