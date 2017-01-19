# Main entry point for sublime plugin

import sublime
import sublime_plugin

import os.path as path

from .logging import *
from .mope_common import *
from .mope_client import *

mopeProjectFile = "mope-project.json"
mopeClient = MopeClient()

class MopeConnectCommand(sublime_plugin.WindowCommand):
	def __init__(self, window):
		self.window = window
		self.settings = sublime.load_settings("Mope.sublime-settings")
		self.interface = self.settings.get("interface")
		self.port = self.settings.get("port")

	def run(self):
		print("NOT IMPLEMENTED: Connecting to %s:%d" % (self.interface, self.port))
		openedFolders = self.window.folders()
		if len(openedFolders) != 1:
			sublime.error_message("Can't handle multiple project roots! Please open only 1 directory")
		else:
			root = openedFolders[0]
			projectFile = path.join(root, mopeProjectFile)
			json = read_project_file(root, projectFile)
			info("json: "+json)
			mopeClient.connect(self.interface, self.port, json)

class MopeCompileProjectCommand(sublime_plugin.WindowCommand):
	def __init__(self, window):
		self.window = window

	def run(self):
		print("WARNING compile project not implemented!")
		openFile = self.window.active_view().file_name()
		debug("opened file: "+openFile)
		mopeClient.compile(openFile)

class MopeEvListener(sublime_plugin.EventListener):
	def on_post_save_async(self, view):
		openFile = view.file_name()
		debug("saved the file: "+openFile)
		mopeClient.compile(openFile)

class MopeOpenDocumentationCommand(MopeCommon):
	def __init__(self, window):
		super(MopeCommon, self).__init__(window)
		pass

	def run(self):
		print("WARNING open documentation not implemented!")

class MopeShowTypeCommand(MopeCommon):
	def __init__(self, window):
		super(MopeCommon, self).__init__(window)
		pass

	def run(self):
		print("WARNING show type not implemented!")