# by amounra 1120 : http://www.aumhaa.com
# written against Live 11.0b29 on 021521


import Live
import math
import sys
import logging
from re import *
from itertools import chain, starmap

from ableton.v2.base import inject, listens, listens_group, nop
from ableton.v2.control_surface import ControlSurface, ControlElement, Layer, Skin, PrioritizedResource, Component, ClipCreator, DeviceBankRegistry
from ableton.v2.control_surface.elements import EncoderElement, ComboElement, ButtonMatrixElement, DoublePressElement, MultiElement, DisplayDataSource, SysexElement
from ableton.v2.control_surface.components import ClipSlotComponent, SceneComponent, SessionComponent, TransportComponent, BackgroundComponent, ViewControlComponent, SessionRingComponent, SessionRecordingComponent, SessionNavigationComponent, MixerComponent, PlayableComponent
from ableton.v2.control_surface.components.mixer import SimpleTrackAssigner
from ableton.v2.control_surface.control import control_color
from ableton.v2.control_surface.mode import AddLayerMode, ModesComponent, DelayMode
from ableton.v2.control_surface.elements.physical_display import PhysicalDisplayElement
from ableton.v2.control_surface.components.session_recording import *
from ableton.v2.control_surface.control import PlayableControl, ButtonControl, control_matrix
from ableton.v2.control_surface.components.scroll import ScrollComponent
from ableton.v2.control_surface.components.view_control import BasicSceneScroller

from .Map import *
from .colors import *
from .mono_encoder import MonoEncoderElement
from .mono_mixer import MonoMixerComponent, MonoChannelStripComponent
from .device import DeviceComponent
from .mono_button import *
from .mono_encoder import MonoEncoderElement
from .device_navigator import *
from .debug import initialize_debug
logger = logging.getLogger(__name__)
debug = initialize_debug()

# DEBUG = False
# try:
# 	from aumhaa.v2.base import initialize_debug
# except:
# 	def log_flattened_arguments(*a, **k):
# 		args = ''
# 		for item in a:
# 			args = args + str(item) + ' '
# 		logger.info(args)
# 	def initialize_debug():
# 		return log_flattened_arguments if DEBUG else no_debug


MIDI_NOTE_TYPE = 0
MIDI_CC_TYPE = 1
MIDI_PB_TYPE = 2
MIDI_MSG_TYPES = (MIDI_NOTE_TYPE, MIDI_CC_TYPE, MIDI_PB_TYPE)
MIDI_NOTE_ON_STATUS = 144
MIDI_NOTE_OFF_STATUS = 128
MIDI_CC_STATUS = 176
MIDI_PB_STATUS = 224


def is_device(device):
	return (not device is None and isinstance(device, Live.Device.Device) and hasattr(device, 'name'))


def make_pad_translations(chan):
	return tuple((x%4, int(x/4), x+16, chan) for x in range(16))


def return_empty():
	return []

if initialize_debug:
	debug = initialize_debug()


class LinkedSessionInstances(object):
	# _active_instances = []
	# _linked_session_instances = []
	# _minimal_track_offset = -1
	# _minimal_scene_offset = -1
	def __init__(self):
		self._active_instances = []
		self._linked_session_instances = []
		self._minimal_track_offset = -1
		self._minimal_scene_offset = -1



def get_yt_linked_session_ring_instances():
	# debug('BUILTINS access....')
	if isinstance(__builtins__, dict):
		if not 'yt_linked_session_ring_instances' in list(__builtins__.keys()) or not hasattr(__builtins__['yt_linked_session_ring_instances'], '_active_instances'):
			__builtins__['yt_linked_session_ring_instances'] = LinkedSessionInstances()
	else:
		if not hasattr(__builtins__, 'yt_linked_session_ring_instances') or not hasattr(__builtins__['yt_linked_session_ring_instances'], '_active_instances'):
			setattr(__builtins__, 'yt_linked_session_ring_instances', LinkedSessionInstances())
	return __builtins__['yt_linked_session_ring_instances']


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


class SpecialSessionRingComponent(SessionRingComponent):

	_linked_session_ring = None
	_linked_session_instances = []
	_minimal_track_offset = -1
	_minimal_scene_offset = -1

	# @listens('track_offset')
	# def _on_linked_track_offset_changed(self, track_offset):
	# 	self.track_offset = track_offset
	#
	# @listens('scene_offset')
	# def _on_linked_scene_offset_changed(self, scene_offset):
	# 	self.scene_offset = scene_offset

	def __init__(self, script, *a, **k):
		self._script = script
		# self.__is_linked = False
		super(SpecialSessionRingComponent, self).__init__(*a, **k)

	# def _is_linked(self):
	# 	return self.__is_linked

	@listens('offset')
	def _on_linked_offset_changed(self, track_offset, scene_offset):
		debug('new linked offset:', track_offset, scene_offset)
		self.set_offsets(track_offset, scene_offset)

	# def set_linked_session_ring(self, session_ring):
	# 	self._linked_session_ring = session_ring
	# 	# self._on_linked_track_offset_changed.subject = self._linked_session_ring
	# 	# self._on_linked_scene_offset_changed.subject = self._linked_session_ring
	# 	self._on_linked_offset_changed.subject = self._linked_session_ring

	def _globalInstances(self):
		return get_yt_linked_session_ring_instances()


	def link_with_track_offset(self, track_offset):
		if self._is_linked():
			self._unlink()
		self.set_offsets(track_offset, self.scene_offset)
		self._link()

	def unlink(self):
		if self._is_linked():
			self._unlink()

	def _is_linked(self):
		# return self in SpecialSessionRingComponent._linked_session_instances
		return self in self._globalInstances()._linked_session_instances

	def _link(self):
		# SpecialSessionRingComponent._linked_session_instances.append(self)
		self._globalInstances()._linked_session_instances.append(self)

	def _unlink(self):
		# SpecialSessionRingComponent._linked_session_instances.remove(self)
		self._globalInstances()._linked_session_instances.remove(self)

	# def set_offsets(self, track_offset, scene_offset):
	# 	debug('set_offsets', track_offset, scene_offset)
	# 	if self._is_linked():
	# 		debug('sending to linked delegation...')
	# 		self._perform_offset_change(track_offset - self._track_offset, scene_offset - self._scene_offset)
	# 	else:
	# 		super(SpecialSessionRingComponent, self).set_offsets(track_offset, scene_offset)

	def move(self, tracks, scenes):
		if self._is_linked():
			debug('sending to linked delegation...')
			self._perform_offset_change(tracks, scenes)
		else:
			if self._snap_offsets:
				tracks, scenes = self._snapped_offsets(tracks, scenes)
			self._session_ring.move(tracks, scenes)
			self._update_highlight()
			self.notify_offset(self._session_ring.track_offset, self._session_ring.scene_offset)
			self.notify_tracks()

	@staticmethod
	def _perform_offset_change(track_increment, scene_increment):
		debug('_perform_offset_change')
		instanceObject = get_yt_linked_session_ring_instances()
		scenes = Live.Application.get_application().get_document().scenes
		instances_covering_session = 0
		found_negative_offset = False
		minimal_track_offset = -1
		minimal_scene_offset = -1
		for instance in instanceObject._linked_session_instances:
			new_track_offset = instance.track_offset + track_increment
			new_scene_offset = instance.scene_offset + scene_increment
			if new_track_offset >= 0:
				if new_scene_offset >= 0:
					if new_track_offset < len(instance.tracks_to_use()) and new_scene_offset < len(scenes):
						instances_covering_session += 1
						if minimal_track_offset < 0:
							minimal_track_offset = new_track_offset
						else:
							minimal_track_offset = min(minimal_track_offset, new_track_offset)
						if minimal_scene_offset < 0:
							minimal_scene_offset = new_scene_offset
						else:
							minimal_scene_offset = min(minimal_scene_offset, new_scene_offset)
					else:
						found_negative_offset = True
						break

		if not found_negative_offset:
			if instances_covering_session > 0:
				instanceObject._minimal_track_offset = int(minimal_track_offset)
				instanceObject._minimal_scene_offset = int(minimal_scene_offset)
				for instance in instanceObject._linked_session_instances:
					if instance._snap_offsets:
						tracks, scenes = instance._snapped_offsets(track_increment, scene_increment)
					instance._session_ring.move(track_increment, scene_increment)
					instance._update_highlight()
					instance.notify_offset(instance._session_ring.track_offset, instance._session_ring.scene_offset)
					instance.notify_tracks()



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


class SpecialTransportComponent(TransportComponent):

	new_tap_tempo_button = ButtonControl()

	# def _update_stop_button_color(self):
	# 	self._stop_button.color = 'Transport.StopOn' if self._play_toggle.is_toggled else 'Transport.StopOff'

	@new_tap_tempo_button.pressed
	def tap_tempo_button(self, button):
		debug('tap_tempo')
		self.song.tap_tempo()


class MonoEncoderElement(EncoderElement):

	def __init__(self, name = 'MonoEncoder', num = 0, script = None, mapping_feedback_delay = 1, monobridge = None, *a, **k):
		super(MonoEncoderElement, self).__init__(map_mode=Live.MidiMap.MapMode.absolute, *a, **k)


class MonoButtonElement(ButtonElement):

	def __init__(self, name = 'MonoButton', script = None, color_map = None, monobridge = None, *a, **k):
		super(MonoButtonElement, self).__init__(name = name, *a, **k)
		# self._color_map = color_map or [2, 64, 4, 8, 16, 127, 32]
# 		self._num_colors = 7
# 		self._num_flash_states = 18
# 		self._flash_state = 0
# 		self._color = 0
# 		self._on_value = 127
# 		self._off_value = 0
# 		self._darkened = 0
# 		self._is_enabled = True
#
	# def turn_on(self, force = False):
	# 	self.force_next_send()
	# 	if self._on_value in range(0, 128):
	# 		self.send_value(self._on_value)
	# 	else:
	# 		try:
	# 			color = self._skin[self._on_value]
	# 			color.draw(self)
	# 		except SkinColorMissingError:
	# 			#super(MonoButtonElement, self).turn_on()
	# 			debug('skin color missing', self._on_value)
	# 			self.send_value(127)
	#
	#
	# def turn_off(self, force = False):
	# 	self.force_next_send()
	# 	#debug('turn off:', self._off_value)
	# 	if self._off_value in range(0, 128):
	# 		self.send_value(self._off_value)
	# 	else:
	# 		try:
	# 			color = self._skin[self._off_value]
	# 			color.draw(self)
	# 		except SkinColorMissingError:
	# 			#super(MonoButtonElement, self).turn_off()
	# 			debug('skin color missing', self._off_value)
	# 			self.send_value(0)

	def set_light(self, value):
		try:
			super(MonoButtonElement, self).set_light(value)
		except:
			debug('set_light exception for:', self._name if hasattr(self, '_name') else None, 'value:', value)



class YaeltexUniversal(ControlSurface):

	_timer = 0
	_touched = 0
	flash_status = 1
	# _active_instances = []

	def _combine_active_instances():
		debug('_combine_active_instances...')
		globalInstances = get_yt_linked_session_ring_instances()
		support_devices = False
		for instance in globalInstances._active_instances:
			support_devices |= instance._device != None

		track_offset = 0
		if globalInstances._active_instances:
			first_instance = globalInstances._active_instances[0]
			track_offset = first_instance._session_ring.track_offset
		for instance in globalInstances._active_instances:
			instance._activate_combination_mode(track_offset, support_devices)
			track_offset += instance._session_ring.num_tracks

	_combine_active_instances = staticmethod(_combine_active_instances)

	def _activate_combination_mode(self, track_offset, support_devices):
		self._session_ring.link_with_track_offset(track_offset)

	def _should_combine(self):
		return DO_COMBINE

	def _do_combine(self):
		if self._should_combine():
			globalInstances = get_yt_linked_session_ring_instances()
			if self not in globalInstances._active_instances:
				globalInstances._active_instances = sorted((globalInstances._active_instances + [self]),
				  key=(lambda x: x._instance_id))
				YaeltexUniversal._combine_active_instances()

	def _do_uncombine(self):
		globalInstances = get_yt_linked_session_ring_instances()
		if self in globalInstances._active_instances:
			globalInstances._active_instances.remove(self)
			self._session_ring.unlink()
			YaeltexUniversal._combine_active_instances()


	def __init__(self, c_instance):
		self.__c_instance = c_instance
		self._instance_id = c_instance.instance_identifier()
		# debug('instance_id:', self._instance_id)
		super(YaeltexUniversal, self).__init__(c_instance)
		self._skin = Skin(YAELTEXColors)
		with self.component_guard():
			self._setup_controls()
			self._setup_session_control()
			self._setup_mixer_control()
			self._setup_view_control()
			self._setup_transport_control()
			self._setup_device_control()
			# self._setup_session_recording_component()
			# self._setup_main_modes()
		# self._main_modes.selected_mode = 'Main'
		# self._main_modes.set_enabled(True)
		self._do_combine()


	def instance_identifier(self):
		return self.__c_instance.instance_identifier

	def _setup_controls(self):
		is_momentary = True
		optimized = True
		resource = PrioritizedResource
		self._mute_buttons = [MonoButtonElement(is_momentary = is_momentary, msg_type = MIDI_NOTE_TYPE, channel = MUTE_CHANNEL, identifier = MUTE_NOTES[index], name = 'MuteButton_' + str(index), script = self, skin = self._skin, optimized_send_midi = optimized, resource_type = resource) for index in range(len(MUTE_NOTES))]
		self._solo_buttons = [MonoButtonElement(is_momentary = is_momentary, msg_type = MIDI_NOTE_TYPE, channel = SOLO_CHANNEL, identifier = SOLO_NOTES[index], name = 'SoloButton_' + str(index), script = self, skin = self._skin, optimized_send_midi = optimized, resource_type = resource) for index in range(len(SOLO_NOTES))]
		self._arm_buttons = [MonoButtonElement(is_momentary = is_momentary, msg_type = MIDI_NOTE_TYPE, channel = ARM_CHANNEL, identifier = ARM_NOTES[index], name = 'ArmButton_' + str(index), script = self, skin = self._skin, optimized_send_midi = optimized, resource_type = resource) for index in range(len(ARM_NOTES))]
		self._select_buttons = [MonoButtonElement(is_momentary = is_momentary, msg_type = MIDI_NOTE_TYPE, channel = SELECT_CHANNEL, identifier = SELECT_NOTES[index], name = 'SelectButton_' + str(index), script = self, skin = self._skin, optimized_send_midi = optimized, resource_type = resource) for index in range(len(SELECT_NOTES))]
		self._crossfade_assign_buttons = [MonoButtonElement(is_momentary = is_momentary, msg_type = MIDI_NOTE_TYPE, channel = CROSSFADE_ASSIGN_CHANNEL, identifier = CROSSFADE_ASSIGN_NOTES[index], name = 'CrossfadeAssignButton_' + str(index), script = self, skin = self._skin, optimized_send_midi = optimized, resource_type = resource) for index in range(len(CROSSFADE_ASSIGN_NOTES))]

		self._cliplaunch_buttons = [MonoButtonElement(is_momentary = is_momentary, msg_type = MIDI_NOTE_TYPE, channel = CLIPLAUNCH_CHANNEL, identifier = CLIPLAUNCH_NOTES[index], name = 'ClipLaunchButton_' + str(index), script = self, skin = self._skin, optimized_send_midi = optimized, resource_type = resource) for index in range(len(CLIPLAUNCH_NOTES))]
		self._clipstop_buttons = [MonoButtonElement(is_momentary = is_momentary, msg_type = MIDI_NOTE_TYPE, channel = CLIPSTOP_CHANNEL, identifier = CLIPSTOP_NOTES[index], name = 'ClipStopButton_' + str(index), script = self, skin = self._skin, optimized_send_midi = optimized, resource_type = resource) for index in range(len(CLIPSTOP_NOTES))]
		self._all_clipstop_button = MonoButtonElement(is_momentary = is_momentary, msg_type = MIDI_NOTE_TYPE, channel = ALLCLIPSTOP_CHANNEL, identifier = ALLCLIPSTOP_NOTE, name = 'AllClipStopButton', script = self, skin = self._skin, optimized_send_midi = optimized, resource_type = resource)
		self._scenelaunch_buttons = [MonoButtonElement(is_momentary = is_momentary, msg_type = MIDI_NOTE_TYPE, channel = SCENELAUNCH_CHANNEL, identifier = SCENELAUNCH_NOTES[index], name = 'SceneLaunchButton_' + str(index), script = self, skin = self._skin, optimized_send_midi = optimized, resource_type = resource) for index in range(len(SCENELAUNCH_NOTES))]

		self._session_nav_up = MonoButtonElement(is_momentary = is_momentary, msg_type = MIDI_NOTE_TYPE, channel = SESSIONNAV_CHANNEL, identifier = SESSIONNAV_NOTES[0], name = 'SessionNavUpButton', script = self, skin = self._skin, optimized_send_midi = optimized, resource_type = resource)
		self._session_nav_down = MonoButtonElement(is_momentary = is_momentary, msg_type = MIDI_NOTE_TYPE, channel = SESSIONNAV_CHANNEL, identifier = SESSIONNAV_NOTES[1], name = 'SessionNavDownButton', script = self, skin = self._skin, optimized_send_midi = optimized, resource_type = resource)
		self._session_nav_left = MonoButtonElement(is_momentary = is_momentary, msg_type = MIDI_NOTE_TYPE, channel = SESSIONNAV_CHANNEL, identifier = SESSIONNAV_NOTES[2], name = 'SessionNavLeftButton', script = self, skin = self._skin, optimized_send_midi = optimized, resource_type = resource)
		self._session_nav_right = MonoButtonElement(is_momentary = is_momentary, msg_type = MIDI_NOTE_TYPE, channel = SESSIONNAV_CHANNEL, identifier = SESSIONNAV_NOTES[3], name = 'SessionNavRightButton', script = self, skin = self._skin, optimized_send_midi = optimized, resource_type = resource)

		self._session_selected_clip_launch = MonoButtonElement(is_momentary = is_momentary, msg_type = MIDI_NOTE_TYPE, channel = SESSIONCLIPLAUNCH_CHANNEL, identifier = SESSIONCLIPLAUNCH_NOTE, name = 'SessionSelectedClipLaunch', script = self, skin = self._skin, optimized_send_midi = optimized, resource_type = resource)
		self._session_selected_scene_launch = MonoButtonElement(is_momentary = is_momentary, msg_type = MIDI_NOTE_TYPE, channel = SESSIONSCENELAUNCH_CHANNEL, identifier = SESSIONSCENELAUNCH_NOTE, name = 'SessionSelectedSceneLaunch', script = self, skin = self._skin, optimized_send_midi = optimized, resource_type = resource)

		self._master_select_button = MonoButtonElement(is_momentary = is_momentary, msg_type = MIDI_NOTE_TYPE, channel = MASTER_SELECT_CHANNEL, identifier = MASTER_SELECT_NOTE, name = 'MasterSelect_Button', script = self, skin = self._skin, optimized_send_midi = optimized, resource_type = resource)

		self._device_randomize_macro_button = MonoButtonElement(is_momentary = is_momentary, msg_type = MIDI_NOTE_TYPE, channel = PARAMETER_CHANNEL, identifier = DEVICE_RANDOMIZE_MACRO_NOTE, name = 'DeviceBankPrev_Button', script = self, skin = self._skin, optimized_send_midi = optimized, resource_type = resource)
		self._device_add_macro_button = MonoButtonElement(is_momentary = is_momentary, msg_type = MIDI_NOTE_TYPE, channel = PARAMETER_CHANNEL, identifier = DEVICE_ADD_MACRO_NOTE, name = 'DeviceBankPrev_Button', script = self, skin = self._skin, optimized_send_midi = optimized, resource_type = resource)
		self._device_delete_macro_button = MonoButtonElement(is_momentary = is_momentary, msg_type = MIDI_NOTE_TYPE, channel = PARAMETER_CHANNEL, identifier = DEVICE_DELETE_MACRO_NOTE, name = 'DeviceBankNext_Button', script = self, skin = self._skin, optimized_send_midi = optimized, resource_type = resource)
		self._device_prev_macro_button = MonoButtonElement(is_momentary = is_momentary, msg_type = MIDI_NOTE_TYPE, channel = PARAMETER_CHANNEL, identifier = DEVICE_PREV_MACRO_NOTE, name = 'DeviceBankPrev_Button', script = self, skin = self._skin, optimized_send_midi = optimized, resource_type = resource)
		self._device_next_macro_button = MonoButtonElement(is_momentary = is_momentary, msg_type = MIDI_NOTE_TYPE, channel = PARAMETER_CHANNEL, identifier = DEVICE_NEXT_MACRO_NOTE, name = 'DeviceBankNext_Button', script = self, skin = self._skin, optimized_send_midi = optimized, resource_type = resource)
		self._device_bank_prev_button = MonoButtonElement(is_momentary = is_momentary, msg_type = MIDI_NOTE_TYPE, channel = PARAMETER_CHANNEL, identifier = DEVICE_BANK_PREV_NOTE, name = 'DeviceBankPrev_Button', script = self, skin = self._skin, optimized_send_midi = optimized, resource_type = resource)
		self._device_bank_next_button = MonoButtonElement(is_momentary = is_momentary, msg_type = MIDI_NOTE_TYPE, channel = PARAMETER_CHANNEL, identifier = DEVICE_BANK_NEXT_NOTE, name = 'DeviceBankNext_Button', script = self, skin = self._skin, optimized_send_midi = optimized, resource_type = resource)
		self._parameter_on_off_button = MonoButtonElement(is_momentary = is_momentary, msg_type = MIDI_NOTE_TYPE, channel = PARAMETER_CHANNEL, identifier = PARAMETER_ON_OFF_NOTE, name = 'ParameterOnOff_Button', script = self, skin = self._skin, optimized_send_midi = optimized, resource_type = resource)
		self._device_nav_prev_button = MonoButtonElement(is_momentary = is_momentary, msg_type = MIDI_NOTE_TYPE, channel = PARAMETER_CHANNEL, identifier = DEVICE_NAV_PREV, name = 'DeviceNavPrev_Button', script = self, skin = self._skin, optimized_send_midi = optimized, resource_type = resource)
		self._device_nav_next_button = MonoButtonElement(is_momentary = is_momentary, msg_type = MIDI_NOTE_TYPE, channel = PARAMETER_CHANNEL, identifier = DEVICE_NAV_NEXT, name = 'DeviceNavNext_Button', script = self, skin = self._skin, optimized_send_midi = optimized, resource_type = resource)


		self._play_button = MonoButtonElement(is_momentary = is_momentary, msg_type = MIDI_NOTE_TYPE, channel = TRANSPORT_CHANNEL, identifier = TRANSPORT_PLAY_NOTE, name = 'PlayButton', script = self, skin = self._skin, optimized_send_midi = optimized, resource_type = resource)
		self._stop_button = MonoButtonElement(is_momentary = is_momentary, msg_type = MIDI_NOTE_TYPE, channel = TRANSPORT_CHANNEL, identifier = TRANSPORT_STOP_NOTE, name = 'StopButton', script = self, skin = self._skin, optimized_send_midi = optimized, resource_type = resource)
		self._record_button = MonoButtonElement(is_momentary = is_momentary, msg_type = MIDI_NOTE_TYPE, channel = TRANSPORT_CHANNEL, identifier = TRANSPORT_REC_NOTE, name = 'RecordButton', script = self, skin = self._skin, optimized_send_midi = optimized, resource_type = resource)
		self._overdub_button = MonoButtonElement(is_momentary = is_momentary, msg_type = MIDI_NOTE_TYPE, channel = TRANSPORT_CHANNEL, identifier = TRANSPORT_OD_NOTE, name = 'OverdubButton', script = self, skin = self._skin, optimized_send_midi = optimized, resource_type = resource)
		self._metronome_button = MonoButtonElement(is_momentary = is_momentary, msg_type = MIDI_NOTE_TYPE, channel = TRANSPORT_CHANNEL, identifier = TRANSPORT_CLICK_NOTE, name = 'MetronomeButton', script = self, skin = self._skin, optimized_send_midi = optimized, resource_type = resource)
		self._tap_tempo_button = MonoButtonElement(is_momentary = is_momentary, msg_type = MIDI_NOTE_TYPE, channel = TRANSPORT_CHANNEL, identifier = TRANSPORT_TAPTEMPO_NOTE, name = 'TapTempoButton', script = self, skin = self._skin, optimized_send_midi = optimized, resource_type = resource)
		self._loop_button = MonoButtonElement(is_momentary = is_momentary, msg_type = MIDI_NOTE_TYPE, channel = TRANSPORT_CHANNEL, identifier = TRANSPORT_LOOP_NOTE, name = 'LoopButton', script = self, skin = self._skin, optimized_send_midi = optimized, resource_type = resource)

		self._volume_controls = [MonoEncoderElement(mapping_feedback_delay = -1, msg_type = MIDI_CC_TYPE, channel = VOLUME_CHANNEL, identifier = VOLUME_CCS[index], name = 'Volume_Control_' + str(index), num = index, script = self, optimized_send_midi = optimized, resource_type = resource) for index in range(len(VOLUME_CCS))]
		self._pan_controls = [MonoEncoderElement(mapping_feedback_delay = -1, msg_type = MIDI_CC_TYPE, channel = PAN_CHANNEL, identifier = PAN_CCS[index], name = 'Pan_Control_' + str(index), num = index, script = self, optimized_send_midi = optimized, resource_type = resource) for index in range(len(PAN_CCS))]

		self._sendA_controls = [MonoEncoderElement(mapping_feedback_delay = -1, msg_type = MIDI_CC_TYPE, channel = SENDA_CHANNEL, identifier = SENDA_CCS[index], name = 'SendA_Control_' + str(index), num = index, script = self, optimized_send_midi = optimized, resource_type = resource) for index in range(len(SENDA_CCS))]
		self._sendB_controls = [MonoEncoderElement(mapping_feedback_delay = -1, msg_type = MIDI_CC_TYPE, channel = SENDB_CHANNEL, identifier = SENDB_CCS[index], name = 'SendB_Control_' + str(index), num = index, script = self, optimized_send_midi = optimized, resource_type = resource) for index in range(len(SENDB_CCS))]
		self._sendC_controls = [MonoEncoderElement(mapping_feedback_delay = -1, msg_type = MIDI_CC_TYPE, channel = SENDC_CHANNEL, identifier = SENDC_CCS[index], name = 'SendC_Control_' + str(index), num = index, script = self, optimized_send_midi = optimized, resource_type = resource) for index in range(len(SENDC_CCS))]
		self._sendD_controls = [MonoEncoderElement(mapping_feedback_delay = -1, msg_type = MIDI_CC_TYPE, channel = SENDD_CHANNEL, identifier = SENDD_CCS[index], name = 'SendD_Control_' + str(index), num = index, script = self, optimized_send_midi = optimized, resource_type = resource) for index in range(len(SENDD_CCS))]
		self._sendE_controls = [MonoEncoderElement(mapping_feedback_delay = -1, msg_type = MIDI_CC_TYPE, channel = SENDE_CHANNEL, identifier = SENDE_CCS[index], name = 'SendE_Control_' + str(index), num = index, script = self, optimized_send_midi = optimized, resource_type = resource) for index in range(len(SENDE_CCS))]
		self._sendF_controls = [MonoEncoderElement(mapping_feedback_delay = -1, msg_type = MIDI_CC_TYPE, channel = SENDF_CHANNEL, identifier = SENDF_CCS[index], name = 'SendF_Control_' + str(index), num = index, script = self, optimized_send_midi = optimized, resource_type = resource) for index in range(len(SENDF_CCS))]
		self._sendG_controls = [MonoEncoderElement(mapping_feedback_delay = -1, msg_type = MIDI_CC_TYPE, channel = SENDG_CHANNEL, identifier = SENDG_CCS[index], name = 'SendG_Control_' + str(index), num = index, script = self, optimized_send_midi = optimized, resource_type = resource) for index in range(len(SENDG_CCS))]
		self._sendH_controls = [MonoEncoderElement(mapping_feedback_delay = -1, msg_type = MIDI_CC_TYPE, channel = SENDH_CHANNEL, identifier = SENDH_CCS[index], name = 'SendH_Control_' + str(index), num = index, script = self, optimized_send_midi = optimized, resource_type = resource) for index in range(len(SENDH_CCS))]

		self._return_volume_controls = [MonoEncoderElement(mapping_feedback_delay = -1, msg_type = MIDI_CC_TYPE, channel = RETURN_VOLUME_CHANNEL, identifier = RETURN_VOLUME_CCS[index], name = 'Return_Volume_Control_' + str(index), num = index, script = self, optimized_send_midi = optimized, resource_type = resource) for index in range(len(RETURN_VOLUME_CCS))]

		self._track_parameter_on_off_buttons  = [MonoButtonElement(is_momentary = is_momentary, msg_type = MIDI_NOTE_TYPE, channel = TRACK_PARAMETER_ON_OFF_CHANNEL, identifier = TRACK_PARAMETER_ON_OFF_NOTES[index], name = 'TrackParameterOnOff_Button_' + str(index), script = self, skin = self._skin, optimized_send_midi = optimized, resource_type = resource) for index in range(len(TRACK_PARAMETER_ON_OFF_NOTES))]

		def make_track_parameter_controls(instance, track_index, device_index, chn, ccs):
			PARAM_BANK_SIZE = 16 if EXTENDED_PARAM_DIALS else 8
			attr_name = str('_track'+str(track_index+1)+'_parameter'+str(device_index+1)+'controls')
			element_name = str('Track'+str(track_index+1)+'_Device'+str(device_index+1)+'_Parameter_Controls')
			elements = [MonoEncoderElement(mapping_feedback_delay = -1, msg_type = MIDI_CC_TYPE, channel = chn, identifier = ccs[index+(PARAM_BANK_SIZE*device_index)], name = element_name + str(index), num = index, script = instance, optimized_send_midi = optimized, resource_type = resource) for index in range(8)]
			setattr(instance, attr_name, elements)
			matrix_attr_name = '_track'+str(track_index+1)+'_parameter'+str(device_index+1)+'_control_matrix'
			matrix_element_name = 'Track'+str(track_index+1)+'_Parameter1_Matrix'
			matrix = ButtonMatrixElement(name = matrix_element_name, rows = [getattr(instance, attr_name)])
			setattr(instance, matrix_attr_name, matrix)


		for track in range(8):
			for device in range(8):
				make_track_parameter_controls(instance = self, track_index = track, device_index = device, chn = TRACK_PARAMETER_CHANNELS[track], ccs = TRACK_PARAMETER_CCS[track])

		def make_selected_track_parameter_controls(instance, device_index, chn, ccs):
			PARAM_BANK_SIZE = 16 if EXTENDED_PARAM_DIALS else 8
			attr_name = str('_selected_track_parameter'+str(device_index+1)+'controls')
			element_name = str('SelectedTrack_Device'+str(device_index+1)+'_Parameter_Controls')
			elements = [MonoEncoderElement(mapping_feedback_delay = -1, msg_type = MIDI_CC_TYPE, channel = chn, identifier = ccs[index+(PARAM_BANK_SIZE*device_index)], name = element_name + str(index), num = index, script = instance, optimized_send_midi = optimized, resource_type = resource) for index in range(8)]
			setattr(instance, attr_name, elements)
			matrix_attr_name = '_selected_track_parameter'+str(device_index+1)+'_control_matrix'
			# logger.warning('name is:'+matrix_attr_name)
			matrix_element_name = 'SelectedTrack_Parameter'+str(device_index+1)+'_Matrix'
			matrix = ButtonMatrixElement(name = matrix_element_name, rows = [getattr(instance, attr_name)])
			setattr(instance, matrix_attr_name, matrix)

		for device in range(8):
			make_selected_track_parameter_controls(instance = self, device_index = device, chn = SELECTEDTRACK_PARAMETER_CHANNEL, ccs = SELECTEDTRACK_PARAMETER_CCS)

		self._track_select_control = MonoEncoderElement(mapping_feedback_delay = -1, msg_type = MIDI_CC_TYPE, channel = TRACK_SELECT_CHANNEL, identifier = TRACK_SELECT_CC, name = 'TrackSelect_Control', num = 0, script = self, optimized_send_midi = optimized, resource_type = resource)
		self._scene_select_control = MonoEncoderElement(mapping_feedback_delay = -1, msg_type = MIDI_CC_TYPE, channel = SCENE_SELECT_CHANNEL, identifier = SCENE_SELECT_CC, name = 'SceneSelect_Control', num = 0, script = self, optimized_send_midi = optimized, resource_type = resource)
		self._track_bank_nav_control = MonoEncoderElement(mapping_feedback_delay = -1, msg_type = MIDI_CC_TYPE, channel = TRACK_BANK_NAV_CHANNEL, identifier = TRACK_BANK_NAV_CC, name = 'TrackBank_Control', num = 0, script = self, optimized_send_midi = optimized, resource_type = resource)
		self._scene_bank_nav_control = MonoEncoderElement(mapping_feedback_delay = -1, msg_type = MIDI_CC_TYPE, channel = SCENE_BANK_NAV_CHANNEL, identifier = SCENE_BANK_NAV_CC, name = 'SceneBank_Control', num = 0, script = self, optimized_send_midi = optimized, resource_type = resource)

		self._masterVolume_control = MonoEncoderElement(mapping_feedback_delay = -1, msg_type = MIDI_CC_TYPE, channel = MASTER_VOLUME_CHANNEL, identifier = MASTER_VOLUME_CC, name = 'Master_Volume_Control', num = 0, script = self, optimized_send_midi = optimized, resource_type = resource)
		self._cueVolume_control = MonoEncoderElement(mapping_feedback_delay = -1, msg_type = MIDI_CC_TYPE, channel = CUE_VOLUME_CHANNEL, identifier = CUE_VOLUME_CC, name = 'Cue_Volume_Control', num = 0, script = self, optimized_send_midi = optimized, resource_type = resource)
		self._crossfader_control = MonoEncoderElement(mapping_feedback_delay = -1, msg_type = MIDI_CC_TYPE, channel = CROSSFADER_CHANNEL, identifier = CROSSFADER_CC, name = 'Crossfader_Control', num = 0, script = self, optimized_send_midi = optimized, resource_type = resource)
		self._tempo_control = MonoEncoderElement(mapping_feedback_delay = -1, msg_type = MIDI_CC_TYPE, channel = TEMPO_CONTROL_CHANNEL, identifier = TEMPO_CONTROL_CC, name = 'Tempo_Control', num = 0, script = self, optimized_send_midi = optimized, resource_type = resource)


		self._parameter_controls = [MonoEncoderElement(mapping_feedback_delay = -1, msg_type = MIDI_CC_TYPE, channel = PARAMETER_CHANNEL, identifier = PARAMETER_CCS[index], name = 'Parameter_Control_' + str(index), num = index, script = self, optimized_send_midi = optimized, resource_type = resource) for index in range(len(PARAMETER_CCS))]

		# self._encoder_button = [MonoButtonElement(is_momentary = is_momentary, msg_type = MIDI_NOTE_TYPE, channel = CHANNEL, identifier = DS1_ENCODER_BUTTONS[index], name = 'EncoderButton_' + str(index), script = self, skin = self._skin, optimized_send_midi = optimized, resource_type = resource) for index in range(4)]
		self._mute_button_matrix = ButtonMatrixElement(name = 'MuteButtonMatrix', rows = [self._mute_buttons])
		self._solo_button_matrix = ButtonMatrixElement(name = 'SoloButtonMatrix', rows = [self._solo_buttons])
		self._arm_button_matrix = ButtonMatrixElement(name = 'ArmButtonMatrix', rows = [self._arm_buttons])
		self._select_button_matrix = ButtonMatrixElement(name = 'SelectButtonMatrix', rows = [self._select_buttons])


		self._volume_control_matrix = ButtonMatrixElement(name = 'VolumeControlMatrix', rows = [self._volume_controls])
		self._pan_control_matrix = ButtonMatrixElement(name = 'PanControlMatrix', rows = [self._pan_controls])
		self._parameter_control_matrix = ButtonMatrixElement(name = 'ParameterControlMatrix', rows = [self._parameter_controls])

		self._send_control_matrix = ButtonMatrixElement(name = 'SendControlMatrix', rows = [self._sendA_controls,
																							self._sendB_controls,
																							self._sendC_controls,
																							self._sendD_controls,
																							self._sendE_controls,
																							self._sendF_controls,
																							self._sendG_controls,
																							self._sendH_controls])

		self._track1_parameter_on_off_buttons = ButtonMatrixElement(name = 'Track1_Parameter_OnOff_Matrix', rows = [self._track_parameter_on_off_buttons[0:8]])
		self._track2_parameter_on_off_buttons = ButtonMatrixElement(name = 'Track2_Parameter_OnOff_Matrix', rows = [self._track_parameter_on_off_buttons[8:16]])
		self._track3_parameter_on_off_buttons = ButtonMatrixElement(name = 'Track3_Parameter_OnOff_Matrix', rows = [self._track_parameter_on_off_buttons[16:24]])
		self._track4_parameter_on_off_buttons = ButtonMatrixElement(name = 'Track4_Parameter_OnOff_Matrix', rows = [self._track_parameter_on_off_buttons[24:32]])
		self._track5_parameter_on_off_buttons = ButtonMatrixElement(name = 'Track5_Parameter_OnOff_Matrix', rows = [self._track_parameter_on_off_buttons[32:40]])
		self._track6_parameter_on_off_buttons = ButtonMatrixElement(name = 'Track6_Parameter_OnOff_Matrix', rows = [self._track_parameter_on_off_buttons[40:48]])
		self._track7_parameter_on_off_buttons = ButtonMatrixElement(name = 'Track7_Parameter_OnOff_Matrix', rows = [self._track_parameter_on_off_buttons[48:56]])
		self._track8_parameter_on_off_buttons = ButtonMatrixElement(name = 'Track8_Parameter_OnOff_Matrix', rows = [self._track_parameter_on_off_buttons[56:64]])
		self._selected_track_parameter_on_off_buttons = ButtonMatrixElement(name = 'Selected_Track_Parameter_OnOff_Matrix', rows = [self._track_parameter_on_off_buttons[64:72]])

		self._return_volume_control_matrix = ButtonMatrixElement(name = 'ReturnVolumeControlMatrix', rows = [self._return_volume_controls])

		self._output_meter_level_controls = [MonoEncoderElement(mapping_feedback_delay = -1, msg_type = MIDI_CC_TYPE, channel = METER_CHANNEL, identifier = METER_CCS[index], name = 'Output_Meter_Level_Control_' + str(index), num = index, script = self, optimized_send_midi = False, resource_type = resource) for index in range(len(METER_CCS))]
		self._output_meter_level_matrix = ButtonMatrixElement(name = 'OutputMeterLevelMatrix', rows = [self._output_meter_level_controls])

		self._output_meter_left_controls = [MonoEncoderElement(mapping_feedback_delay = -1, msg_type = MIDI_CC_TYPE, channel = METER_CHANNEL, identifier = METER_LEFT_CCS[index], name = 'Output_Meter_Left_Control_' + str(index), num = index, script = self, optimized_send_midi = False, resource_type = resource) for index in range(len(METER_LEFT_CCS))]
		self._output_meter_left_matrix = ButtonMatrixElement(name = 'OutputMeterLeftMatrix', rows = [self._output_meter_left_controls])

		self._output_meter_right_controls = [MonoEncoderElement(mapping_feedback_delay = -1, msg_type = MIDI_CC_TYPE, channel = METER_CHANNEL, identifier = METER_RIGHT_CCS[index], name = 'Output_Meter_Right_Control_' + str(index), num = index, script = self, optimized_send_midi = False, resource_type = resource) for index in range(len(METER_RIGHT_CCS))]
		self._output_meter_right_matrix = ButtonMatrixElement(name = 'OutputMeterRightMatrix', rows = [self._output_meter_right_controls])

		self._output_meter_sum_controls = [MonoEncoderElement(mapping_feedback_delay = -1, msg_type = MIDI_CC_TYPE, channel = METER_CHANNEL, identifier = METER_SUM_CCS[index], name = 'Output_Meter_Sum_Control_' + str(index), num = index, script = self, optimized_send_midi = False, resource_type = resource) for index in range(len(METER_SUM_CCS))]
		self._output_meter_sum_matrix = ButtonMatrixElement(name = 'OutputMeterSumMatrix', rows = [self._output_meter_sum_controls])

		self._cliplaunch_button_matrix = ButtonMatrixElement(name = 'ClipLaunchButtonMatrix', rows = [self._cliplaunch_buttons[0:16],
																									self._cliplaunch_buttons[16:32],
																									self._cliplaunch_buttons[32:48],
																									self._cliplaunch_buttons[48:64],
																									self._cliplaunch_buttons[64:80],
																									self._cliplaunch_buttons[80:96],
																									self._cliplaunch_buttons[96:112],
																									self._cliplaunch_buttons[112:128]])

		self._clipstop_button_matrix = ButtonMatrixElement(name = 'ClipStopButtonMatrix', rows = [self._clipstop_buttons])
		self._scenelaunch_button_matrix = ButtonMatrixElement(name = 'SceneLaunchMatrix', rows = [self._scenelaunch_buttons])

		self._crossfade_assign_button_matrix = ButtonMatrixElement(name = 'CrossfadeAssignMatrix', rows = [self._crossfade_assign_buttons])



	def _setup_autoarm(self):
		self._auto_arm = AutoArmComponent(name='Auto_Arm')
		self._auto_arm.can_auto_arm_track = self._can_auto_arm_track


	def _tracks_to_use(self):
		return self.song.visible_tracks + self.song.return_tracks


	def _setup_session_control(self):
		self._session_ring = SpecialSessionRingComponent(script = self, num_tracks = SESSION_BOX_SIZE[0], num_scenes = SESSION_BOX_SIZE[1], tracks_to_use = self._tracks_to_use)
		# self._session_ring._session_ring.callback = nop
		self._session_ring.set_enabled(True)

		self._session_navigation = SpecialSessionNavigationComponent(name = 'SessionNavigation', session_ring = self._session_ring)
		self._session_navigation._vertical_banking.scroll_up_button.color = 'Session.NavigationButtonOn'
		self._session_navigation._vertical_banking.scroll_down_button.color = 'Session.NavigationButtonOn'
		self._session_navigation._horizontal_banking.scroll_up_button.color = 'Session.NavigationButtonOn'
		self._session_navigation._horizontal_banking.scroll_down_button.color = 'Session.NavigationButtonOn'
		self._session_navigation.layer = Layer(priority = 4,
											up_button = self._session_nav_up,
											down_button = self._session_nav_down,
											left_button = self._session_nav_left,
											right_button = self._session_nav_right,
											scene_bank_nav_dial = self._scene_bank_nav_control,
											track_bank_nav_dial = self._track_bank_nav_control,)
		self._session_navigation.set_enabled(True)

		self._session = SpecialSessionComponent(session_ring = self._session_ring, auto_name = True)
		self._session.set_rgb_mode(LIVE_COLORS_TO_MIDI_VALUES, RGB_COLOR_TABLE, clip_slots_only=True)
		self._session.layer = Layer(priority = 4,
			clip_launch_buttons = self._cliplaunch_button_matrix.submatrix[:SESSION_BOX_SIZE[0], :SESSION_BOX_SIZE[1]],
			stop_track_clip_buttons = self._clipstop_button_matrix.submatrix[:SESSION_BOX_SIZE[0],:],
			stop_all_clips_button = self._all_clipstop_button,
			scene_launch_buttons = self._scenelaunch_button_matrix.submatrix[:SESSION_BOX_SIZE[1],:],
			selected_clip_launch_button = self._session_selected_clip_launch,
			selected_scene_launch_button = self._session_selected_scene_launch)
		#self._session_ring.layer = Layer(priority = 4, scene_bank_nav_dial = self._scene_bank_nav_control, track_bank_nav_dial = self._track_bank_nav_control,)
		# self._session.clips_layer = AddLayerMode(self._session, Layer(priority = 4, clip_launch_buttons = self._top_buttons, stop_track_clip_buttons = self._bottom_buttons))
		self._session.set_enabled(True)


	def _setup_mixer_control(self):

		self._mixer = MonoMixerComponent(name = 'Mixer', num_returns = 8, tracks_provider = self._session_ring, track_assigner = SimpleTrackAssigner(), invert_mute_feedback = True, auto_name = True, enable_skinning = True, enable_vu_meters = VU_METER_ENABLED, channel_strip_component_type=MonoChannelStripComponent)
		self._mixer.set_enabled(False)
		self._mixer.master_strip().set_volume_control(self._masterVolume_control)
		self._mixer.set_prehear_volume_control(self._cueVolume_control)

		LayerNames = ['parameter_controls', 'parameter_controls2', 'parameter_controls3', 'parameter_controls4', 'parameter_controls5', 'parameter_controls6', 'parameter_controls7', 'parameter_controls8']

		if SELECTED_STRIP_PARAMETER_CONTROLS_ENABLED:
			def make_selected_track_parameter_control_layer(instance):
				kw = {'parameter_controls_on_off_buttons':getattr(instance, '_selected_track_parameter_on_off_buttons')}
				for device_index in range(8):
					if STRIP_PARAM_CONTROLS_ENABLED_FLAGS[device_index]:
						kw[LayerNames[device_index]] = getattr(instance, '_selected_track_parameter'+str(device_index+1)+'_control_matrix')
				return kw

			self._selected_strip = self._mixer.selected_strip()
			strip_layer = make_selected_track_parameter_control_layer(instance=self)
			self._selected_strip.layer = Layer(**strip_layer)

		if TRACK_STRIP_PARAMETER_CONTROLS_ENABLED:
			def make_parameter_control_layer(instance, track_index):
				kw = {'parameter_controls_on_off_buttons':getattr(instance, '_track'+str(track_index+1)+'_parameter_on_off_buttons')}
				for device_index in range(8):
					if STRIP_PARAM_CONTROLS_ENABLED_FLAGS[device_index]:
						kw[LayerNames[device_index]] = getattr(instance, '_track'+str(track_index+1)+'_parameter'+str(device_index+1)+'_control_matrix')
				return kw

			self._strip = [self._mixer.channel_strip(index) for index in range(min(SESSION_BOX_SIZE[0], 8))]
			for strip_index in range(len(self._strip)):
				strip_layer = make_parameter_control_layer(instance=self, track_index=strip_index)
				self._strip[strip_index].layer = Layer(**strip_layer)


		self._mixer.layer = Layer(priority = 4,
			volume_controls = self._volume_control_matrix.submatrix[:SESSION_BOX_SIZE[0],:],
			summed_output_meter_level_controls = self._output_meter_sum_matrix.submatrix[:SESSION_BOX_SIZE[0],:],
			mute_buttons = self._mute_button_matrix.submatrix[:SESSION_BOX_SIZE[0],:],
			arm_buttons = self._arm_button_matrix.submatrix[:SESSION_BOX_SIZE[0],:],
			solo_buttons = self._solo_button_matrix.submatrix[:SESSION_BOX_SIZE[0],:],
			track_select_buttons = self._select_button_matrix.submatrix[:SESSION_BOX_SIZE[0],:],
			pan_controls = self._pan_control_matrix.submatrix[:SESSION_BOX_SIZE[0],:],
			return_controls = self._return_volume_control_matrix.submatrix[:SESSION_BOX_SIZE[0],:],
			crossfader_control = self._crossfader_control,
			prehear_volume_control = self._cueVolume_control,
			crossfade_toggles = self._crossfade_assign_button_matrix.submatrix[:SESSION_BOX_SIZE[0],:],
			send_controls = self._send_control_matrix.submatrix[:SESSION_BOX_SIZE[0],:NUM_SEND_CONTROLS],)


			# output_meter_level_controls = self._output_meter_level_matrix,
			# output_meter_left_controls = self._output_meter_left_matrix,
			# output_meter_right_controls = self._output_meter_right_matrix,

		self._mixer.master_strip().layer = Layer(volume_control = self._masterVolume_control, select_button = self._master_select_button)

		self._mixer.set_enabled(True)
		self._mixer._selected_strip.set_enabled(True)


	def _setup_view_control(self):
		self._view_control = SpecialViewControlComponent(name='View_Control')
		self._view_control.layer = Layer(scene_select_dial = self._scene_select_control,
										track_select_dial = self._track_select_control,)
		#self._view_control.main_layer = AddLayerMode(self._view_control, Layer(prev_track_button=self._button[24],
		#											next_track_button= self._button[25],
		#											next_scene_button=self._button[27],
		#											prev_scene_button = self._button[26]))
		self._view_control.set_enabled(True)


	def _setup_transport_control(self):
		self._transport = TransportComponent()
		self._transport.name = 'Transport'
		# self._transport._record_toggle.view_transform = lambda value: 'Transport.RecordOn' if value else 'Transport.RecordOff'
		self._transport.layer = Layer(priority = 4,
			stop_button = self._stop_button,
			play_button = self._play_button,
			record_button = self._record_button,
			metronome_button = self._metronome_button,
			overdub_button = self._overdub_button,
			tap_tempo_button = self._tap_tempo_button,
			tempo_control = self._tempo_control,
			loop_button = self._loop_button)
		self._transport.set_enabled(True)


	def _setup_device_control(self):
		self._device = DeviceComponent(name = 'Device_Component', device_provider = self._device_provider, device_bank_registry = DeviceBankRegistry())
		self._device.layer = Layer(priority = 4, parameter_controls = self._parameter_control_matrix,
												on_off_button = self._parameter_on_off_button,
												bank_prev_button = self._device_bank_prev_button,
												bank_next_button = self._device_bank_next_button,
												add_macro_button = self._device_add_macro_button,
												delete_macro_button = self._device_delete_macro_button,
												prev_macro_button = self._device_prev_macro_button,
												next_macro_button = self._device_next_macro_button,
												randomize_macro_button = self._device_randomize_macro_button,)
		self._device.set_enabled(True)

		self._device_navigation = DeviceNavigator(self._device_provider, self._mixer, self)
		self._device_navigation.layer = Layer(priority = 4, prev_button = self._device_nav_prev_button, next_button = self._device_nav_next_button)
		self._device_navigation.set_enabled(True)


	# def _setup_session_recording_component(self):
	# 	self._clip_creator = ClipCreator()
	# 	self._clip_creator.name = 'ClipCreator'
	# 	self._recorder = SessionRecordingComponent(ViewControlComponent())
	# 	self._recorder.set_enabled(True)
	# 	self._recorder.layer = Layer(priority = 4, automation_button = self._grid[1][2], record_button  = self._grid[2][1],)


	def _setup_main_modes(self):
		self._main_modes = ModesComponent(name = 'MainModes')
		self._main_modes.add_mode('disabled', [])
		self._main_modes.add_mode('Main', [self._device, self._session, self._session_navigation, self._mixer, self._mixer._selected_strip, self._transport])
		self._main_modes.layer = Layer(priority = 4)
		self._main_modes.selected_mode = 'disabled'
		self._main_modes.set_enabled(True)


	def _can_auto_arm_track(self, track):
		routing = track.current_input_routing
		return routing == 'Ext: All Ins' or routing == 'All Ins' or routing.startswith('YaeltexUniversal Input')
		#self._main_modes.selected_mode in ['Sends', 'Device'] and


	# def flash(self):
	# 	if(self.flash_status > 0):
	# 		for control in self.controls:
	# 			if isinstance(control, MonoButtonElement):
	# 				control.flash(self._timer)
		# pass

	# def update_display(self):
	# 	super(ControlSurface, self).update_display()
	# 	self._timer = (self._timer + 1) % 256
	# 	self.flash()


	def touched(self):
		pass


	def check_touch(self):
		pass

	# def connect_script_instances(self, instanciated_scripts):
	# 	debug('connect script instances:', instanciated_scripts)
	# 	for s in instanciated_scripts:
	# 		if isinstance(s, YaeltexUniversal):
	# 			debug('found another instance of YaeltexUniversal')


	def disconnect(self):
		self._do_uncombine()
		super(YaeltexUniversal, self).disconnect()


	def connect_script_instances(self, instanciated_scripts):
		debug('connect_script_instances', instanciated_scripts)
		self._connected_scripts = []
		globalInstances = get_yt_linked_session_ring_instances()
		for script in instanciated_scripts:
			# debug(script)
			if isinstance (script, YaeltexUniversal):
				debug('is Yaeltex.....')
				# YaeltexUniversal._combine_active_instances()
				if not script in globalInstances._active_instances:
					globalInstances._active_instances.append(script)


		debug('connected_scripts:', self._connected_scripts)
		debug('YaeltexUniversal._active_instances:', globalInstances._active_instances)
		self._do_combine()
#	a
