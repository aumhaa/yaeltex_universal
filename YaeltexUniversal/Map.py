# by amounra 0216 : http://www.aumhaa.com
# written against Live 9.6 release on 021516


from ableton.v2.control_surface.elements.color import Color
from .colors import *

VU_METER_LOG_SCALING = False
VU_METER_ENABLED = True

SESSION_BOX_SIZE = (16, 8)  #maximum size for this is 16 tracks x 8 scenes

MUTE_NOTES = list(range(16))
MUTE_CHANNEL = 0

SOLO_NOTES = list(range(16, 32))
SOLO_CHANNEL = 0

ARM_NOTES = list(range(32, 48))
ARM_CHANNEL = 0

SELECT_NOTES = list(range(48, 64))
SELECT_CHANNEL = 0

CROSSFADE_ASSIGN_NOTES = list(range(64,80))
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

TRACK_PARAMETER_CCS = [TRACK1_PARAMETER_CCS,
						TRACK2_PARAMETER_CCS,
						TRACK3_PARAMETER_CCS,
						TRACK4_PARAMETER_CCS,
						TRACK5_PARAMETER_CCS,
						TRACK6_PARAMETER_CCS,
						TRACK7_PARAMETER_CCS,
						TRACK8_PARAMETER_CCS]

TRACK_PARAMETER_CHANNELS = [TRACK1_PARAMETER_CHANNEL,
						TRACK2_PARAMETER_CHANNEL,
						TRACK3_PARAMETER_CHANNEL,
						TRACK4_PARAMETER_CHANNEL,
						TRACK5_PARAMETER_CHANNEL,
						TRACK6_PARAMETER_CHANNEL,
						TRACK7_PARAMETER_CHANNEL,
						TRACK8_PARAMETER_CHANNEL]

SELECTEDTRACK_PARAMETER_CCS = list(range(0, 64))

SELECTEDTRACK_PARAMETER_CHANNEL = 10

NUM_SEND_CONTROLS = 2

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

TRANSPORT_CHANNEL = 4

SELECTED_STRIP_PARAMETER_CONTROLS_ENABLED = True
TRACK_STRIP_PARAMETER_CONTROLS_ENABLED = True
STRIP_PARAM1_CONTROLS_ENABLED = True
STRIP_PARAM2_CONTROLS_ENABLED = False
STRIP_PARAM3_CONTROLS_ENABLED = False
STRIP_PARAM4_CONTROLS_ENABLED = False
STRIP_PARAM5_CONTROLS_ENABLED = False
STRIP_PARAM6_CONTROLS_ENABLED = False
STRIP_PARAM7_CONTROLS_ENABLED = False
STRIP_PARAM8_CONTROLS_ENABLED = False

STRIP_PARAM_CONTROLS_ENABLED_FLAGS = [STRIP_PARAM1_CONTROLS_ENABLED,
									STRIP_PARAM2_CONTROLS_ENABLED,
									STRIP_PARAM3_CONTROLS_ENABLED,
									STRIP_PARAM4_CONTROLS_ENABLED,
									STRIP_PARAM5_CONTROLS_ENABLED,
									STRIP_PARAM6_CONTROLS_ENABLED,
									STRIP_PARAM7_CONTROLS_ENABLED,
									STRIP_PARAM8_CONTROLS_ENABLED]



class YAELTEXColors:


	class ModeButtons:
		Main = MonoColor(1)
		Select = MonoColor(5)
		Clips = MonoColor(6)


	class DefaultButton:
		On = MonoColor(127)
		Off = MonoColor(0)
		Disabled = MonoColor(0)
		Alert = MonoColor(1)


	class Session:
		StopClipDisabled = MonoColor(0)
		StopClipTriggered = MonoColor(7)
		StopClip = MonoColor(7)
		Scene = MonoColor(3)
		NoScene = MonoColor(0)
		SceneTriggered = MonoColor(6)
		ClipTriggeredPlay = MonoColor(7)
		ClipTriggeredRecord = MonoColor(5)
		RecordButton = MonoColor(0)
		ClipEmpty = MonoColor(0)
		ClipStopped = MonoColor(1)
		ClipStarted = MonoColor(6)
		ClipRecording = MonoColor(5)
		NavigationButtonOn = MonoColor(3)
		NavigationButtonOff = MonoColor(2)
		ZoomOn = MonoColor(1)
		ZoomOff = MonoColor(7)


	class Zooming:
		Selected = MonoColor(2)
		Stopped = MonoColor(1)
		Playing = MonoColor(6)
		Empty = MonoColor(0)


	class LoopSelector:
		Playhead = MonoColor(2)
		OutsideLoop = MonoColor(7)
		InsideLoopStartBar = MonoColor(3)
		SelectedPage = MonoColor(1)
		InsideLoop = MonoColor(3)
		PlayheadRecord = MonoColor(5)


	class Transport:
		PlayOn = MonoColor(6)
		PlayOff = MonoColor(6)
		StopOn = MonoColor(7)
		StopOff = MonoColor(7)
		RecordOn = MonoColor(5)
		RecordOff = MonoColor(5)
		OverdubOn = MonoColor(4)
		OverdubOff = MonoColor(4)
		SeekBackwardOn = MonoColor(3)
		SeekBackwardOff = MonoColor(3)
		LoopOn = MonoColor(2)
		LoopOff = MonoColor(2)


	class Mixer:
		SoloOn = MonoColor(7)
		SoloOff = MonoColor(3)
		MuteOn = MonoColor(2)
		MuteOff = MonoColor(1)
		ArmSelected = MonoColor(5)
		ArmUnselected = MonoColor(5)
		ArmOff = MonoColor(6)
		StopClip = MonoColor(7)
		SelectedOn = MonoColor(7)
		SelectedOff = MonoColor(4)
		XFadeOff = MonoColor(0)
		XFadeAOn = MonoColor(2)
		XFadeBOn = MonoColor(4)


	class Recording:
		On = MonoColor(5)
		Transition = MonoColor(1)
		Off = MonoColor(4)


	class Automation:
		On = MonoColor(0)
		Off = MonoColor(2)


	class Recorder:
		On = MonoColor(1)
		Off = MonoColor(7)
		NewOn = MonoColor(2)
		NewOff = MonoColor(1)
		FixedOn = MonoColor(3)
		FixedOff = MonoColor(1)
		RecordOn = MonoColor(4)
		RecordOff = MonoColor(1)
		AutomationOn = MonoColor(2)
		AutomationOff = MonoColor(1)
		FixedAssigned = MonoColor(4)
		FixedNotAssigned = MonoColor(0)


	class Device:
		NavOn = MonoColor(4)
		NavOff = MonoColor(0)
		BankOn = MonoColor(2)
		BankOff = MonoColor(0)
		ChainNavOn = MonoColor(5)
		ChainNavOff = MonoColor(0)
		ContainNavOn = MonoColor(3)
		ContainNavOff = MonoColor(0)
