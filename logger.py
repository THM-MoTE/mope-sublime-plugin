import logging

def initLogger():
	import sys
	logger = logging.getLogger("mope")
	formatter = logging.Formatter("[MoPE] %(asctime)s [%(levelname)-5.5s]  %(message)s")
	logger.handlers.clear()

	streamHandler = logging.StreamHandler(sys.stdout)
	streamHandler.setFormatter(formatter)
	logger.addHandler(streamHandler)
	logger.setLevel(logging.DEBUG)
	logger.info("Logger initialized")
	return logger

log = initLogger()
