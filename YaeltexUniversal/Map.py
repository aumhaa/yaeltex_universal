# by amounra 0216 : http://www.aumhaa.com
# written against Live 9.6 release on 021516


from ableton.v2.control_surface.elements.color import Color
from .colors import *

VU_METER_LOG_SCALING = False

SESSION_BOX_SIZE = (16, 8)  #maximum size for this is 16 tracks x 8 scenes

MUTE_NOTES = list(range(16))
MUTE_CHANNEL = 0

SOLO_NOTES = list(range(16, 32))
SOLO_CHANNEL = 0

ARM_NOTES = list(range(32, 48))
ARM_CHANNEL = 0

SELECT_NOTES = list(range(48, 60))
SELECT_CHANNEL = 0

CROSSFADE_ASSIGN_NOTES = list(range(60,76))
CROSSFADE_ASSIGN_CHANNEL = 0

VOLUME_CCS = list(range(16))
VOLUME_CHANNEL = 0

PAN_CCS = list(range(16, 32))
PAN_CHANNEL = 0

PARAMETER_ON_OFF_NOTE = 127
PARAMETER_CCS = list(range(32, 40))
PARAMETER_CHANNEL = 0

TRACK_PARAMETER_ON_OFF_NOTES = list(range(72))
TRACK_PARAMETER_ON_OFF_CHANNEL = 3

TRACK1_PARAMETER_CCS = list(range(0, 64))
TRACK1_PARAMETER_CHANNEL = 2

TRACK2_PARAMETER_CCS = list(range(0, 64))
TRACK2_PARAMETER_CHANNEL = 3

TRACK3_PARAMETER_CCS = list(range(0, 64))
TRACK3_PARAMETER_CHANNEL = 4

TRACK4_PARAMETER_CCS = list(range(0, 64))
TRACK4_PARAMETER_CHANNEL = 5

TRACK5_PARAMETER_CCS = list(range(0, 64))
TRACK5_PARAMETER_CHANNEL = 6

TRACK6_PARAMETER_CCS = list(range(0, 64))
TRACK6_PARAMETER_CHANNEL = 7

TRACK7_PARAMETER_CCS = list(range(0, 64))
TRACK7_PARAMETER_CHANNEL = 8

TRACK8_PARAMETER_CCS = list(range(0, 64))
TRACK8_PARAMETER_CHANNEL = 9

SELECTEDTRACK_PARAMETER_CCS = (0, 1, 2, 3, 4, 5, 6, 7,
								8, 9, 10, 11, 12, 13, 14, 15,
								16, 17, 18, 19, 20, 21, 22, 23,
								24, 25, 26, 27, 28, 29, 30, 31,
								32, 33, 34, 35, 36, 37, 38, 39,
								40, 41, 42, 43, 44, 45, 46, 47,
								48, 49, 50, 51, 52, 53, 54, 55,
								56, 57, 58, 59, 60, 61, 62, 63)

SELECTEDTRACK_PARAMETER_CHANNEL = 10

SENDA_CCS = list(range(16))
SENDA_CHANNEL = 1

SENDB_CCS = list(range(16,32))
SENDB_CHANNEL = 1

SENDC_CCS = list(range(32, 48))
SENDC_CHANNEL = 1

SENDD_CCS = list(range(48, 64))
SENDD_CHANNEL = 1

SENDE_CCS = list(range(64, 80))
SENDE_CHANNEL = 1

SENDF_CCS = list(range(80, 96))
SENDF_CHANNEL = 1

SENDG_CCS = list(range(96, 112))
SENDG_CHANNEL = 1

SENDH_CCS = list(range(112, 128))
SENDH_CHANNEL = 1

RETURN_VOLUME_CCS = list(range(117, 124))
RETURN_VOLUME_CHANNEL = 0

TEMPO_CONTROL_CC = 124
TEMPO_CONTROL_CHANNEL = 0

CROSSFADER_CC = 125
CROSSFADER_CHANNEL = 0

CUE_VOLUME_CC = 126
CUE_VOLUME_CHANNEL = 0

MASTER_VOLUME_CC = 127
MASTER_VOLUME_CHANNEL = 0

METER_CCS = list(range(16))
METER_LEFT_CCS = list(range(16,32))
METER_RIGHT_CCS = list(range(32,48))
METER_SUM_CCS = list(range(48,64))
METER_CHANNEL = 15

CLIPLAUNCH_NOTES = list(range(128))
CLIPLAUNCH_CHANNEL = 1

CLIPSTOP_NOTES = list(range(16))
CLIPSTOP_CHANNEL = 2

SCENELAUNCH_NOTES = list(range(16,24))
SCENELAUNCH_CHANNEL = 2

SESSIONNAV_NOTES = list(range(24,28))
SESSIONNAV_CHANNEL = 2

ALLCLIPSTOP_NOTE = 127
ALLCLIPSTOP_CHANNEL = 2

TRANSPORT_PLAY_NOTE = 1
TRANSPORT_STOP_NOTE = 2
TRANSPORT_REC_NOTE = 3
TRANSPORT_OD_NOTE = 4
TRANSPORT_CLICK_NOTE = 5
TRANSPORT_TAPTEMPO_NOTE = 6
TRANSPORT_LOOP_NOTE = 7

TRANSPORT_CHANNEL = 3


# These color values can easily be set to numerical values:
#
#   class TestClass:
#		Testcolor = MonoColor(64)


class YAELTEXColors:


	class ModeButtons:
		Main = LividRGB.WHITE
		Select = LividRGB.RED
		Clips = LividRGB.GREEN


	class DefaultButton:
		On = MonoColor(127)  #LividRGB.WHITE
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
		XFadeOff = LividRGB.OFF
		XFadeAOn = LividRGB.YELLOW
		XFadeBOn = LividRGB.MAGENTA


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
