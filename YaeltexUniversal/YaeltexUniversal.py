# by amounra 1120 : http://www.aumhaa.com
# written against Live 10.1.25 on 111520

from __future__ import absolute_import, print_function
import Live
import math
import sys
from re import *
from itertools import imap, chain, starmap

from ableton.v2.base import inject, listens, listens_group
from ableton.v2.control_surface import ControlSurface, ControlElement, Layer, Skin, PrioritizedResource, Component, ClipCreator, DeviceBankRegistry
from ableton.v2.control_surface.elements import ComboElement, ButtonMatrixElement, DoublePressElement, MultiElement, DisplayDataSource, SysexElement
from ableton.v2.control_surface.components import ClipSlotComponent, SceneComponent, SessionComponent, TransportComponent, BackgroundComponent, ViewControlComponent, SessionRingComponent, SessionRecordingComponent, SessionNavigationComponent, MixerComponent, PlayableComponent
from ableton.v2.control_surface.components.mixer import SimpleTrackAssigner
from ableton.v2.control_surface.control import control_color
from ableton.v2.control_surface.mode import AddLayerMode, ModesComponent, DelayMode
from ableton.v2.control_surface.elements.physical_display import PhysicalDisplayElement
from ableton.v2.control_surface.components.session_recording import *

from ableton.v2.control_surface.control import PlayableControl, ButtonControl, control_matrix

from aumhaa.v2.base import initialize_debug
from aumhaa.v2.control_surface import SendLividSysexMode, MomentaryBehaviour, ExcludingMomentaryBehaviour, DelayedExcludingMomentaryBehaviour, ShiftedBehaviour, LatchingShiftedBehaviour, FlashingBehaviour
from aumhaa.v2.control_surface.mod_devices import *
from aumhaa.v2.control_surface.mod import *
from aumhaa.v2.control_surface.elements import MonoEncoderElement, MonoBridgeElement, generate_strip_string
from aumhaa.v2.control_surface.elements.mono_button import *
from aumhaa.v2.control_surface.components import MonoDeviceComponent, DeviceNavigator, TranslationComponent, MonoMixerComponent, MonoChannelStripComponent
from aumhaa.v2.control_surface.components.device import DeviceComponent
from aumhaa.v2.control_surface.components.mono_instrument import *
from aumhaa.v2.livid import LividControlSurface, LividSettings, LividRGB
from aumhaa.v2.control_surface.components.fixed_length_recorder import FixedLengthSessionRecordingComponent
from aumhaa.v2.control_surface.components.device import DeviceComponent
from aumhaa.v2.control_surface.components.m4l_interface import M4LInterfaceComponent

from .Map import *


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


debug = initialize_debug()


class SpecialSessionComponent(SessionComponent):


	def set_scene_launch_buttons(self, buttons):
		assert(not buttons or buttons.width() == self._session_ring.num_scenes and buttons.height() == 1)
		if buttons:
			for button, (x, _) in buttons.iterbuttons():
				scene = self.scene(x)
				#debug('setting scene launch for button:', button, 'scene:', scene)
				scene.set_launch_button(button)

		else:
			for x in xrange(self._session_ring.num_scenes):
				scene = self.scene(x)
				scene.set_launch_button(None)



class SpecialSessionNavigationComponent(SessionNavigationComponent):


	def set_track_select_dial(self, dial):
		self._on_track_select_dial_value.subject = dial


	@listens('value')
	def _on_track_select_dial_value(self, value):
		#debug('_on_track_select_dial_value:', value)
		#self._can_bank_left() and self._bank_left() if value == 127 else self._can_bank_right() and self._bank_right()
		self._horizontal_banking.can_scroll_up() and self._horizontal_banking.scroll_up() if value == 127 else self._horizontal_banking.can_scroll_down() and self._horizontal_banking.scroll_down()



class SpecialTransportComponent(TransportComponent):


	def _update_stop_button_color(self):
		self._stop_button.color = 'Transport.StopOn' if self._play_toggle.is_toggled else 'Transport.StopOff'




class YaeltexUniversal(ControlSurface):


	def __init__(self, c_instance):
		super(YaeltexUniversal, self).__init__(c_instance)
		self._skin = Skin(YAELTEXColors)
		with self.component_guard():
			# self._define_sysex()
			self._setup_controls()
			# self._setup_background()
			# self._setup_m4l_interface()
			self._setup_session_control()
			self._setup_mixer_control()
			# self._setup_transport_control()
			# self._setup_device_control()
			# self._setup_session_recording_component()
			self._setup_main_modes()
		self._main_modes.set_enabled(True)


	def _setup_controls(self):
		is_momentary = True
		optimized = True
		resource = PrioritizedResource
		self._volume_controls = [MonoEncoderElement(mapping_feedback_delay = -1, msg_type = MIDI_CC_TYPE, channel = VOLUME_CHANNEL, identifier = VOLUME_CCS[index], name = 'Volume_Control_' + str(index), num = index, script = self, optimized_send_midi = optimized, resource_type = resource) for index in range(16)]
		self._sendA_controls = [MonoEncoderElement(mapping_feedback_delay = -1, msg_type = MIDI_CC_TYPE, channel = SENDA_CHANNEL, identifier = SENDA_CCS[index], name = 'SendA_Control_' + str(index), num = index, script = self, optimized_send_midi = optimized, resource_type = resource) for index in range(16)]
		self._sendB_controls = [MonoEncoderElement(mapping_feedback_delay = -1, msg_type = MIDI_CC_TYPE, channel = SENDB_CHANNEL, identifier = SENDB_CCS[index], name = 'SendB_Control_' + str(index), num = index, script = self, optimized_send_midi = optimized, resource_type = resource) for index in range(16)]
		self._sendC_controls = [MonoEncoderElement(mapping_feedback_delay = -1, msg_type = MIDI_CC_TYPE, channel = SENDC_CHANNEL, identifier = SENDC_CCS[index], name = 'SendC_Control_' + str(index), num = index, script = self, optimized_send_midi = optimized, resource_type = resource) for index in range(16)]
		self._sendD_controls = [MonoEncoderElement(mapping_feedback_delay = -1, msg_type = MIDI_CC_TYPE, channel = SENDD_CHANNEL, identifier = SENDD_CCS[index], name = 'SendD_Control_' + str(index), num = index, script = self, optimized_send_midi = optimized, resource_type = resource) for index in range(16)]
		self._sendE_controls = [MonoEncoderElement(mapping_feedback_delay = -1, msg_type = MIDI_CC_TYPE, channel = SENDE_CHANNEL, identifier = SENDE_CCS[index], name = 'SendE_Control_' + str(index), num = index, script = self, optimized_send_midi = optimized, resource_type = resource) for index in range(16)]
		self._sendF_controls = [MonoEncoderElement(mapping_feedback_delay = -1, msg_type = MIDI_CC_TYPE, channel = SENDF_CHANNEL, identifier = SENDF_CCS[index], name = 'SendF_Control_' + str(index), num = index, script = self, optimized_send_midi = optimized, resource_type = resource) for index in range(16)]
		self._sendG_controls = [MonoEncoderElement(mapping_feedback_delay = -1, msg_type = MIDI_CC_TYPE, channel = SENDG_CHANNEL, identifier = SENDG_CCS[index], name = 'SendG_Control_' + str(index), num = index, script = self, optimized_send_midi = optimized, resource_type = resource) for index in range(16)]
		self._sendH_controls = [MonoEncoderElement(mapping_feedback_delay = -1, msg_type = MIDI_CC_TYPE, channel = SENDH_CHANNEL, identifier = SENDH_CCS[index], name = 'SendH_Control_' + str(index), num = index, script = self, optimized_send_midi = optimized, resource_type = resource) for index in range(16)]
		self._masterVolume_control = MonoEncoderElement(mapping_feedback_delay = -1, msg_type = MIDI_CC_TYPE, channel = MASTER_VOLUME_CHANNEL, identifier = MASTER_VOLUME_CC, name = 'Master_Volume_Control', num = 0, script = self, optimized_send_midi = optimized, resource_type = resource)
		self._cueVolume_control = MonoEncoderElement(mapping_feedback_delay = -1, msg_type = MIDI_CC_TYPE, channel = CUE_VOLUME_CHANNEL, identifier = CUE_VOLUME_CC, name = 'Cue_Volume_Control', num = 0, script = self, optimized_send_midi = optimized, resource_type = resource)
		self._crossfader_control = MonoEncoderElement(mapping_feedback_delay = -1, msg_type = MIDI_CC_TYPE, channel = CROSSFADER_CHANNEL, identifier = CROSSFADER_CC, name = 'Crossfader_Control', num = 0, script = self, optimized_send_midi = optimized, resource_type = resource)

		# self._encoder_button = [MonoButtonElement(is_momentary = is_momentary, msg_type = MIDI_NOTE_TYPE, channel = CHANNEL, identifier = DS1_ENCODER_BUTTONS[index], name = 'EncoderButton_' + str(index), script = self, skin = self._skin, optimized_send_midi = optimized, resource_type = resource) for index in range(4)]

		self._volume_control_matrix = ButtonMatrixElement(name = 'VolumeControlMatrix', rows = [self._volume_controls])

		self._output_meter_level_controls = [MonoEncoderElement(mapping_feedback_delay = -1, msg_type = MIDI_CC_TYPE, channel = METER_CHANNEL, identifier = METER_CCS[index], name = 'Output_Meter_Level_Control_' + str(index), num = index, script = self, optimized_send_midi = False, resource_type = resource) for index in range(16)]
		self._output_meter_level_matrix = ButtonMatrixElement(name = 'OutputMeterLevelMatrix', rows = [self._output_meter_level_controls])

		self._output_meter_left_controls = [MonoEncoderElement(mapping_feedback_delay = -1, msg_type = MIDI_CC_TYPE, channel = METER_CHANNEL, identifier = METER_LEFT_CCS[index], name = 'Output_Meter_Left_Control_' + str(index), num = index, script = self, optimized_send_midi = False, resource_type = resource) for index in range(16)]
		self._output_meter_left_matrix = ButtonMatrixElement(name = 'OutputMeterLeftMatrix', rows = [self._output_meter_left_controls])

		self._output_meter_right_controls = [MonoEncoderElement(mapping_feedback_delay = -1, msg_type = MIDI_CC_TYPE, channel = METER_CHANNEL, identifier = METER_LEFT_CCS[index], name = 'Output_Meter_Right_Control_' + str(index), num = index, script = self, optimized_send_midi = False, resource_type = resource) for index in range(16)]
		self._output_meter_right_matrix = ButtonMatrixElement(name = 'OutputMeterRightMatrix', rows = [self._output_meter_right_controls])


	def _setup_background(self):
		self._background = BackgroundComponent(name = 'Background')
		self._background.layer = Layer(priority = 0, fader_matrix = self._fader_matrix,
													top_buttons = self._top_buttons,
													bottom_buttons = self._bottom_buttons,
													dial_matrix = self._dial_matrix,
													side_dial_matrix = self._side_dial_matrix,
													encoder_button_matrix = self._encoder_button_matrix,
													grid_matrix = self._grid_matrix)
		self._background.set_enabled(True)


	def _setup_autoarm(self):
		self._auto_arm = AutoArmComponent(name='Auto_Arm')
		self._auto_arm.can_auto_arm_track = self._can_auto_arm_track


	def _tracks_to_use(self):
		return self.song.visible_tracks + self.song.return_tracks


	def _setup_session_control(self):
		self._session_ring = SessionRingComponent(num_tracks = 16, num_scenes = 1, tracks_to_use = self._tracks_to_use)
		self._session_ring.set_enabled(True)

		self._session_navigation = SpecialSessionNavigationComponent(name = 'SessionNavigation', session_ring = self._session_ring)
		self._session_navigation._vertical_banking.scroll_up_button.color = 'Session.NavigationButtonOn'
		self._session_navigation._vertical_banking.scroll_down_button.color = 'Session.NavigationButtonOn'
		self._session_navigation._horizontal_banking.scroll_up_button.color = 'Session.NavigationButtonOn'
		self._session_navigation._horizontal_banking.scroll_down_button.color = 'Session.NavigationButtonOn'
		# self._session_navigation.layer = Layer(priority = 4, track_select_dial = ComboElement(control = self._encoder[1], modifier = [self._encoder_button[1]] ), up_button = self._grid[0][1], down_button = self._grid[0][2])
		self._session_navigation.set_enabled(False)

		self._session = SpecialSessionComponent(session_ring = self._session_ring, auto_name = True)
		# hasattr(self._session, '_enable_skinning') and self._session._enable_skinning()
		# self._session.layer = Layer(priority = 4, scene_launch_buttons = self._grid_matrix.submatrix[1:2, 1:2])
		# self._session.clips_layer = AddLayerMode(self._session, Layer(priority = 4, clip_launch_buttons = self._top_buttons, stop_track_clip_buttons = self._bottom_buttons))
		self._session.set_enabled(False)


	def _setup_mixer_control(self):

		self._mixer = MonoMixerComponent(name = 'Mixer', num_returns = 8, tracks_provider = self._session_ring, track_assigner = SimpleTrackAssigner(), invert_mute_feedback = True, auto_name = True, enable_skinning = True, channel_strip_component_type=MonoChannelStripComponent)
		self._mixer.master_strip().set_volume_control(self._masterVolume_control)
		self._mixer.set_prehear_volume_control(self._cueVolume_control)
		self._mixer.layer = Layer(volume_controls = self._volume_control_matrix,
			output_meter_level_controls = self._output_meter_level_matrix,
			output_meter_left_controls = self._output_meter_left_matrix,
			output_meter_right_controls = self._output_meter_right_matrix)
		# self._strip = [self._mixer.channel_strip(index) for index in range(16)]

		# self._mixer.selected_strip().layer = Layer(priority = 4, parameter_controls = self._selected_parameter_controls)
		# self._mixer.master_strip().layer = Layer(priority = 4, parameter_controls = self._side_dial_matrix.submatrix[:3, :])
		# self._mixer.main_layer = AddLayerMode(self._mixer, Layer(priority = 4, solo_buttons = self._bottom_buttons, mute_buttons = self._top_buttons))
		# self._mixer.select_layer = AddLayerMode(self._mixer, Layer(priority = 4, arm_buttons = self._bottom_buttons, track_select_buttons = self._top_buttons))
		# self.song.view.selected_track = self._mixer.channel_strip(0)._track
		self._mixer.set_enabled(False)


	def _setup_transport_control(self):
		self._transport = SpecialTransportComponent()
		self._transport.name = 'Transport'
		self._transport._record_toggle.view_transform = lambda value: 'Transport.RecordOn' if value else 'Transport.RecordOff'
		self._transport.layer = Layer(priority = 4, stop_button = self._grid[1][0], play_button = self._grid[0][0], record_button = self._grid[2][0])
		self._transport.set_enabled(True)


	def _setup_device_control(self):
		self._device = DeviceComponent(name = 'Device_Component', device_provider = self._device_provider, device_bank_registry = DeviceBankRegistry())

		self._device_navigator = DeviceNavigator(self._device_provider, self._mixer, self)
		self._device_navigator.name = 'Device_Navigator'


	def _setup_session_recording_component(self):
		self._clip_creator = ClipCreator()
		self._clip_creator.name = 'ClipCreator'
		self._recorder = SessionRecordingComponent(ViewControlComponent())
		self._recorder.set_enabled(True)
		self._recorder.layer = Layer(priority = 4, automation_button = self._grid[1][2], record_button  = self._grid[2][1],)


	# def _setup_m4l_interface(self):
	# 	self._m4l_interface = M4LInterfaceComponent(controls=self.controls, component_guard=self.component_guard, priority = 10)
	# 	self._m4l_interface.name = "M4LInterface"
	# 	self.get_control_names = self._m4l_interface.get_control_names
	# 	self.get_control = self._m4l_interface.get_control
	# 	self.grab_control = self._m4l_interface.grab_control
	# 	self.release_control = self._m4l_interface.release_control


	def _setup_translations(self):
		controls = []
		for control in self.controls:
			controls.append(control)
		self._translations = TranslationComponent(controls, 10)
		self._translations.name = 'TranslationComponent'
		self._translations.set_enabled(False)


	def _setup_main_modes(self):
		self._main_modes = ModesComponent(name = 'MainModes')
		self._main_modes.add_mode('Main', [self._mixer, self._session])
		self._main_modes.layer = Layer(priority = 4)
		self._main_modes.selected_mode = 'Main'
		self._main_modes.set_enabled(True)


	def _can_auto_arm_track(self, track):
		routing = track.current_input_routing
		return routing == 'Ext: All Ins' or routing == 'All Ins' or routing.startswith('YaeltexUniversal Input')
		#self._main_modes.selected_mode in ['Sends', 'Device'] and


#	a
