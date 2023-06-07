# by amounra 0216 : http://www.aumhaa.com
# written against Live 9.6 release on 021516


from ableton.v2.control_surface.elements.color import Color
from .colors import *

EXTENDED_PARAM_DIALS = False  #Set this to false if you're only using 8 dials, true for 16

DO_COMBINE = True  #set this to false if you don't want scripts to link their session/track together

VU_METER_LOG_SCALING = False
VU_METER_ENABLED = False

SESSION_BOX_SIZE = (8, 4)  #maximum size for this is 16 tracks x 8 scenes

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

MASTER_SELECT_NOTE = 117
MASTER_SELECT_CHANNEL = 0

DEVICE_NAV_PREV = 118
DEVICE_NAV_NEXT = 119
DEVICE_RANDOMIZE_MACRO_NOTE = 120
DEVICE_ADD_MACRO_NOTE = 121
DEVICE_DELETE_MACRO_NOTE = 122
DEVICE_PREV_MACRO_NOTE = 123
DEVICE_NEXT_MACRO_NOTE = 124
DEVICE_BANK_PREV_NOTE = 125
DEVICE_BANK_NEXT_NOTE = 126
PARAMETER_ON_OFF_NOTE = 127

if not EXTENDED_PARAM_DIALS:
	PARAMETER_CCS = list(range(32, 40))
	PARAMETER_CHANNEL = 0
else:
	PARAMETER_CCS = list(range(32, 48))
	PARAMETER_CHANNEL = 0

TRACK_PARAMETER_ON_OFF_NOTES = list(range(72))
TRACK_PARAMETER_ON_OFF_CHANNEL = 3

if not EXTENDED_PARAM_DIALS:
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

	SELECTEDTRACK_PARAMETER_CCS = list(range(0, 64))
	SELECTEDTRACK_PARAMETER_CHANNEL = 10

else:
	TRACK1_PARAMETER_CCS = list(range(0, 128))
	TRACK1_PARAMETER_CHANNEL = 2

	TRACK2_PARAMETER_CCS = list(range(0, 128))
	TRACK2_PARAMETER_CHANNEL = 3

	TRACK3_PARAMETER_CCS = list(range(0, 128))
	TRACK3_PARAMETER_CHANNEL = 4

	TRACK4_PARAMETER_CCS = list(range(0, 128))
	TRACK4_PARAMETER_CHANNEL = 5

	TRACK5_PARAMETER_CCS = list(range(0, 128))
	TRACK5_PARAMETER_CHANNEL = 6

	TRACK6_PARAMETER_CCS = list(range(0, 128))
	TRACK6_PARAMETER_CHANNEL = 7

	TRACK7_PARAMETER_CCS = list(range(0, 128))
	TRACK7_PARAMETER_CHANNEL = 8

	TRACK8_PARAMETER_CCS = list(range(0, 128))
	TRACK8_PARAMETER_CHANNEL = 9

	SELECTEDTRACK_PARAMETER_CCS = list(range(0, 128))
	SELECTEDTRACK_PARAMETER_CHANNEL = 10

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

NUM_SEND_CONTROLS = 4

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

TRACK_SELECT_CC = 115
TRACK_SELECT_CHANNEL = 0

SCENE_SELECT_CC = 116
SCENE_SELECT_CHANNEL = 0

TRACK_BANK_NAV_CC = 113
TRACK_BANK_NAV_CHANNEL = 0

SCENE_BANK_NAV_CC = 114
SCENE_BANK_NAV_CHANNEL = 0

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

SESSIONCLIPLAUNCH_NOTE = 28
SESSIONCLIPLAUNCH_CHANNEL = 2

SESSIONSCENELAUNCH_NOTE = 29
SESSIONSCENELAUNCH_CHANNEL = 2

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
STRIP_PARAM2_CONTROLS_ENABLED = True
STRIP_PARAM3_CONTROLS_ENABLED = True
STRIP_PARAM4_CONTROLS_ENABLED = True
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
		Select = MonoColor(97)
		Clips = MonoColor(6)


	class DefaultButton:
		On = MonoColor(75)
		Off = MonoColor(0)
		Disabled = MonoColor(0)
		Alert = MonoColor(127)


	class Session:
		StopClipDisabled = MonoColor(0)
		StopClipTriggered = MonoColor(75)
		StopClip = MonoColor(22)
		Scene = MonoColor(118)
		NoScene = MonoColor(0)
		SceneTriggered = MonoColor(57)
		ClipTriggeredPlay = MonoColor(7)
		ClipTriggeredRecord = MonoColor(5)
		RecordButton = MonoColor(121)
		ClipEmpty = MonoColor(127)
		ClipStopped = MonoColor(120)
		ClipStarted = MonoColor(43)
		ClipRecording = MonoColor(109)
		NavigationButtonOn = MonoColor(102)
		NavigationButtonOff = MonoColor(2)
		ZoomOn = MonoColor(36)
		ZoomOff = MonoColor(0)
		SelectedClipLaunch = MonoColor(8)
		SelectedSceneLaunch = MonoColor(88)


	class Zooming:
		Selected = MonoColor(2)
		Stopped = MonoColor(0)
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
		PlayOn = MonoColor(49)
		PlayOff = MonoColor(0)
		StopOn = MonoColor(127)
		StopOff = MonoColor(0)
		RecordOn = MonoColor(118)
		RecordOff = MonoColor(0)
		OverdubOn = MonoColor(1)
		OverdubOff = MonoColor(0)
		SeekBackwardOn = MonoColor(3)
		SeekBackwardOff = MonoColor(0)
		LoopOn = MonoColor(19)
		LoopOff = MonoColor(0)


	class Mixer:
		SoloOn = MonoColor(81)
		SoloOff = MonoColor(0)
		MuteOn = MonoColor(16)
		MuteOff = MonoColor(0)
		ArmSelected = MonoColor(121)
		ArmUnselected = MonoColor(7)
		ArmOff = MonoColor(0)
		StopClip = MonoColor(60)
		SelectedOn = MonoColor(49)
		SelectedOff = MonoColor(0)
		XFadeOff = MonoColor(0)
		XFadeAOn = MonoColor(49)
		XFadeBOn = MonoColor(75)


	class Recording:
		On = MonoColor(1)
		Transition = MonoColor(105)
		Off = MonoColor(0)


	class Automation:
		On = MonoColor(121)
		Off = MonoColor(0)


	class Recorder:
		On = MonoColor(1)
		Off = MonoColor(0)
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
		NavOn = MonoColor(19)
		NavOff = MonoColor(0)
		BankOn = MonoColor(49)
		BankOff = MonoColor(0)
		ChainNavOn = MonoColor(43)
		ChainNavOff = MonoColor(0)
		ContainNavOn = MonoColor(43)
		ContainNavOff = MonoColor(0)
		AddVariation = MonoColor(49)
		DeleteVariation = MonoColor(2)
		VariationNavOn = MonoColor(3)
		VariationNavOff = MonoColor(4)
		RandomizeControls = MonoColor(75)
