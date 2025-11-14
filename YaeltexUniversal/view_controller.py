# by amounra 1125 : http://www.aumhaa.com
# version 2.3


import Live
import math
import logging
# from re import *

from ableton.v2.base import listens
from ableton.v2.control_surface.components.scroll import ScrollComponent
from ableton.v2.control_surface.components.view_control import BasicSceneScroller, ViewControlComponent
from .device_navigator import *

from .debug import initialize_debug

LOCAL_DEBUG = False
debug = initialize_debug(local_debug = LOCAL_DEBUG)


class SpecialViewControlComponent(ViewControlComponent):


	def __init__(self, *a, **k):
		super(SpecialViewControlComponent, self).__init__(*a, **k)
		self._basic_scroll_scenes = ScrollComponent(BasicSceneScroller())
		self.register_slot(self.song, self._basic_scroll_scenes.update, 'scenes')
		self.register_slot(self.song.view, self._basic_scroll_scenes.update, 'selected_scene')


	def set_scene_select_dial(self, dial):
		self._on_scene_select_dial_value.subject = dial


	@listens('value')
	def _on_scene_select_dial_value(self, value):
		debug('_on_scene_select_dial_value', value)
		self._basic_scroll_scenes.scroll_up() if value < 65 else self._basic_scroll_scenes.scroll_down()


	def set_track_select_dial(self, dial):
		self._on_track_select_dial_value.subject = dial


	@listens('value')
	def _on_track_select_dial_value(self, value):
		debug('_on_scene_select_dial_value', value)
		self._scroll_tracks.scroll_up() if value < 65 else self._scroll_tracks.scroll_down()
