import SimpleHTTPServer, SocketServer, atexit

class ControllerPageServer(object):
	"""Very simple wrapper class for an HTTP server."""
	handler = SimpleHTTPServer.SimpleHTTPRequestHandler
	
	def __init__(self, port, host=""):
		self.port = port
		self.host = host
		self.http = SocketServer.TCPServer((self.host, self.port), self.handler)
		self.running = False
		
	def run(self):
		self.running = True 
		while self.running:
			self.http.handle_request()
	
		