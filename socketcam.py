import sys
import socketio
import time
from threading import Thread
import random
from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2

THREAD = Thread()

class StreamThread(Thread):
    """Stream data on thread"""
    def __init__(self):
        self.delay = 1/15
        super(StreamThread, self).__init__()
        self.camera = PiCamera()
        self.camera.resolution = (640, 480)
        self.camera.framerate = 30
        self.rawCapture = PiRGBArray(self.camera, size=(640, 480))
        time.sleep(0.1)

    def get_data(self):
        for frame in self.camera.capture_continuous(self.rawCapture, format="bgr", use_video_port=True):
        	# grab the raw NumPy array representing the image, then initialize the timestamp
        	# and occupied/unoccupied text
        	image = frame.array

        	# show the frame
        	finalimage = cv2.imencode('.jpg', image)[1].tostring()
        	sio.emit("camImage",{"image":finalimage,"sensor":random.randint(0,100)},namespace="/cam")
	        #time.sleep(self.delay)
        	# clear the stream in preparation for the next frame
        	self.rawCapture.truncate(0)
    def run(self):
        """Default run method"""
        self.get_data()

sio = socketio.Client()

@sio.on('connect', namespace='/cam')
def test_connect():
	print("Connected")

@sio.on('move', namespace='/cam')
def ack(data):
    print(data)

if len(sys.argv) > 1:
    sio.connect(sys.argv[1])
else:
    sio.connect('http://10.0.33.235:8000/')

if not THREAD.isAlive():
	THREAD = StreamThread()
	THREAD.start()
