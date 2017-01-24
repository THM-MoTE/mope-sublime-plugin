# Commons for all Sublime commands

import sublime
import sublime_plugin

import os.path as path
import json

from .logger import *

def read_project_file(rootDir, projectFile):
	if path.exists(projectFile):
		#read file and convert into map/json object
		log.debug("project file exists")
		with open(projectFile, "r") as file:
			return file.read()
	else:
		#create file with project informations
		log.warn("project file doesn't exist")
		with open(projectFile, "w") as file:
			data = { "path": rootDir, "outputDirectory": "target" }
			jsonStr = json.dumps(data, indent=2)
			file.write(jsonStr)
			return jsonStr

def isModelica():
	openedFile = currentFile()
	return openedFile.endswith(".mo")

def currentFile():
	return sublime.active_window().active_view().file_name()

def fullWordBelowCursor(view, pos=None):
	cursorPos = pos if pos is not None else view.sel()[0]
	expandedRegion = view.expand_by_class(cursorPos, sublime.CLASS_WORD_START, " ")
	return view.substr(expandedRegion).strip()