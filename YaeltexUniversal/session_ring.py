# by amounra 1125 : http://www.aumhaa.com
# version 2.3


import Live
import math
import logging
# from re import *

from ableton.v2.base import listens
from ableton.v2.control_surface.components import ClipSlotComponent, SceneComponent, SessionComponent, TransportComponent, BackgroundComponent, ViewControlComponent, SessionRingComponent, SessionRecordingComponent, SessionNavigationComponent, MixerComponent, PlayableComponent

from .debug import initialize_debug

LOCAL_DEBUG = False
debug = initialize_debug(local_debug = LOCAL_DEBUG)

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
		self._snap_offsets = True
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
