from Tkinter import *
import example_accel as accel
import simpleserver, cmath, math
from threading import Thread

class TiltDemo(object):
	def __init__(self, http=8888, ws=9876):
		## Server ##
		self.HTTP_PORT = http
		self.WS_PORT = ws
		self.threads = []
		self.sensorData = accel.SensorData()
		self.buffer = []
		
		## Tkinter ##
		self.canvas = Canvas(width=200, height=200)
		self.canvas.pack()
		
		# a square
		self.xy = [(50, 50), (150, 50), (150, 150), (50, 150)]
		self.polygon_item = self.canvas.create_polygon(self.xy)
		self.center = 100, 100
		self.start = None
		
	def runServers(self):
		try: 
			self.ws = accel.SensorDataServer( self.sensorData, callback=self.update )
			self.threads.append( Thread(target=self.ws.start_server, args=[self.WS_PORT]) )
			
			self.httpd = simpleserver.ControllerPageServer(port=self.HTTP_PORT	)
			self.threads.append( Thread(target=self.httpd.run) )

			for t in self.threads:
				t.start()
			print "Started HTTP server on port %s and WebSockets server on port %s." % (self.HTTP_PORT, self.WS_PORT)
		except SystemExit, KeyboardInterrupt:
			for t in self.threads:
				t.terminate()			
				
	def update(self):
		angle = self.sensorData.heading * (math.pi/180)  #radians
		cAngle = cmath.exp(angle*-1j) # data I'm getting is backwards
		
		center = complex(self.center[0], self.center[1])
		newXY = []
		for x, y in self.xy:
			vector = cAngle * ( complex(x, y) - center ) + center
			newXY.append(vector.real)
			newXY.append(vector.imag)
		self.canvas.coords(self.polygon_item, *newXY)


	def run(self):
		self.runServers()
		print "Starting GUI"
		mainloop()
		
TiltDemo().run()