# by amounra 1125 : http://www.aumhaa.com
# version 2.3

import Live
import logging

# from re import *

logger = logging.getLogger(__name__)

def log_flattened_arguments(*a, **k):
	args = ''
	for item in a:
		args = args + str(item) + ' '
	logger.info(args)


def nop(*a, **k):
	pass


def initialize_debug(local_debug = False):
	return log_flattened_arguments if local_debug else nop









