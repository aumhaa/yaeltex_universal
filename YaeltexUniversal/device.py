# by amounra 1125 : http://www.aumhaa.com
# version 2.3


import Live
import math
import sys
import logging

#from ableton.v2.control_surface.components import DeviceComponent as DeviceComponentBase
#from _Generic.Devices import best_of_parameter_bank, device_parameters_to_map, number_of_parameter_banks, parameter_bank_names, parameter_banks
from ableton.v2.base import depends, listens, listens_group, liveobj_valid, EventObject, flatten
from ableton.v2.control_surface.component import Component
from ableton.v2.control_surface.control import ButtonControl
from ableton.v2.control_surface.elements import DisplayDataSource
from _Generic.Devices import *
from .Map import *
from .debug import initialize_debug
logger = logging.getLogger(__name__)
debug = initialize_debug()

def best_of_parameter_bank(device, device_bob_dict=DEVICE_BOB_DICT):
	if device:
		if device.class_name in device_bob_dict:
			bobs = device_bob_dict[device.class_name]
			return list(map(partial(get_parameter_by_name, device), bobs[0]))
	if device.class_name in MAX_DEVICES:
		try:
			parameter_indices = device.get_bank_parameters(-1)
			return [device.parameters[i] if i != -1 else None for i in parameter_indices]
		except:
			return []

		return device.parameters[1:17]

def create_device_bank(device, banking_info):
	bank = None
	if liveobj_valid(device):
		if banking_info.has_bank_count(device):
			bank_class = MaxDeviceParameterBank
		elif banking_info.device_bank_definition(device) is not None:
			# bank_class = DescribedDeviceParameterBank
			bank_class = LargeDescribedDeviceParameterBank
		else:
			bank_class = DeviceParameterBank
		bank = bank_class(device=device, size=16, banking_info=banking_info)
	return bank


def xstr(s):
	if s is None:
		return ''
	else:
		return str(s)


def special_number_of_parameter_banks(device, device_dict = DEVICE_DICT):
	""" Determine the amount of parameter banks the given device has """
	if device != None:
		if device.class_name in list(device_dict.keys()):
			device_bank = device_dict[device.class_name]
			return math.floor(len(device_bank)/2) + (1 if len(device_bank)%2 else 0)
		else:
			if device.class_name in MAX_DEVICES:
				try:
					banks = device.get_bank_count()
				except:
					banks = 0
				if banks != 0:
					return banks
			param_count = len(device.parameters[1:])
			return math.floor(param_count / 16 + (1 if param_count % 16 else 0))
	return 0


def special_parameter_bank_names(device, bank_name_dict = BANK_NAME_DICT):
	if device != None:
		if device.class_name in list(bank_name_dict.keys()):
			ret = group(bank_name_dict[device.class_name], 2)
			ret1 = [[i for i in bank_names if not i is None] for bank_names in ret]
			return [' - '.join(i) for i in ret1]
		banks = special_number_of_parameter_banks(device)
		def _default_bank_name(bank_index):
			return 'Bank ' + str(bank_index + 1)

		if device.class_name in MAX_DEVICES and banks != 0:
			def _is_ascii(c):
				return ord(c) < 128

			def _bank_name(bank_index):
				try:
					name = device.get_bank_name(bank_index)
				except:
					name = None
				if name:
					return str(list(filter(_is_ascii, name)))
				else:
					return _default_bank_name(bank_index)

			return list(map(_bank_name, list(range(0, banks))))
		else:
			return list(map(_default_bank_name, list(range(0, banks))))
	return []


def special_parameter_banks(device, device_dict = DEVICE_DICT):
	""" Determine the parameters to use for a device """
	if device != None:
		if device.class_name == 'LegacyModDeviceProxy':
			return group(device_parameters_to_map(device), 16)
		elif device.class_name in list(device_dict.keys()):
			def names_to_params(bank):
				return list(map(partial(get_parameter_by_name, device), bank))

			return group([i for i in flatten(list(map(names_to_params, device_dict[device.class_name])))], 16)
		else:
			if device.class_name in MAX_DEVICES:
				try:
					banks = device.get_bank_count()
				except:
					banks = 0
				if banks != 0:
					def _bank_parameters(bank_index):
						try:
							parameter_indices = device.get_bank_parameters(bank_index)
						except:
							parameter_indices = []
						if len(parameter_indices) != 16:
							return [ None for i in range(0, 16) ]
						else:
							return [ (device.parameters[i] if i != -1 else None) for i in parameter_indices ]

					return list(map(_bank_parameters, list(range(0, banks))))
			return group(device_parameters_to_map(device), 16)
	return []


class DeviceBankRegistry(EventObject):
	__events__ = ('device_bank',)

	def __init__(self, *a, **k):
		super(DeviceBankRegistry, self).__init__(*a, **k)
		self._device_bank_registry = {}
		self._device_bank_listeners = []

	def compact_registry(self):
		newreg = dict([k__ for k__ in list(self._device_bank_registry.items()) if k__[0] != None])
		self._device_bank_registry = newreg

	def set_device_bank(self, device, bank):
		key = self._find_device_bank_key(device) or device
		old = self._device_bank_registry[key] if key in self._device_bank_registry else 0
		if old != bank:
			self._device_bank_registry[key] = bank
			self.notify_device_bank(device, bank)

	def get_device_bank(self, device):
		return self._device_bank_registry.get(self._find_device_bank_key(device), 0)

	def _find_device_bank_key(self, device):
		for k in self._device_bank_registry.keys():
			if k == device:
				return k



class DeviceComponentBase(Component):
	""" Class representing a device in Live """

	add_macro_button = ButtonControl(color = "Device.AddVariation")
	delete_macro_button = ButtonControl(color = "Device.DeleteVariation")
	next_macro_button = ButtonControl(color = "Device.VariationNavOn")
	prev_macro_button = ButtonControl(color = "Device.VariationNavOn")
	randomize_macro_button = ButtonControl(color = "Device.RandomizeControls")

	@depends(device_bank_registry=None)
	@depends(device_provider=None)
	def __init__(self, device_provider = None, device_bank_registry = None, *a, **k):
		assert device_bank_registry is not None
		super(DeviceComponentBase, self).__init__(*a, **k)
		self._device_bank_registry = device_bank_registry
		self._device_provider = device_provider
		self._parameter_controls = None
		self._bank_up_button = None
		self._bank_down_button = None
		self._bank_buttons = None
		self._on_off_button = None
		self._device_name_data_source = None
		self._bank_index = 0
		self._bank_name = '<No Bank>'

		def make_button_slot(name):
			return self.register_slot(None, getattr(self, '_%s_value' % name), 'value')

		self._bank_up_button_slot = make_button_slot('bank_up')
		self._bank_down_button_slot = make_button_slot('bank_down')
		self._on_off_button_slot = make_button_slot('on_off')
		self.__on_device_bank_changed.subject = self._device_bank_registry
		self.__on_provided_device_changed.subject = self._device_provider
		self.__on_provided_device_changed()

	def disconnect(self):
		self._device_bank_registry = None
		self._release_parameters(self._parameter_controls)
		self._parameter_controls = None
		self._bank_up_button = None
		self._bank_down_button = None
		self._bank_buttons = None
		self._on_off_button = None
		self._device_provider = None
		super(DeviceComponentBase, self).disconnect()

	#this property can't be listened to, so we can't skin it based on whether it can be incremented or decremented :/
	# @listens('selected_variation_index')
	# def _update_device_macro_buttons(self):
	# 	device = self._get_device()
	# 	if liveobj_valid(device):
	# 		if hasattr(device, 'selected_variation_index'):
	# 			index = device.selected_variation_index
	# 			count = device.variation_count
	# 			self.prev_macro_button.color = "Device.VariationNavOn" if (index > 0) else "Device.VariationNavOff"
	# 			self.next_macro_button.color = "Device.VariationNavOn" if (index < (count-1)) else "Device.VariationNavOff"


	def _get_device(self):
		return self._device_provider.device

	def on_enabled_changed(self):
		self.update()

	@listens('device')
	def __on_provided_device_changed(self):
		self._on_device_changed(self._get_device())

	def _on_device_changed(self, device):
		if liveobj_valid(device):
			self._release_parameters(self._parameter_controls)
		self.__on_device_name_changed.subject = device
		self.__on_parameters_changed.subject = device
		self.__on_device_on_off_changed.subject = self._on_off_parameter()
		if liveobj_valid(device):
			self._bank_index = 0
		self._bank_index = self._device_bank_registry.get_device_bank(device)
		self._bank_name = '<No Bank>'
		self.__on_device_name_changed()
		# self._update_device_macro_buttons.subject = device if hasattr(device, 'selected_variation_index') else None  #this property can't be listened to, so we can't skin it based on whether it can be incremented or decremented :/
		self.update()

	@randomize_macro_button.pressed
	def randomize_macro_button(self, button):
		debug('randomize_macro_button.pressed')
		device = self._get_device()
		if liveobj_valid(device):
			if hasattr(device, 'randomize_macros'):
				device.randomize_macros()

	@add_macro_button.pressed
	def add_macro_button(self, button):
		debug('add_macro_button.pressed')
		device = self._get_device()
		if liveobj_valid(device):
			if hasattr(device, 'store_variation'):
				device.store_variation()

	@delete_macro_button.pressed
	def delete_macro_button(self, button):
		debug('delete_macro_button.pressed')
		device = self._get_device()
		if liveobj_valid(device):
			if hasattr(device, 'delete_selected_variation'):
				# debug('deleting...')
				index = device.selected_variation_index
				device.delete_selected_variation()
				if device.variation_count:
					device.selected_variation_index = max(0, index-1)

	@prev_macro_button.pressed
	def prev_macro_button(self, button):
		debug('prev_macro_button.pressed')
		device = self._get_device()
		if liveobj_valid(device):
			if hasattr(device, 'selected_variation_index'):
				index = device.selected_variation_index
				count = device.variation_count
				if index > -1:
					device.selected_variation_index = max(0, index-1)
				else:
					device.selected_variation_index = count-1
				device.recall_selected_variation()

	@next_macro_button.pressed
	def next_macro_button(self, button):
		debug('next_macro_button.pressed')
		device = self._get_device()
		if liveobj_valid(device):
			if hasattr(device, 'selected_variation_index'):
				index = device.selected_variation_index
				count = device.variation_count
				if index > -1:
					device.selected_variation_index = min(count-1, index+1)
				else:
					device.selected_variation_index = 0
				device.recall_selected_variation()


	def set_bank_prev_button(self, button):
		if button != self._bank_down_button:
			self._bank_down_button = button
			self._bank_down_button_slot.subject = button
			self.update()

	def set_bank_next_button(self, button):
		if button != self._bank_up_button:
			self._bank_up_button = button
			self._bank_up_button_slot.subject = button
			self.update()

	def set_bank_nav_buttons(self, down_button, up_button):
		self.set_bank_prev_button(down_button)
		self.set_bank_next_button(up_button)

	def set_bank_buttons(self, buttons):
		self._bank_buttons = buttons
		self.__on_bank_value.replace_subjects(buttons or [])
		self.update()

	def set_parameter_controls(self, controls):
		self._release_parameters(self._parameter_controls)
		self._parameter_controls = controls
		self.update()

	def set_on_off_button(self, button):
		self._on_off_button = button
		self._on_off_button_slot.subject = button
		self._update_on_off_button()

	def device_name_data_source(self):
		if self._device_name_data_source == None:
			self._device_name_data_source = DisplayDataSource()
			self.__on_device_name_changed()
		return self._device_name_data_source

	def update(self):
		super(DeviceComponentBase, self).update()
		if self.is_enabled() and liveobj_valid(self._get_device()):
			self._device_bank_registry.set_device_bank(self._get_device(), self._bank_index)
			if self._parameter_controls != None:
				old_bank_name = self._bank_name
				self._assign_parameters()
				#if self._bank_name != old_bank_name:
				#	self._show_msg_callback(self._get_device().name + u' Bank: ' + self._bank_name)
		elif self._parameter_controls != None:
			self._release_parameters(self._parameter_controls)
		if self.is_enabled():
			self._update_on_off_button()
			self._update_device_bank_buttons()
			self._update_device_bank_nav_buttons()
			# self._update_device_macro_buttons()


	def _bank_up_value(self, value):
		assert self._bank_up_button != None
		assert value != None
		assert isinstance(value, int)
		if self.is_enabled():
			if not self._bank_up_button.is_momentary() or value != 0:
				if liveobj_valid(self._get_device()):
					num_banks = self._number_of_parameter_banks()
					if self._bank_down_button == None:
						self._bank_name = ''
						self._bank_index = (self._bank_index + 1) % num_banks if self._bank_index != None else 0
						self.update()
					elif self._bank_index == None or num_banks > self._bank_index + 1:
						self._bank_name = ''
						self._bank_index = self._bank_index + 1 if self._bank_index != None else 0
						self.update()

	def _bank_down_value(self, value):
		assert self._bank_down_button != None
		assert value != None
		assert isinstance(value, int)
		if self.is_enabled():
			if not self._bank_down_button.is_momentary() or value != 0:
				if liveobj_valid(self._get_device()) and (self._bank_index == None or self._bank_index > 0):
					self._bank_name = ''
					self._bank_index = self._bank_index - 1 if self._bank_index != None else max(0, self._number_of_parameter_banks() - 1)
					self.update()

	def _on_off_value(self, value):
		assert self._on_off_button != None
		assert value in range(128)
		if not self._on_off_button.is_momentary() or value != 0:
			parameter = self._on_off_parameter()
			if parameter != None and parameter.is_enabled:
				parameter.value = float(int(parameter.value == 0.0))

	@listens_group('value')
	def __on_bank_value(self, value, button):
		self._bank_value(value, button)

	def _bank_value(self, value, button):
		if self.is_enabled() and liveobj_valid(self._get_device()):
			if not button.is_momentary() or value != 0:
				bank = list(self._bank_buttons).index(button)
				if bank != self._bank_index:
					if self._number_of_parameter_banks() > bank:
						self._bank_name = ''
						self._bank_index = bank
						self.update()
				#else:
				#	self._show_msg_callback(self._get_device().name + u' Bank: ' + self._bank_name)

	def _is_banking_enabled(self):
		direct_banking = self._bank_buttons != None
		roundtrip_banking = self._bank_up_button != None
		increment_banking = self._bank_up_button != None and self._bank_down_button != None
		return direct_banking or roundtrip_banking or increment_banking

	def _assign_parameters(self):
		assert self.is_enabled()
		assert liveobj_valid(self._get_device())
		assert self._parameter_controls != None
		self._bank_name, bank = self._current_bank_details()
		for control, parameter in zip(self._parameter_controls, bank):
			if control != None:
				if parameter != None:
					control.connect_to(parameter)
				else:
					control.release_parameter()

		self._release_parameters(self._parameter_controls[len(bank):])

	@listens('value')
	def __on_device_on_off_changed(self):
		self._update_on_off_button()

	@listens('name')
	def __on_device_name_changed(self):
		if self._device_name_data_source != None:
			self._device_name_data_source.set_display_string(self._get_device().name if self.is_enabled() and liveobj_valid(self._get_device()) else 'No Device')

	@listens('parameters')
	def __on_parameters_changed(self):
		self.update()

	def _on_off_parameter(self):
		result = None
		if liveobj_valid(self._get_device()):
			for parameter in self._get_device().parameters:
				if str(parameter.name).startswith('Device On'):
					result = parameter
					break

		return result

	def _update_on_off_button(self):
		if self.is_enabled() and self._on_off_button != None:
			turn_on = False
			if liveobj_valid(self._get_device()):
				parameter = self._on_off_parameter()
				turn_on = parameter != None and parameter.value > 0.0
			self._on_off_button.set_light(turn_on)

	def _update_device_bank_buttons(self):
		if self.is_enabled():
			for index, button in enumerate(self._bank_buttons or []):
				if button:
					turn_on = index == self._bank_index and liveobj_valid(self._get_device())
					button.set_light(turn_on)

	def _update_device_bank_nav_buttons(self):
		if self.is_enabled():
			if self._bank_up_button != None and self._bank_down_button != None:
				can_bank_up = self._bank_index == None or self._number_of_parameter_banks() > self._bank_index + 1
				can_bank_down = self._bank_index == None or self._bank_index > 0
				self._bank_up_button.set_light(self._get_device() and can_bank_up)
				self._bank_down_button.set_light(self._get_device() and can_bank_down)

	def _best_of_parameter_bank(self):
		return best_of_parameter_bank(self._get_device())


	def _parameter_banks(self):
		if EXTENDED_PARAM_DIALS:
			return special_parameter_banks(self._get_device())
		else:
			return parameter_banks(self._get_device())


	def _parameter_bank_names(self):
		if EXTENDED_PARAM_DIALS:
			return special_parameter_bank_names(self._get_device())
		else:
			return parameter_bank_names(self._get_device())

#this is uncommeented in the Vadim version script
#	def _device_parameters_to_map(self):
#		return device_parameters_to_map(self._get_device())

	def _number_of_parameter_banks(self):
		if EXTENDED_PARAM_DIALS:
			return special_number_of_parameter_banks(self._get_device())
		else:
			return number_of_parameter_banks(self._get_device())


	def _device_parameters_to_map(self):
		return device_parameters_to_map(self._get_device())

	def _current_bank_details(self):
		bank_name = self._bank_name
		bank = []
		# best_of only have 8 params, so we're automatically setting its return to false
		# best_of = self._best_of_parameter_bank()
		best_of = False
		banks = self._parameter_banks()
		if banks:
			if self._bank_index != None and self._is_banking_enabled() or not best_of:
				index = self._bank_index if self._bank_index != None else 0
				bank = banks[index]
				# debug('bank is:', bank)
				bank_name = self._parameter_bank_names()[index]
			else:
				bank = best_of
				bank_name = 'Best of Parameters'
		# debug('current_bank_details:', bank_name, bank)
		return (bank_name, bank)

	@listens('device_bank')
	def __on_device_bank_changed(self, device, new_bank_index):
		if device == self._get_device() and new_bank_index != self._bank_index and self._number_of_parameter_banks() > new_bank_index:
			self._bank_index = new_bank_index
			self.update()

	def _release_parameters(self, controls):
		if controls != None:
			for control in controls:
				if control != None:
					control.release_parameter()


class DeviceComponent(DeviceComponentBase):


	def _get_device(self):
		return self._device_provider.device if self._device_provider else None
