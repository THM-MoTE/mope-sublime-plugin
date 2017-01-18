from .logging import *

class MopeClient:
	def __init__(self):
		self.interface = ""
		self.port = 0
		self.connected = False

	def connect(self, interface, port, projectJson):
		debug("Client#connect called with %s %d %s" % (interface, port, projectJson))
		self.interface = interface
		self.port = port
		self.connected = True
	
	def disconnect(self):
		self.connected = False

	def isConnected(self):
		return self.connected