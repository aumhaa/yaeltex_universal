# by amounra 1125 : http://www.aumhaa.com
# version 2.3



import Live
import math

from ableton.v2.control_surface.elements.button import ButtonElement
from ableton.v2.control_surface.skin import Skin, SkinColorMissingError
# from .mono_bridge import MonoBridgeProxy
from .constants import *
from .debug import initialize_debug

LOCAL_DEBUG = False
debug = initialize_debug(local_debug= LOCAL_DEBUG)


class MonoButtonElement(ButtonElement):

	def __init__(self, name = 'MonoButton', script = None, color_map = None, monobridge = None, *a, **k):
		super(MonoButtonElement, self).__init__(name = name, *a, **k)


	def set_light(self, value):
		try:
			super(MonoButtonElement, self).set_light(value)
		except:
			debug('set_light exception for:', self._name if hasattr(self, '_name') else None, 'value:', value)



