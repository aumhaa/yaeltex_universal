# by amounra 1225 : http://www.aumhaa.com
# version 2.3

from itertools import chain
from future.moves.itertools import zip_longest
import Live
from enum import IntEnum
from ableton.v2.base.event import listens, listens_group
from ableton.v2.control_surface.elements.physical_display import PhysicalDisplayElement
from ableton.v2.control_surface.elements.display_data_source import DisplayDataSource
from ableton.v2.control_surface.elements.sysex_element import *
from ableton.v2.control_surface import Component
from ableton.v2.control_surface.control_element import ControlElement, NotifyingControlElement
from ableton.v2.base import task
from ableton.v2.control_surface.components import DisplayingDeviceParameterComponent

from .debug import initialize_debug


LOCAL_DEBUG = True
debug = initialize_debug(local_debug = LOCAL_DEBUG)


# F0 79 74 78 01 01 04 [ParamType] [SourceIndex] [Data...] F7

# 240 121 116 120 1 1 4 [ParamType] [SourceIndex] [Data...] 247

YAELTEX_MESSAGE_HEADER = (240, 121, 116, 120, 1, 1, 4,)
YAELTEX_MESSAGE_TAIL = (247,)






class DisplayParameterType(IntEnum):
	PARAM_NONE = 0  # Reserved. Should not be used.
	
	# Track Parameters (Sent per track)
	PARAM_TRACK_NAME = 1  # String: The name of the track (e.g., "Lead Synth")
	PARAM_TRACK_VOLUME_VAL = 2  # u16: The raw MIDI value of the volume fader (0-16383 for high-res)  why u16???
	PARAM_TRACK_VOLUME_STR = 3  # String: The dB representation (e.g., "-6.1 dB")
	PARAM_TRACK_PAN_VAL = 4  # u16: The raw MIDI value of the pan control  why u16???
	PARAM_TRACK_PAN_STR = 5  # String: The pan representation (e.g., "24L", "C", "32R")
	PARAM_TRACK_MUTE_STATE = 6  # Bool (0/1): The mute button state (ON/OFF)
	PARAM_TRACK_SOLO_STATE = 7  # Bool (0/1): The solo/cue button state (ON/OFF)
	PARAM_TRACK_ARM_STATE = 8  # Bool (0/1): The record arm button state (ON/OFF)
	PARAM_TRACK_VU_LEVEL = 9  # u8 or u16: Peak VU meter level for the track  why u16???
	PARAM_TRACK_COLOR = 10  # 16 bit RGB565: The color of the track
	PARAM_TRACK_IS_SELECTED = 11  # Bool (0/1): If the track is currently selected
	
	# Track Sends (A-H)
	PARAM_TRACK_SEND_A_VAL = 12  # u16: Value for Send A  #why????
	PARAM_TRACK_SEND_B_VAL = 13
	PARAM_TRACK_SEND_C_VAL = 14
	PARAM_TRACK_SEND_D_VAL = 15
	PARAM_TRACK_SEND_E_VAL = 16
	PARAM_TRACK_SEND_F_VAL = 17
	PARAM_TRACK_SEND_G_VAL = 18
	PARAM_TRACK_SEND_H_VAL = 19
	
	# Device Parameters (For the selected device on a track)
	PARAM_DEVICE_NAME = 20  # String: Name of the currently selected device (e.g., "Auto Filter")
	PARAM_DEVICE_ON_OFF_STATE = 21  # Bool (0/1): Whether the device is active
	PARAM_DEVICE_BANK_NAME = 22  # String: Name of the current parameter bank (e.g., "Filter", "Macros")
	
	# Device Parameters 1-8 (for the current bank)
	PARAM_DEVICE_PARAM_1_NAME = 23  # String: Name of the 1st parameter in the bank (e.g., "Frequency")
	PARAM_DEVICE_PARAM_1_VAL = 24  # u16: Raw value of the parameter #why????
	PARAM_DEVICE_PARAM_1_STR = 25  # String: Formatted value (e.g., "1.2 kHz", "50%")
	PARAM_DEVICE_PARAM_2_NAME = 26
	PARAM_DEVICE_PARAM_2_VAL = 27
	PARAM_DEVICE_PARAM_2_STR = 28
	PARAM_DEVICE_PARAM_3_NAME = 29
	PARAM_DEVICE_PARAM_3_VAL = 30
	PARAM_DEVICE_PARAM_3_STR = 31
	PARAM_DEVICE_PARAM_4_NAME = 32
	PARAM_DEVICE_PARAM_4_VAL = 33
	PARAM_DEVICE_PARAM_4_STR = 34
	PARAM_DEVICE_PARAM_5_NAME = 35
	PARAM_DEVICE_PARAM_5_VAL = 36
	PARAM_DEVICE_PARAM_5_STR = 37
	PARAM_DEVICE_PARAM_6_NAME = 38
	PARAM_DEVICE_PARAM_6_VAL = 39
	PARAM_DEVICE_PARAM_6_STR = 40
	PARAM_DEVICE_PARAM_7_NAME = 41
	PARAM_DEVICE_PARAM_7_VAL = 42
	PARAM_DEVICE_PARAM_7_STR = 43
	PARAM_DEVICE_PARAM_8_NAME = 44
	PARAM_DEVICE_PARAM_8_VAL = 45
	PARAM_DEVICE_PARAM_8_STR = 46
	
	# Session / Clip Parameters (Sent per clip slot)
	PARAM_CLIP_STATE = 47  # Enum: 0:Empty, 1:HasClip, 2:Playing, 3:Recording, 4:Triggered
	PARAM_CLIP_NAME = 48  # String: Name of the clip in the slot
	PARAM_CLIP_COLOR = 49  # 16 bit RGB565: The color of the clip
	
	# Global & Transport Parameters (System-wide)
	PARAM_TRANSPORT_PLAY_STATE = 50  # Bool (0/1): If transport is playing
	PARAM_TRANSPORT_REC_STATE = 51  # Bool (0/1): If global recording is enabled
	PARAM_METRONOME_STATE = 52  # Bool (0/1): If the metronome is enabled
	PARAM_OVERDUB_STATE = 53  # Bool (0/1): If overdub is enabled
	PARAM_LOOP_STATE = 54  # Bool (0/1): If the loop brace is active
	PARAM_TEMPO_VAL = 55  # Float: The exact BPM value (e.g., 120.50)  #why would you possibly need this?
	PARAM_TEMPO_STR = 56  # String: Formatted BPM string (e.g., "120.50")
	PARAM_CROSSFADER_POS = 57  # u16: Raw value of the crossfader
	PARAM_MASTER_VOLUME_VAL = 58  # u16: Raw value of the master fader
	PARAM_MASTER_VOLUME_STR = 59  # String: dB representation of the master fader
	PARAM_MASTER_VU_LEVEL = 60  # u8 or u16: Peak VU meter level for the master track
	
	# Special Utility Parameters
	PARAM_FULL_VIEW_REFRESH = 61  # Special command from script to force a full redraw of a view's data


DisplayParameterTypeDict = {
	'PARAM_NONE': 0,  # Reserved. Should not be used.
	
	# Track Parameters (Sent per track)
	'PARAM_TRACK_NAME': 1,  # String: The name of the track (e.g., "Lead Synth")
	'PARAM_TRACK_VOLUME_VAL': 2,  # u16: The raw MIDI value of the volume fader (0-16383 for high-res)
	'PARAM_TRACK_VOLUME_STR': 3,  # String: The dB representation (e.g., "-6.1 dB")
	'PARAM_TRACK_PAN_VAL': 4,  # u16: The raw MIDI value of the pan control
	'PARAM_TRACK_PAN_STR': 5,  # String: The pan representation (e.g., "24L", "C", "32R")
	'PARAM_TRACK_MUTE_STATE': 6,  # Bool (0/1): The mute button state (ON/OFF)
	'PARAM_TRACK_SOLO_STATE': 7,  # Bool (0/1): The solo/cue button state (ON/OFF)
	'PARAM_TRACK_ARM_STATE': 8,  # Bool (0/1): The record arm button state (ON/OFF)
	'PARAM_TRACK_VU_LEVEL': 9,  # u8 or u16: Peak VU meter level for the track
	'PARAM_TRACK_COLOR': 10,  # 16 bit RGB565: The color of the track
	'PARAM_TRACK_IS_SELECTED': 11,  # Bool (0/1): If the track is currently selected
	
	# Track Sends (A-H)
	'PARAM_TRACK_SEND_A_VAL': 12,  # u16: Value for Send A
	'PARAM_TRACK_SEND_B_VAL': 13,
	'PARAM_TRACK_SEND_C_VAL': 14,
	'PARAM_TRACK_SEND_D_VAL': 15,
	'PARAM_TRACK_SEND_E_VAL': 16,
	'PARAM_TRACK_SEND_F_VAL': 17,
	'PARAM_TRACK_SEND_G_VAL': 18,
	'PARAM_TRACK_SEND_H_VAL': 19,
	
	# Device Parameters (For the selected device on a track)
	'PARAM_DEVICE_NAME': 20,  # String: Name of the currently selected device (e.g., "Auto Filter")
	'PARAM_DEVICE_ON_OFF_STATE': 21,  # Bool (0/1): Whether the device is active
	'PARAM_DEVICE_BANK_NAME': 22,  # String: Name of the current parameter bank (e.g., "Filter", "Macros")
	
	# Device Parameters 1-8 (for the current bank)
	'PARAM_DEVICE_PARAM_1_NAME': 23,  # String: Name of the 1st parameter in the bank (e.g., "Frequency")
	'PARAM_DEVICE_PARAM_1_VAL': 24,  # u16: Raw value of the parameter
	'PARAM_DEVICE_PARAM_1_STR': 25,  # String: Formatted value (e.g., "1.2 kHz", "50%")
	'PARAM_DEVICE_PARAM_2_NAME': 26,
	'PARAM_DEVICE_PARAM_2_VAL': 27,
	'PARAM_DEVICE_PARAM_2_STR': 28,
	'PARAM_DEVICE_PARAM_3_NAME': 29,
	'PARAM_DEVICE_PARAM_3_VAL': 30,
	'PARAM_DEVICE_PARAM_3_STR': 31,
	'PARAM_DEVICE_PARAM_4_NAME': 32,
	'PARAM_DEVICE_PARAM_4_VAL': 33,
	'PARAM_DEVICE_PARAM_4_STR': 34,
	'PARAM_DEVICE_PARAM_5_NAME': 35,
	'PARAM_DEVICE_PARAM_5_VAL': 36,
	'PARAM_DEVICE_PARAM_5_STR': 37,
	'PARAM_DEVICE_PARAM_6_NAME': 38,
	'PARAM_DEVICE_PARAM_6_VAL': 39,
	'PARAM_DEVICE_PARAM_6_STR': 40,
	'PARAM_DEVICE_PARAM_7_NAME': 41,
	'PARAM_DEVICE_PARAM_7_VAL': 42,
	'PARAM_DEVICE_PARAM_7_STR': 43,
	'PARAM_DEVICE_PARAM_8_NAME': 44,
	'PARAM_DEVICE_PARAM_8_VAL': 45,
	'PARAM_DEVICE_PARAM_8_STR': 46,
	
	# Session / Clip Parameters (Sent per clip slot)
	'PARAM_CLIP_STATE': 47,  # Enum: 0:Empty, 1:HasClip, 2:Playing, 3:Recording, 4:Triggered
	'PARAM_CLIP_NAME': 48,  # String: Name of the clip in the slot
	'PARAM_CLIP_COLOR': 49,  # 16 bit RGB565: The color of the clip
	
	# Global & Transport Parameters (System-wide)
	'PARAM_TRANSPORT_PLAY_STATE': 50,  # Bool (0/1): If transport is playing
	'PARAM_TRANSPORT_REC_STATE': 51,  # Bool (0/1): If global recording is enabled
	'PARAM_METRONOME_STATE': 52,  # Bool (0/1): If the metronome is enabled
	'PARAM_OVERDUB_STATE': 53,  # Bool (0/1): If overdub is enabled
	'PARAM_LOOP_STATE': 54,  # Bool (0/1): If the loop brace is active
	'PARAM_TEMPO_VAL': 55,  # Float: The exact BPM value (e.g., 120.50)
	'PARAM_TEMPO_STR': 56,  # String: Formatted BPM string (e.g., "120.50")
	'PARAM_CROSSFADER_POS': 57,  # u16: Raw value of the crossfader
	'PARAM_MASTER_VOLUME_VAL': 58,  # u16: Raw value of the master fader
	'PARAM_MASTER_VOLUME_STR': 59,  # String: dB representation of the master fader
	'PARAM_MASTER_VU_LEVEL': 60,  # u8 or u16: Peak VU meter level for the master track
	
	# Special Utility Parameters
	'PARAM_FULL_VIEW_REFRESH': 61  # Special command from script to force a full redraw of a view's data
}

TYPES = DisplayParameterType
DEVICE_PARAM_NAME_TYPES = (TYPES.PARAM_DEVICE_PARAM_1_NAME, TYPES.PARAM_DEVICE_PARAM_2_NAME, TYPES.PARAM_DEVICE_PARAM_3_NAME, TYPES.PARAM_DEVICE_PARAM_4_NAME, TYPES.PARAM_DEVICE_PARAM_5_NAME, TYPES.PARAM_DEVICE_PARAM_6_NAME, TYPES.PARAM_DEVICE_PARAM_7_NAME, TYPES.PARAM_DEVICE_PARAM_8_NAME)
DEVICE_PARAM_STR_TYPES = (TYPES.PARAM_DEVICE_PARAM_1_STR, TYPES.PARAM_DEVICE_PARAM_2_STR, TYPES.PARAM_DEVICE_PARAM_3_STR, TYPES.PARAM_DEVICE_PARAM_4_STR, TYPES.PARAM_DEVICE_PARAM_5_STR, TYPES.PARAM_DEVICE_PARAM_6_STR, TYPES.PARAM_DEVICE_PARAM_7_STR, TYPES.PARAM_DEVICE_PARAM_8_STR)
DEVICE_PARAM_VAL_TYPES = (TYPES.PARAM_DEVICE_PARAM_1_VAL, TYPES.PARAM_DEVICE_PARAM_2_VAL, TYPES.PARAM_DEVICE_PARAM_3_VAL, TYPES.PARAM_DEVICE_PARAM_4_VAL, TYPES.PARAM_DEVICE_PARAM_5_VAL, TYPES.PARAM_DEVICE_PARAM_6_VAL, TYPES.PARAM_DEVICE_PARAM_7_VAL, TYPES.PARAM_DEVICE_PARAM_8_VAL)	
SEND_PARAM_VAL_TYPES = (TYPES.PARAM_TRACK_SEND_A_VAL, TYPES.PARAM_TRACK_SEND_B_VAL, TYPES.PARAM_TRACK_SEND_C_VAL, TYPES.PARAM_TRACK_SEND_D_VAL, TYPES.PARAM_TRACK_SEND_E_VAL, TYPES.PARAM_TRACK_SEND_F_VAL, TYPES.PARAM_TRACK_SEND_G_VAL, TYPES.PARAM_TRACK_SEND_H_VAL)	
class ValueDisplayDataSource(object):

	def __init__(self, value=0, *a, **k):
		(super(ValueDisplayDataSource, self).__init__)(*a, **k)
		self._value = value
		self._update_callback = None
		self._in_update = False

	def set_update_callback(self, update_callback):
		self._update_callback = update_callback
		if update_callback:
			self.update()

	def set_value(self, new_value):
		if self._value != new_value:
			self._value = new_value
			self.update()

	def clear(self):
		self.set_value(0)

	def update(self):
		self._in_update = True
		if self._update_callback is not None:
			self._update_callback()
		self._in_update = False

	def display_string(self):
		return self._value



class SpecialDisplayingDeviceParameterComponent(DisplayingDeviceParameterComponent):

	def __init__(self, *a, **k):
		self._parameter_value_data_sources = list(map(ValueDisplayDataSource, (0, 0, 0, 0, 0, 0, 0, 0)))
		(super(SpecialDisplayingDeviceParameterComponent, self).__init__)(*a, **k)

	def _connect_parameters(self):
		parameters = self._parameter_provider.parameters[:self.controls.control_count]
		for control, parameter_info in zip_longest(self.controls, parameters):
			parameter = parameter_info.parameter if parameter_info else None
			control.mapped_parameter = parameter

	def _update_parameter_values(self):
		if self.is_enabled():
			for parameter, data_source in zip_longest(self.parameters, self._parameter_value_data_sources):
				value_string = self.parameter_to_string(parameter)
				if data_source:
					data_source.set_display_string(value_string)
					

class SubscriptionEntry(object):
	def __init__(self, id = '', display_object = None, *a, **k):
		self.id = id
		self.display_object = display_object
		self.subscribers = []
		super(SubscriptionEntry, self).__init__(*a, **k)
	
	def add_subscriber(self, subscriber_id):
		if subscriber_id not in self.subscribers:
			self.subscribers.append(subscriber_id)
			self.set_enabled(True)

	def remove_subscriber(self, subscriber_id):
		if subscriber_id in self.subscribers:
			self.subscribers.remove(subscriber_id)
		if len(self.subscribers) == 0:
			self.set_enabled(False)

	def set_enabled(self, enabled):
		if self.display_object:
			self.display_object.set_block_messages(not enabled)


class YaeltexDisplayComponent(Component):
	def __init__(self, mixer = None, device = None, device_parameters = None, *a, **k):
		self._mixer = mixer
		self._device = device
		self._device_parameters = device_parameters
		super(YaeltexDisplayComponent, self).__init__(*a, **k)
		# self._parameter_displays = []
		self._parameter_subscriptions = []
		self._last_subscription_list = {}

		# here we need a single instance of parameter_displays, or actually.....we don't need anything special.  there's no need for an intermediary component. 
		# we'll need a hash list to take care of whether or not a subscription should be EOL'd. 
		# really this is way more convoluted than it needs to be. The controller should only be sending subscriptions/unsubscriptions based only on the parameter(s) it wants to receive, and dealing with the hash on its end since all of the extra data its sending is arbitrary to the concerns of the scirpt side logic.  

		"""#we're going to store our subscriptions in a dictionary, with the format:
		{id: unique, based on param# and the speciifcs of the param request.  We'll use this to hash for un/subscribe,
		object:  class dependent transmission object (e.g. YaeltexTextDisplayElement, YaeltexValueDisplayElement),
		subscriptions:  [] list of all entities still alive asking for the subscription.}
		"""

		# for index in range(8):
		# 	self._parameter_displays.append(YaeltexParameterDisplayComponent(index = index, mixer = self._mixer, device_parameters = self._device_parameters))

	def handle_subscription_message(self, instance, view, subscriptions):
		# debug('handling subscription message for instance:', instance, 'view:', view, 'subscriptions:', subscriptions)
		# display = self._parameter_displays[instance] if instance < len(self._parameter_displays) else None
		# if display:
		# 	display.subscribe(subscriptions)

		# here we need to actually check to see if we're going to need to actually remove something before we do it and re-add, otherwise terribly inefficient. 
		# apparently we need to keep a view hash as well so that we can store the last subscription call from the controller there and then compare it with the current one to see what we actually need to remove. 
		removed_subscriptions = []
		new_subscriptions = []

		unique_id = str(instance)+'_'+str(view)
		last_subscriptions = self._last_subscription_list.get(unique_id, None)
		if not last_subscriptions is None and len(last_subscriptions) > 0:
			# dif last subscriptions and current subscriptions, remove only what is necessary
			removed_subscriptions = [sub for sub in last_subscriptions if sub not in subscriptions]
			new_subscriptions = [sub for sub in subscriptions if sub not in last_subscriptions]
		else:
			new_subscriptions = subscriptions
		
		for sub in removed_subscriptions:
			self.remove_subscription_from_logical_display(unique_id, sub)
		for sub in new_subscriptions:
			self.add_subscription_for_logical_display(unique_id, sub)
		self._last_subscription_list[unique_id] = subscriptions

		


		# self.remove_subscriptions_from_logical_display(instance, view, subscriptions)
		# for sub in subscriptions:
		# 	if self.should_subscribe(instance, view):

	def remove_subscription_from_logical_display(self, unique_id, subscription):
		if len(subscription) != 2:
			return
		subscription_id = subscription[0],'_',subscription[1]
		if subscription_id in self._parameter_subscriptions:
			self._parameter_subscriptions.remove_subscriber(unique_id)


	def add_subscription_for_logical_display(self, unique_id, subscription):
		''' most of this should work.  2.3.26 I had implemented as much as I could with a faulty controller, but can't really test much due to the tediousness
		that is required for reboots of the controller, and the fact that that controller only functions partially or intermittently.
		Send knobs send nothing.
		Controller becomes unresponsive after the first connect request from the script.
		Some subscriptions appear to be wrong, for instance the device parameter names do not match their linked controls (this might be script side, but I lost the desire to debug at this point)
		Everything listed was tested as roughly working except for send values and clip info, which have not been implemented in their corresponding modules yet.'''

		
		if len(subscription) != 2:
			return
		debug('Adding subscription for logical display:', unique_id, ' subscription:', subscription)
		subscription_id = subscription[0],'_',subscription[1]
		if subscription_id in self._parameter_subscriptions:
			self._parameter_subscriptions.add_subscriber(unique_id)
			debug('Added subscriber for logical display:', unique_id, ' subscription:', subscription)
			return
		else:
			subscription_obj = None
			param_type = subscription[0]
			source_index = subscription[1]
			Type = TYPES(param_type)
			# debug('Creating subscription to parameter type:', Type)

			if Type == TYPES.PARAM_TRACK_NAME:
				# case TYPES.PARAM_TRACK_NAME:
				if(source_index < 1 or source_index > len(self._mixer._channel_strips)):
					debug('Invalid source index for track name subscription:', source_index)
					return
				debug('Creating subscription to track name:', source_index)
				display = ParameterTextDisplayElement(param_type, source_index)
				data_source = self._mixer.channel_strip(source_index-1)._track_name_data_source
				display.segment(0).set_data_source(data_source)
				subscription_obj = SubscriptionEntry(id = subscription_id, display_object = display)
				debug('Created subscription to track name:', source_index)	

			elif Type == TYPES.PARAM_TRACK_VOLUME_VAL:
				if(source_index < 1 or source_index > len(self._mixer._channel_strips)):
					debug('Invalid source index for track volume value subscription:', source_index)
					return
				debug('Creating subscription to track volume value:', source_index)
				display = ParameterValueDisplayElement(param_type, source_index)
				display.set_parameter(self._mixer.channel_strip(source_index-1)._track.mixer_device.volume)
				subscription_obj = SubscriptionEntry(id = subscription_id, display_object = display)
				debug('Created subscription to track volume value:', source_index)
	
			elif Type == TYPES.PARAM_TRACK_COLOR:
				if(source_index < 1 or source_index > len(self._mixer._channel_strips)):
					debug('Invalid source index for track color subscription:', source_index)
					return
				debug('Creating subscription to track color:', source_index)
				display = ColorDisplayElement(param_type, source_index)
				display.set_parameter(self._mixer.channel_strip(source_index-1))
				subscription_obj = SubscriptionEntry(id = subscription_id, display_object = display)
				debug('Created subscription to track color:', source_index)

			elif Type == TYPES.PARAM_TRACK_VU_LEVEL:
				if(source_index < 1 or source_index > len(self._mixer._channel_strips)):
					debug('Invalid source index for track VU level subscription:', source_index)
					return
				debug('Creating subscription to track VU level:', source_index)
				display = VUDisplayElement(param_type, source_index)
				display.set_parameter(self._mixer._channel_strips[source_index-1])
				subscription_obj = SubscriptionEntry(id = subscription_id, display_object = display)
				debug('Created subscription to track VU level:', source_index)

			elif Type in SEND_PARAM_VAL_TYPES:
				debug('Creating subscription to track send value:', source_index)
				# send_index = Type - TYPES.PARAM_TRACK_SEND_A_VAL
				# display = ValueDisplayElement(param_type, source_index)
				# display.set_parameter(self._mixer.channel_strip(source_index).sends[send_index])
				# subscription_obj = SubscriptionEntry(id = subscription_id, display_object = display)
				# debug('Created subscription to track send value:', source_index)

			# elif Type == TYPES.PARAM_TRACK_COLOR:
			# 	debug('Creating subscription to track color:', source_index)
	
			elif Type in DEVICE_PARAM_NAME_TYPES:
				debug('Creating subscription to device parameter name:', source_index)
				display = ParameterTextDisplayElement(param_type, source_index)
				data_source = self._device_parameters._parameter_name_data_sources[source_index-1]
				display.segment(0).set_data_source(data_source)
				subscription_obj = SubscriptionEntry(id = subscription_id, display_object = display)
				debug('Created subscription to device parameter name:', source_index)	

			elif Type in DEVICE_PARAM_STR_TYPES:
				debug('Creating subscription to device parameter name:', source_index)
				display = ParameterTextDisplayElement(param_type, source_index)
				data_source = self._device_parameters._parameter_value_data_sources[source_index-1]
				display.segment(0).set_data_source(data_source)
				subscription_obj = SubscriptionEntry(id = subscription_id, display_object = display)	
				debug('Created subscription to device parameter string:', source_index)

			elif Type in DEVICE_PARAM_VAL_TYPES:
				debug('Creating subscription to device parameter value:', source_index)
				display = ParameterValueDisplayElement(param_type, source_index)
				display.set_parameter(self._device.parameters[source_index-1].parameter)
				display._on_parameters_changed.subject = self._device
				subscription_obj = SubscriptionEntry(id = subscription_id, display_object = display)
				# display.segment(0).set_data_source(data_source)
				debug('Created subscription to device parameter value:', source_index)

			elif Type == TYPES.PARAM_CLIP_STATE:
				debug('Creating subscription to clip state:', source_index)
				display = ParameterValueDisplayElement(param_type, source_index)
				# clip_slot = self._mixer.channel_strip(source_index-1)._clip_slot


			elif Type == TYPES.PARAM_CLIP_NAME:
				debug('Creating subscription to clip name:', source_index)
				# display = ParameterTextDisplayElement(param_type, source_index)
				# clip_slot = self._mixer.channel_strip(source_index)._clip_slot
				# data_source = clip_slot._clip_name_data_source
				# display.segment(0).set_data_source(data_source)
				# subscription_obj = SubscriptionEntry(id = subscription_id, display_object = display)
				# debug('Created subscription to clip name:', source_index)

			elif Type == TYPES.PARAM_CLIP_COLOR:
				debug('Creating subscription to clip color:', source_index)	


			if not subscription_obj is None:
				self._parameter_subscriptions.append(subscription_obj)
				subscription_obj.add_subscriber(unique_id)
				debug('Appended subscription object for logical display:', subscription_obj)

	def should_subscribe(self):
		pass


class YaeltexTextDisplayElement(PhysicalDisplayElement):

	def __init__(self, param_type = 0, source_index = 0, *a, **k):
		self._message_param_type = param_type
		self._message_source_index = source_index
		super(YaeltexTextDisplayElement, self).__init__(width_in_chars = 8, num_segments = 1, *a, **k)
		self.set_message_parts(YAELTEX_MESSAGE_HEADER + (self._message_param_type, self._message_source_index), YAELTEX_MESSAGE_TAIL)

class YaeltexValueDisplayElement(NotifyingControlElement):

	def __init__(self, param_type = 0, source_index = 0, *a, **k):
		self._message_param_type = param_type
		self._message_source_index = source_index
		super(YaeltexValueDisplayElement, self).__init__(*a, **k)
		self._parameter = None
		self._message_header = None
		self._message_tail = None
		self._message_clear_all = None
		self._message_to_send = None
		self._last_sent_message = None
		self._block_messages = False
		self.set_message_parts(YAELTEX_MESSAGE_HEADER + (self._message_param_type, self._message_source_index), YAELTEX_MESSAGE_TAIL)
		self._send_message_task = self._tasks.add(task.run(self._send_message))
		self._send_message_task.kill()

	def set_parameter(self, parameter):
		self._parameter = parameter
		# debug('Setting parameter:', parameter)
		self._on_parameter_value_changed.subject = parameter
		self._on_parameter_value_changed()

	@property
	def parameter(self):
		return self._parameter

	@property
	def parameter_value(self):
		if self._parameter is not None:
			# return int(self._parameter.value * 127)
			return self._parameter.value
		return 0

	@listens('value')
	def _on_parameter_value_changed(self):
		self._request_send_message()


	@listens('parameters')
	def _on_parameters_changed(self):
		debug('Parameters changed')
		self.update_observed_parameter()

	def update_observed_parameter(self):
		pass


	def set_message_parts(self, header, tail):
		self._message_header = header
		self._message_tail = tail

	@property
	def message_header(self):
		return self._message_header

	@property
	def message_tail(self):
		return self._message_tail

	def set_clear_all_message(self, message):
		self._message_clear_all = message

	def set_translation_table(self, translation_table):
		self._translation_table = translation_table

	def set_block_messages(self, block):
		if block != self._block_messages:
			self._block_messages = block
		self.clear_send_cache()

	def display_message(self, value):
		if not self._block_messages:
			# message = adjust_string(message, self._width)
			self._message_to_send = self._message_header + tuple(self._translate_value(value)) + self._message_tail
			self._request_send_message()

	def update(self):
		# if len(self._logical_segments) > 0:
		if not self._block_messages:
			self._message_to_send = None
			self._request_send_message()

	def clear_send_cache(self):
		self._last_sent_message = None
		self._request_send_message()

	def reset(self):
		# super(YaeltexValueDisplayElement, self).reset()
		if not self._block_messages:
			if self._message_clear_all is not None:
				self._message_to_send = self._message_clear_all
			else:
				self._message_to_send = self._message_header + (0,) + self._message_tail
			self._request_send_message()

	def send_midi(self, midi_bytes):
		if midi_bytes != self._last_sent_message:
			ControlElement.send_midi(self, midi_bytes)
			self._last_sent_message = midi_bytes

	def _request_send_message(self):
		self._send_message_task.restart()

	def _send_message(self):
		if not self._block_messages:
			self._message_to_send = self._build_message()
			self.send_midi(self._message_to_send)

	def _translate_value(self, value):
		pass

	def _build_message(self):
		msg = self._message_header + (self._translate_value(self.parameter_value),) + self._message_tail
		# debug('Built message:', msg)
		return msg


class ParameterTextDisplayElement(YaeltexTextDisplayElement):

	def __init__(self, *a, **k	):
		super(ParameterTextDisplayElement, self).__init__(*a, **k)

class ParameterValueDisplayElement(YaeltexValueDisplayElement):

	def __init__(self, *a, **k):
		super(ParameterValueDisplayElement, self).__init__(*a, **k)

	def _translate_value(self, value): 
		# debug('Translating value:', self._parameter, value)
		if self.parameter is not None:
			return int(value * 127)
		return 0

class BooleanDisplayElement(YaeltexValueDisplayElement):

	def __init__(self, *a, **k):
		super(BooleanDisplayElement, self).__init__(*a, **k)

	def _translate_value(self, value):
		if self._parameter is not None:
			return int(bool(value))
		return 0

class ColorDisplayElement(YaeltexValueDisplayElement):

	def __init__(self, *a, **k):
		super(ColorDisplayElement, self).__init__(*a, **k)

	def _translate_value(self, value):
		if self._parameter is not None:
			return value
		return 0

	@listens('color')
	def _on_color_changed(self):
		debug('color changed')
		self._request_send_message()

	def set_parameter(self, parameter):
		self._parameter = parameter
		debug('Setting parameter:', parameter)
		self._on_color_changed.subject = parameter
		self._on_color_changed()

	@property
	def parameter_value(self):
		if self._parameter is not None:
			# return int(self._parameter.value * 127)
			# debug('Getting summed output meter level:', self._parameter.summed_output_meter_level)
			return self._parameter.color
		return 0

class VUDisplayElement(YaeltexValueDisplayElement):

	def __init__(self, *a, **k):
		super(VUDisplayElement, self).__init__(*a, **k)

	def _translate_value(self, value):
		if self._parameter is not None:
			# debug('Translating VU value:', value)
			return int(value * 127)
		return 0

	
	def set_parameter(self, parameter):
		self._parameter = parameter
		debug('Setting parameter:', parameter)
		self._on_summed_output_meter_level_changed.subject = parameter
		self._on_summed_output_meter_level_changed()

	@listens('summed_output_meter_level')
	def _on_summed_output_meter_level_changed(self):
		# debug('VU level changed')
		self._request_send_message()

	@property
	def parameter_value(self):
		if self._parameter is not None:
			# return int(self._parameter.value * 127)
			# debug('Getting summed output meter level:', self._parameter.summed_output_meter_level)
			return self._parameter.summed_output_meter_level
		return 0


class ClipStateDisplayElement(YaeltexValueDisplayElement):

	def __init__(self, *a, **k):
		super(ClipStateDisplayElement, self).__init__(*a, **k)

	def _translate_value(self, value):
		if self._parameter is not None:
			return int(value)
		return 0




#a




