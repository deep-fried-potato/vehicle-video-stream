import sys
import socketio
import time
from threading import *
import random
from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2
import RPi.GPIO as GPIO
import time
import queue

servoPIN = 17
motorPIN = 14
vrPIN = 4
GPIO.setmode(GPIO.BCM)

GPIO.setup(servoPIN, GPIO.OUT)
GPIO.setup(motorPIN, GPIO.OUT)
GPIO.setup(vrPIN, GPIO.OUT)

p = GPIO.PWM(servoPIN, 50) # GPIO 17 for PWM with 50Hz
pp = GPIO.PWM(vrPIN, 50)
pp.start(7.5)

THREAD = Thread()
q = queue.Queue()
vrr = queue.Queue()

class StreamThread(Thread):
    """Stream data on thread"""
    def __init__(self):
        self.delay = 1/15
        super(StreamThread, self).__init__()
        self.camera = PiCamera()
        self.camera.resolution = (360, 180)
        self.camera.framerate = 10
        self.rawCapture = PiRGBArray(self.camera, size=(360, 180))
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

def orient():
    while True:
        orin = vrr.get()
        pp.ChangeDutyCycle(orin)

def rotate():
    print('rotate')
    p.start(7.5) # Initialization
    try:
        while True:
            angle = q.get()
            print(angle)
            if float(angle) == 13:
                GPIO.output(motorPIN,1)
                continue
            elif float(angle) == 14:
                GPIO.output(motorPIN,0)
                continue

            p.ChangeDutyCycle(float(angle))
            time.sleep(1)
    except KeyboardInterrupt:
        p.stop()

@sio.on('vr_orient', namespace='/cam')
def VRorient(data):
    data = data['Orientation']
 #   data = data
    vrr.put(data)

@sio.on('move', namespace='/cam')
def ack(data):
    print(data['direction'])
    if data['direction'] == 'Left':
        q.put(4)
    elif data['direction'] =='Right':
        q.put(9)
    elif data['direction'] == 'Straight':
        q.put(7.5)
    elif data['direction'] =='Forward':
        q.put(13)
    else:
        q.put(14)
if len(sys.argv) > 1:
    sio.connect('http://' + sys.argv[1] + ':8000/')
else:
    sio.connect('http://10.0.33.235:8000/')

if not THREAD.isAlive():
        THREAD = StreamThread()
        THREAD.daemon = True
        THREAD.start()

t1 = Thread(target=rotate)
t1.deamon = True
t1.start()

t2 = Thread(target=orient)
t2.deamon = True
t2.start()
