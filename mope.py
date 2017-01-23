# Main entry point for sublime plugin

import sublime
import sublime_plugin

import os.path as path

from .logger import *
from .mope_common import *
from .mope_client import *
from .concurrency import *

mopeProjectFile = "mope-project.json"
mopeClient = MopeClient()

def compileAndDisplayErrors(window):
	openFile = window.active_view().file_name()
	log.debug("opened file: "+openFile)
	compilerErrors = mopeClient.compile(openFile)
	infoPanelView = window.create_output_panel("mopeInfoPanel", True)
	infoPanelView.set_read_only(False)
	#edit the panel
	infoPanelView.run_command("mope_display_errors", {"errors": compilerErrors})
	infoPanelView.set_read_only(True)
	window.run_command("show_panel", {"panel": "output.mopeInfoPanel"})
	#self.window.run_command("hide_panel", {"panel": "output.mopeInfoPanel"})

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
			def fn():
				json = read_project_file(root, projectFile)
				log.info("json: "+json)
				try:
					mopeClient.connect(self.interface, self.port, json)
					sublime.message_dialog("Connected to %ss:%d"%(self.interface,self.port))
				except request.URLError:
					sublime.error_message("Couldn't connect to %s:%d!"%(self.interface, self.port))
			runc(fn)

class MopeDisconnectCommand(sublime_plugin.WindowCommand):
	def __init__(self, window):
		self.window = window

	def run(self):
		mopeClient.disconnect()
		sublime.message_dialog("MoPE Disconnected")

class MopeCompileProjectCommand(sublime_plugin.WindowCommand):
	def __init__(self, window):
		self.window = window

	def run(self):
		if isModelica():
			compileAndDisplayErrors(self.window)

class MopeDisplayErrorsCommand(sublime_plugin.TextCommand):
	def run(self, edit, errors):
		infoPanelView = self.view

		def toStringMapping(error):
			return "[{}] {} {}:{} - {}:{} {}".format(
				error["type"].capitalize(),
				error["file"],
				error["start"]["line"],
				error["start"]["column"],
				error["end"]["line"],
				error["end"]["column"],
				error["message"])

		errorLines = "\n".join(map(toStringMapping, errors))
		infoPanelView.insert(edit,0,errorLines)


class MopeEvListener(sublime_plugin.EventListener):
	def on_post_save_async(self, view):
		if isModelica():
			openFile = view.file_name()
			log.debug("saved the file: "+openFile)
			compileAndDisplayErrors(view.window())

	def mapSuggestions(self, suggestions):
		#log.debug("suggestions: "+str(suggestions))
		def mapping(suggestion):
			log.debug(suggestion)
			if suggestion["classComment"] is not None:
				return [suggestion["name"]+"\t"+suggestion["classComment"], suggestion["name"]]	
			else:
				return [suggestion["name"], suggestion["name"]]

		return [mapping(x) for x in suggestions]

	def on_query_completions(self, view, prefix, locations):
		#called when a completion is requested (Ctrl+Space)
		if isModelica():
			for point in locations:
				if view.match_selector(point, "source.modelica"):
					row, col = view.rowcol(point) #0-based cursor position
					subexpr = view.substr(view.expand_by_class(point, sublime.CLASS_WORD_START, " ")).strip()
					line = row+1
					column = col+1
					suggestions = mopeClient.getCompletions(currentFile(), line, column, subexpr)
					return self.mapSuggestions(suggestions)
		else:
			return None
	def on_window_command(self, window, cmdName,  args):
		# disconnect if user closes the window
		if cmdName == "close_window":
			mopeClient.disconnect()
			mopeExecutor.shutdown(False)


class MopeOpenDocumentationCommand(sublime_plugin.WindowCommand):
	def __init__(self, window):
		self.window = window

	def run(self):
		if isModelica():
			activeView = self.window.active_view()
			cursorRegion = activeView.sel()[0]
			wordRegion = activeView.word(cursorRegion)
			wordStr = activeView.substr(wordRegion)
			log.debug("found word "+wordStr)
			mopeClient.openDocumentation(wordStr)

class MopeCheckModelCommand(sublime_plugin.WindowCommand):
	def __init__(self, window):
		self.window = window

	def run(self):
		if isModelica():
			openedFile = currentFile()
			def fn():
				omcStr = mopeClient.checkModel(openedFile)
				sublime.message_dialog(omcStr)
			runc(fn)

class MopeShowTypeCommand(MopeCommon):
	def __init__(self, window):
		super(MopeCommon, self).__init__(window)
		pass

	def run(self):
		print("WARNING show type not implemented!")