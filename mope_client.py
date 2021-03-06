import sublime
import json
import webbrowser
import urllib.request as request

from .logger import *
from .http_utils import *

class MopeClient:
	def __init__(self):
		self.interface = ""
		self.port = 0
		self.connected = False

	def baseUrl(self):
		return "%s:%d/mope"%(self.interface, self.port)

	def projectUrl(self):
		return self.baseUrl()+"/project/"+str(self.projectId)

	def connect(self, interface, port, projectJson):
		log.debug("Client#connect called with %s %d %s" % (interface, port, projectJson))
		self.interface = "http://"+interface
		self.port = port
		self.connected = True
		sResp = json_request(self.baseUrl()+"/connect", projectJson)
		self.projectId = int(sResp.content)
		log.debug("proj id: "+str(self.projectId))

	def disconnect(self):
		if self.isConnected():
			self.connected = False
			requ = request.Request(self.projectUrl()+"/disconnect", method="POST")
			resp = request.urlopen(requ)
			log.info("disconnecting returned: {}".format(resp.getcode()))


	def isConnected(self):
		return self.connected

	def compile(self, file):
		if self.isConnected():
			jsData = json.dumps({"path": file})
			sResp = json_request(self.projectUrl()+"/compile", jsData)
			return sResp.content_as_map()

	def getCompletions(self, file, line, column, word):
		if self.isConnected():
			dataMap = {
				"file": file,
				"position": {
					"line": line,
					"column": column
				},
				"word": word
			}
			jsData = json.dumps(dataMap)
			log.debug("get completions for "+jsData)
			sResp = json_request(self.projectUrl()+"/completion", jsData)
			return sResp.content_as_map()

	def openDocumentation(self, model):
		if self.isConnected():
			uri = self.projectUrl()+"/doc?class=%s"%(model)
			log.info("documentation for "+model+" at "+uri)
			webbrowser.open(uri)

	def checkModel(self, file):
		if self.isConnected():
			jsData = json.dumps({"path": file})
			sResp = json_request(self.projectUrl()+"/checkModel", jsData)
			return sResp.content

	def sourceOf(self, file, line, column, word):
		if self.isConnected():
			dataMap = {
				"file": file,
				"position": {
					"line": line,
					"column": column
				},
				"word": word
			}
			jsData = json.dumps(dataMap)
			sResp = json_request(self.projectUrl()+"/declaration", jsData)
			return sResp.content_as_map()


	def typeOf(self, file, line, column, word):
		if self.isConnected():
			dataMap = {
				"file": file,
				"position": {
					"line": line,
					"column": column
				},
				"word": word
			}
			log.debug("src of "+str(dataMap))
			return json_request(self.projectUrl()+"/typeOf", json.dumps(dataMap)).content_as_map()