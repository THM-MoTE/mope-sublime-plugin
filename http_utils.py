import json
import urllib.request as request

class SimpleRequest():
	def __init__(self, code, body):
		self.statusCode = code
		self.content = body

	def content_as_map(self):
		return json.loads(self.content)

def json_request(url, json):
	requ = request.Request(url, data=json.encode(), headers={"Content-Type": "application/json"}, method="POST")
	resp = request.urlopen(requ)
	return SimpleRequest(resp.getcode(), resp.read().decode())

def decode_json_response(response):
	string = response.read().decode()
	return json.loads(string)