import socketio
import time
from camera_pi import Camera
from threading import Thread
import random

THREAD = Thread()

class StreamThread(Thread):
    """Stream data on thread"""
    def __init__(self):
        self.delay = 1/30
        super(StreamThread, self).__init__()
        self.cam = Camera()
    def get_data(self):
        """
        Get data and emit to socket
        """
        while True:
            image = self.cam.get_frame()
            sio.emit("camImage",{"image":image,"sensor":random.randint(0,100)},namespace="/cam")
            time.sleep(self.delay)
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

sio.connect('http://localhost:8000/')

if not THREAD.isAlive():
	THREAD = StreamThread()
	THREAD.start()
