from flask import Flask, render_template, Response
from flask_socketio import SocketIO,emit
from camera_pi import Camera
import time
from time import sleep
from threading import Thread
app = Flask(__name__)
socketio = SocketIO(app)

THREAD = Thread()

class CountThread(Thread):
	"""Stream data on thread"""
	def __init__(self):
		self.delay = 1/30
		super(CountThread, self).__init__()
		self.cam = Camera()
	def get_data(self):
		"""
		Get data and emit to socket
		"""
		while True:
			image = self.cam.get_frame()
			socketio.emit('imageSend', {'buffer':image},namespace="/client")
			sleep(self.delay)
	def run(self):
		"""Default run method"""
		self.get_data()



@app.route("/")
def index():
	timeNow = time.asctime( time.localtime(time.time()) )
	temp, hum = 69,69
	templateData = {
      'time': timeNow,
      'temp': temp,
      'hum'	: hum
	}
	return render_template('index.html', **templateData)

@app.route('/camera')
def cam():
	"""Video streaming home page."""
	timeNow = time.asctime( time.localtime(time.time()) )
	templateData = {
      'time': timeNow
	}
	return render_template('camera.html', **templateData)
@app.route("/vr")
def vr():
	'''Virtual Reality'''
	return render_template('vr.html')
@app.route("/control")
def control():
	'''Only Control'''
	return render_template('control.html')
@socketio.on("move",namespace="/client")
def relayMove(data):
	socketio.emit("move",data,namespace="/cam")

@socketio.on("vr_orient",namespace="/client")
def relayVRorient(data):
	socketio.emit("vr_orient",data,namespace="/cam")

@socketio.on("camImage",namespace="/cam")
def relayImage(data):
	socketio.emit("image2Client",data,namespace="/client")

if __name__ == '__main__':
    socketio.run(app,host='0.0.0.0', port =8000, debug=True)
