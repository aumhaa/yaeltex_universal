# by amounra 1125 : http://www.aumhaa.com
# version 2.3


import Live
import math
import logging
# from re import *

from ableton.v2.base import listens
from ableton.v2.control_surface.components import SessionNavigationComponent

from .Map import *
from .debug import initialize_debug

LOCAL_DEBUG = False
debug = initialize_debug(local_debug = LOCAL_DEBUG)



class SpecialSessionNavigationComponent(SessionNavigationComponent):


	def set_track_select_dial(self, dial):
		self._on_track_select_dial_value.subject = dial


	@listens('value')
	def _on_track_select_dial_value(self, value):
		#debug('_on_track_select_dial_value:', value)
		#self._can_bank_left() and self._bank_left() if value == 127 else self._can_bank_right() and self._bank_right()
		self._horizontal_banking.can_scroll_up() and self._horizontal_banking.scroll_up() if value == 127 else self._horizontal_banking.can_scroll_down() and self._horizontal_banking.scroll_down()

	def set_scene_bank_nav_dial(self, dial):
		self._on_scene_bank_nav_dial_value.subject = dial

	@listens('value')
	def _on_scene_bank_nav_dial_value(self, value):
		debug('_on_scene_bank_nav_dial_value', value)
		self._vertical_banking.can_scroll_up() and self._vertical_banking.scroll_up() if value < 65 else self._vertical_banking.can_scroll_down() and self._vertical_banking.scroll_down()


	def set_track_bank_nav_dial(self, dial):
		self._on_track_bank_nav_dial_value.subject = dial


	@listens('value')
	def _on_track_bank_nav_dial_value(self, value):
		debug('_on_scene_bank_nav_dial_value', value)
		self._horizontal_banking.can_scroll_up() and self._horizontal_banking.scroll_up() if value < 65 else self._horizontal_banking.can_scroll_down() and self._horizontal_banking.scroll_down()
