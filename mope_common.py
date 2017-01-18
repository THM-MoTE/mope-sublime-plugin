# Commons for all Sublime commands

import sublime
import sublime_plugin

class MopeCommon(sublime_plugin.WindowCommand):
		def __init__(self, window):
			self.settings = sublime.load_settings("Mope.sublime-settings")
			self.interface = self.settings.get("interface")
			self.port = self.settings.get("port")
			print("common instantiated with %s:%d" % (self.interface, self.port))

		def get_interface(self):
			return self.interface

		def get_port(self):
			return self.port