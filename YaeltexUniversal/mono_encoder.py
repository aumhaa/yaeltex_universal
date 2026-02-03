# by amounra 1125 : http://www.aumhaa.com
# version 2.3

import Live

from ableton.v2.control_surface.elements.encoder import EncoderElement

from .constants import *
from .debug import initialize_debug

LOCAL_DEBUG = False
debug = initialize_debug(local_debug = LOCAL_DEBUG)


class MonoEncoderElement(EncoderElement):

	def __init__(self, name = 'MonoEncoder', num = 0, script = None, mapping_feedback_delay = 1, monobridge = None, *a, **k):
		super(MonoEncoderElement, self).__init__(map_mode=Live.MidiMap.MapMode.absolute, *a, **k)









