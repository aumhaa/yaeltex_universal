# by amounra 1125 : http://www.aumhaa.com
# version 2.3


from ableton.v2.control_surface.components import TransportComponent
from ableton.v2.control_surface.control import ButtonControl
from .debug import initialize_debug

LOCAL_DEBUG = False
debug = initialize_debug(local_debug = LOCAL_DEBUG)

class SpecialTransportComponent(TransportComponent):

	new_tap_tempo_button = ButtonControl()

	# def _update_stop_button_color(self):
	# 	self._stop_button.color = 'Transport.StopOn' if self._play_toggle.is_toggled else 'Transport.StopOff'

	@new_tap_tempo_button.pressed
	def tap_tempo_button(self, button):
		debug('tap_tempo')
		self.song.tap_tempo()
