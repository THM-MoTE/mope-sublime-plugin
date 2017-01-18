# Main entry point for sublime plugin

import sublime
import sublime_plugin

from .mope_common import *

class MopeConnectCommand(MopeCommon):
	def __init__(self, window):
		super(MopeCommon, self).__init__(window)

	def run(self):
		print("NOT IMPLEMENTED: Connecting to %s:%d" % (super(MopeCommon, self).get_interface(), super(MopeCommon, self).get_port()))

class MopeCompileProjectommand(MopeCommon):
	def __init__(self, window):
		super(MopeCommon, self).__init__(window)
		pass

	def run(self):
		print("WARNING compile project not implemented!")

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