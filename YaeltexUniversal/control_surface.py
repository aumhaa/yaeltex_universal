# by amounra 1125 : http://www.aumhaa.com
# version 2.3


import Live
import math
import sys

import logging
logger = logging.getLogger(__name__)

from ableton.v2.control_surface import midi
from ableton.v2.control_surface.profile import profile
from ableton.v2.control_surface.control_surface import *
from ableton.v2.control_surface.input_control_element import InputControlElement, MIDI_CC_TYPE, MIDI_NOTE_TYPE, MIDI_PB_TYPE, MIDI_SYSEX_TYPE

from .utilities import YaeltexSettings
from .debug import initialize_debug

LOCAL_DEBUG = False
debug = initialize_debug(local_debug = LOCAL_DEBUG)

QUERY_INTERVAL = 10

class YaeltexControlSurface(ControlSurface):

	_color_type = 'YAEL'
	_connected = False
	_sysex_id = 0
	_model_name = 'Yaeltex Control Surface'
	_version_check = 'Mod_Disabled'

	def __init__(self, *a, **k):
		self.log_message = logger.info
		super(YaeltexControlSurface, self).__init__(*a, **k)
		with self.component_guard():
			self._yaeltex_settings = YaeltexSettings(model = self._sysex_id, control_surface = self)
		self.schedule_message(1, self._open_log)
		#self._connection_routine = self._tasks.add(task.sequence(task.wait(10), task.run(self._check_connection)))
		#self._connection_routine.restart()
		self.schedule_message(2, self._check_connection)


	def _open_log(self):
		self.log_message("<<<<<<<<<<<<<<<<<<<<= " + str(self._model_name) + " " + str(self._version_check) + " log opened =>>>>>>>>>>>>>>>>>>>")
		self.show_message(str(self._model_name) + ' Control Surface Loaded')


	def _close_log(self):
		self.log_message("<<<<<<<<<<<<<<<<<<<<= " + str(self._model_name) + " " + str(self._version_check) + " log closed =>>>>>>>>>>>>>>>>>>>")



	def port_settings_changed(self):
		debug('port settings changed!')
		self._connected = False
		self.schedule_message(QUERY_INTERVAL, self._check_connection)


	def _check_connection(self):
		if not self._connected:
			debug(self._model_name, '_check_connection')
			self._yaeltex_settings.query_surface()
			#self._connection_routine.restart()
			self.schedule_message(QUERY_INTERVAL, self._check_connection)


	def _initialize_hardware(self):
		debug(self._model_name, 'initialize_hardware()')


	def _initialize_script(self):
		self.refresh_state()
		debug(self._model_name, 'initialize_script()')


	# def set_appointed_device(self, device):
	# 	self.song.appointed_device = device


	def process_midi_bytes(self, midi_bytes, midi_processor):
		if midi.is_sysex(midi_bytes):
			try:
				self.handle_sysex(midi_bytes)
			except:
				pass
		super(YaeltexControlSurface, self).process_midi_bytes(midi_bytes, midi_processor)


	def handle_sysex(self, midi_bytes):
		debug('sysex: ', str(midi_bytes))
		#debug('matching:', midi_bytes[3:11], 'to', tuple([6, 2, 0, 1, 97, 1, 0]  + [self._sysex_id]))
		# if midi_bytes[3:11] == tuple([6, 2, 0, 1, 97, 1, 0]  + [self._sysex_id]):
		if midi_bytes[1:8] == tuple([121, 116, 120, 1, 1, 4, 1]):
			if not self._connected:
				debug('connecting from sysex...')
				#self._connection_routine.kill()
				self._connected = True
				#self._livid_settings.set_model(midi_bytes[11])
				self._initialize_hardware()
				self._initialize_script()


	def disconnect(self):
		super(YaeltexControlSurface, self).disconnect()
		self._close_log()
