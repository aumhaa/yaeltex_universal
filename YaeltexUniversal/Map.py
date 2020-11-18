# by amounra 0216 : http://www.aumhaa.com
# written against Live 9.6 release on 021516


from ableton.v2.control_surface.elements.color import Color
from aumhaa.v2.livid.colors import *


MUTE_NOTES = range(16)
MUTE_CHANNEL = 0

SOLO_NOTES = range(16, 32)
SOLO_CHANNEL = 0

ARM_NOTES = range(32, 48)
ARM_CHANNEL = 0

VOLUME_CCS = range(16)
VOLUME_CHANNEL = 0

PAN_CCS = range(16, 32)
PAN_CHANNEL = 0

SENDA_CCS = range(16)
SENDA_CHANNEL = 1

SENDB_CCS = range(16,32)
SENDB_CHANNEL = 1

SENDC_CCS = range(32, 48)
SENDC_CHANNEL = 1

SENDD_CCS = range(48, 64)
SENDD_CHANNEL = 1

SENDE_CCS = range(64, 80)
SENDE_CHANNEL = 1

SENDF_CCS = range(80, 96)
SENDF_CHANNEL = 1

SENDG_CCS = range(96, 112)
SENDG_CHANNEL = 1

SENDH_CCS = range(112, 128)
SENDH_CHANNEL = 1

RETURN_VOLUME_CCS = range(117, 124)
RETURN_VOLUME_CHANNEL = 0

CROSSFADER_CC = 125
CROSSFADER_CHANNEL = 0

CUE_VOLUME_CC = 126
CUE_VOLUME_CHANNEL = 0

MASTER_VOLUME_CC = 127
MASTER_VOLUME_CHANNEL = 0



class YAELTEXColors:


	class ModeButtons:
		Main = LividRGB.WHITE
		Select = LividRGB.RED
		Clips = LividRGB.GREEN


	class DefaultButton:
		On = LividRGB.WHITE
		Off = LividRGB.OFF
		Disabled = LividRGB.OFF
		Alert = LividRGB.BlinkFast.WHITE


	class Session:
		StopClipDisabled = LividRGB.OFF
		StopClipTriggered = LividRGB.BiColor.BLUE.WHITE
		StopClip = LividRGB.BLUE
		Scene = LividRGB.CYAN
		NoScene = LividRGB.OFF
		SceneTriggered = LividRGB.GREEN
		ClipTriggeredPlay = LividRGB.BlinkFast.GREEN
		ClipTriggeredRecord = LividRGB.BlinkFast.RED
		RecordButton = LividRGB.OFF
		ClipEmpty = LividRGB.OFF
		ClipStopped = LividRGB.WHITE
		ClipStarted = LividRGB.GREEN
		ClipRecording = LividRGB.RED
		NavigationButtonOn = LividRGB.CYAN
		NavigationButtonOff = LividRGB.YELLOW
		ZoomOn = LividRGB.BlinkFast.WHITE
		ZoomOff = LividRGB.WHITE


	class Zooming:
		Selected = LividRGB.BlinkFast.YELLOW
		Stopped = LividRGB.WHITE
		Playing = LividRGB.GREEN
		Empty = LividRGB.OFF


	class LoopSelector:
		Playhead = LividRGB.YELLOW
		OutsideLoop = LividRGB.BLUE
		InsideLoopStartBar = LividRGB.CYAN
		SelectedPage = LividRGB.WHITE
		InsideLoop = LividRGB.CYAN
		PlayheadRecord = LividRGB.RED


	class Transport:
		PlayOn = LividRGB.BiColor.WHITE.GREEN
		PlayOff = LividRGB.GREEN
		StopOn = LividRGB.BLUE
		StopOff = LividRGB.BLUE
		RecordOn = LividRGB.BiColor.WHITE.RED
		RecordOff = LividRGB.RED
		OverdubOn = LividRGB.BiColor.WHITE.MAGENTA
		OverdubOff = LividRGB.MAGENTA
		SeekBackwardOn = LividRGB.BlinkMedium.CYAN
		SeekBackwardOff = LividRGB.CYAN
		LoopOn = LividRGB.BlinkMedium.YELLOW
		LoopOff = LividRGB.YELLOW


	class Mixer:
		SoloOn = LividRGB.BLUE
		SoloOff = LividRGB.CYAN
		MuteOn = LividRGB.YELLOW
		MuteOff = LividRGB.WHITE
		ArmSelected = LividRGB.RED
		ArmUnselected = LividRGB.RED
		ArmOff = LividRGB.GREEN
		StopClip = LividRGB.BLUE
		SelectedOn = LividRGB.BLUE
		SelectedOff = LividRGB.MAGENTA


	class Recording:
		On = LividRGB.BiColor.WHITE.MAGENTA
		Transition = LividRGB.BlinkFast.MAGENTA
		Off = LividRGB.MAGENTA


	class Automation:
		On = LividRGB.BiColor.WHITE.YELLOW
		Off = LividRGB.YELLOW


	class Recorder:
		On = LividRGB.WHITE
		Off = LividRGB.BLUE
		NewOn = LividRGB.BlinkMedium.YELLOW
		NewOff = LividRGB.YELLOW
		FixedOn = LividRGB.BlinkMedium.CYAN
		FixedOff = LividRGB.CYAN
		RecordOn = LividRGB.BiColor.WHITE.MAGENTA
		RecordOff = LividRGB.MAGENTA
		AutomationOn = LividRGB.BiColor.WHITE.YELLOW
		AutomationOff = LividRGB.YELLOW
		FixedAssigned = LividRGB.MAGENTA
		FixedNotAssigned = LividRGB.OFF


	class Device:
		NavOn = LividRGB.MAGENTA
		NavOff = LividRGB.OFF
		BankOn = LividRGB.YELLOW
		BankOff = LividRGB.OFF
		ChainNavOn = LividRGB.RED
		ChainNavOff = LividRGB.OFF
		ContainNavOn = LividRGB.CYAN
		ContainNavOff = LividRGB.OFF
