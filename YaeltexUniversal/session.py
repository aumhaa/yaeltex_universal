# by amounra 1125 : http://www.aumhaa.com
# version 2.3


import Live
import math
import logging
# from re import *

from ableton.v2.control_surface.components import SessionComponent
from ableton.v2.control_surface.control import ButtonControl

from .Map import *
from .debug import initialize_debug

LOCAL_DEBUG = False
debug = initialize_debug(local_debug = LOCAL_DEBUG)




class SpecialSessionComponent(SessionComponent):
	selected_clip_launch_button = ButtonControl(color = "Session.SelectedClipLaunch")
	selected_scene_launch_button = ButtonControl(color = "Session.SelectedSceneLaunch")

	def set_scene_launch_buttons(self, buttons):
		assert(not buttons or buttons.width() == self._session_ring.num_scenes and buttons.height() == 1)
		if buttons:
			for button, (x, _) in buttons.iterbuttons():
				scene = self.scene(x)
				#debug('setting scene launch for button:', button, 'scene:', scene)
				scene.set_launch_button(button)

		else:
			for x in range(self._session_ring.num_scenes):
				scene = self.scene(x)
				scene.set_launch_button(None)

	@selected_clip_launch_button.pressed
	def selected_clip_launch_button(self, *a, **k):
		self.song.view.highlighted_clip_slot.fire()

	@selected_scene_launch_button.pressed
	def selected_clip_launch_button(self, *a, **k):
		self.song.view.selected_scene.fire()