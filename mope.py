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
		openedFolders = self.window.folders()
		if len(openedFolders) != 1:
			sublime.error_message("Can't handle multiple project roots! Please open only 1 directory")
		else:
			root = openedFolders[0]
			projectFile = path.join(root, mopeProjectFile)
			json = read_project_file(root, projectFile)
			info("json: "+json)
			try:
				mopeClient.connect(self.interface, self.port, json)
				sublime.message_dialog("Connected to %ss:%d"%(self.interface,self.port))
			except request.URLError:
				sublime.error_message("Couldn't connect to %s:%d!"%(self.interface, self.port))


class MopeCompileProjectCommand(sublime_plugin.WindowCommand):
	def __init__(self, window):
		self.window = window

	def run(self):
		print("WARNING compile project not implemented!")
		openFile = self.window.active_view().file_name()
		debug("opened file: "+openFile)
		mopeClient.compile(openFile)
		infoPanelView = self.window.create_output_panel("mopeInfoPanel", True)
		infoPanelView.set_read_only(False)
		#edit the panel
		infoPanelView.run_command("mope_update_info_panel", {"dataMap": {}})
		infoPanelView.set_read_only(True)
		self.window.run_command("show_panel", {"panel": "output.mopeInfoPanel"})
		#self.window.run_command("hide_panel", {"panel": "output.mopeInfoPanel"})

class MopeUpdateInfoPanelCommand(sublime_plugin.TextCommand):
	def run(self, edit, dataMap):
		infoPanelView = self.view
		#self.view.window().message_dialog("upd")
		infoPanelView.insert(edit, 0, "this is a test")


class MopeEvListener(sublime_plugin.EventListener):
	def on_post_save_async(self, view):
		#TODO check if it's a modelica file/restrict execution to Modelica scope
		openFile = view.file_name()
		debug("saved the file: "+openFile)
		mopeClient.compile(openFile)

	def on_query_completions(self, view, prefix, locations):
		#called when a completion is requested (Ctrl+Space)
		return [
			["Modelica\tThe std lib", "Modelica"],
			["Electrical\tThe electrical lib", "Modelica"]
		]

class MopeOpenDocumentationCommand(sublime_plugin.WindowCommand):
	def __init__(self, window):
		self.window = window

	def run(self):
		print("WARNING open documentation not implemented!")
		activeView = self.window.active_view()
		cursorRegion = activeView.sel()[0]
		#debug("cursor is at: "+str(cursorPos))
		wordRegion = activeView.word(cursorRegion)
		wordStr = activeView.substr(wordRegion)
		debug("found word "+wordStr)
		mopeClient.openDocumentation(wordStr)

class MopeShowTypeCommand(MopeCommon):
	def __init__(self, window):
		super(MopeCommon, self).__init__(window)
		pass

	def run(self):
		print("WARNING show type not implemented!")