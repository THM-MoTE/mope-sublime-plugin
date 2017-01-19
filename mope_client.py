import json

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

	def compile(self, file):
		if self.isConnected():
			jsData = json.dumps({"path": file})
			info("compiling with "+jsData)

	def openDocumentation(self, model):
		#TODO add project uri
		if self.isConnected():
			uri = "/doc?class=%s"%(model)
			info("documentation for "+model+" at "+uri)