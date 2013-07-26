import pywsock, simpleserver, json
from threadkill import *

class SensorDataServer(pywsock.PyWSock):	
	"""A WebSocket server that handles incoming data from a client
	(smartphone). Data is stored in sensorDataObject and an optional
	callback is fired every time new data is loaded."""
	
	def __init__(self, sensorDataObject, callback=lambda:None):
		self.object = sensorDataObject
		self.callback = callback
		
	def process(self, data):
		"""Processes incoming data and sets data in sensor class."""
		position = json.loads(data)["orientation"]
		precision = 2 # decimals
		
		# Right is positive
		self.object.lrTilt  = round(float(position["gamma"]), precision)
		# Forward is positive
		self.object.fbTilt = round(float(position["beta"]), precision)
		# Standard format (0 deg = North)
		self.object.heading = type(position["alpha"]) is float and int(round(float(position["alpha"]))) or 0
		
		# Fire callback on update
		self.callback()
		
		# Optional: depending on what you're doing, broadcast the response to other clients
		# via the WS server.
		# self.broadcast_resp(data)
		
class SensorData(object):
	"""Holds data and is updated by a SensorDataServer object."""
	def __init__(self):
		self.lrTilt = None
		self.fbTilt = None
		self.heading = None
		
	
class ServerLauncher(object):
	"""Wrapper class for server launcher."""
	def __init__(self, http=8888, ws=9876):
		self.HTTP_PORT = http
		self.WS_PORT = ws
		self.threads = []
		self.position = SensorData()
		
	def runServers(self):
		try: 
			self.ws = SensorDataServer( self.position, self.displayOrientationData )
			self.threads.append( Thread(target=self.ws.start_server, args=[self.WS_PORT]) )
			self.httpd = simpleserver.ControllerPageServer(port=self.HTTP_PORT	)
			self.threads.append( Thread(target=self.httpd.run) )
	
			for t in self.threads:
				t.start()
			print "Started HTTP server on port %s and WebSockets server on port %s." % (self.HTTP_PORT, self.WS_PORT)
		except SystemExit, KeyboardInterrupt:
			for t in self.threads:
				t.terminate()	
				
	def displayOrientationData(self):
		"""Reads data from self.position and prints to console. 
		Just an example, you could do many more creative things with this
		obviously."""
		
		lrDir = "left" if self.position.lrTilt < 0 else "right"
		fbDir = "front" if self.position.fbTilt > 0 else "back"
		
		parameters = (self.position.lrTilt, lrDir, self.position.fbTilt, fbDir, self.position.heading)
		string = "L-R tilt: %0.2f deg %s - F-B tilt: %0.2f deg %s - Compass: %0.0f deg" 
				
		print string % parameters
		
		
if __name__ == '__main__':
	ServerLauncher().runServers()
