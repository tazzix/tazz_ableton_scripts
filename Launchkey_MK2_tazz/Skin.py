from __future__ import absolute_import, print_function, unicode_literals
from _Framework.Skin import Skin
from .Colors import Rgb

class Colors:

    class Session:
        SceneTriggered = Rgb.GREEN_BLINK
        NoScene = Rgb.BLACK
        ClipStarted = Rgb.GREEN_PULSE
        ClipRecording = Rgb.RED_PULSE
        ClipTriggeredPlay = Rgb.GREEN_BLINK
        ClipTriggeredRecord = Rgb.RED_BLINK
        ClipEmpty = Rgb.BLACK
        RecordButton = Rgb.RED_HALF
        StopClip = Rgb.GREEN
        StopClipTriggered = Rgb.GREEN_BLINK
        StoppedClip = Rgb.GREEN_HALF
        Enabled = Rgb.YELLOW

    class Mode:
        DeviceMode = Rgb.PURPLE_HALF
        DeviceModeOn = Rgb.PURPLE
        VolumeMode = Rgb.DARK_YELLOW_HALF
        VolumeModeOn = Rgb.DARK_YELLOW
        PanMode = Rgb.ORANGE_HALF
        PanModeOn = Rgb.ORANGE
        PadMode = Rgb.YELLOW_HALF
        PadModeOn = Rgb.YELLOW
        Send0Mode = Rgb.DARK_BLUE_HALF
        Send0ModeOn = Rgb.BRIGHT_PURPLE
        Send1Mode = Rgb.BLUE_HALF
        Send1ModeOn = Rgb.BLUE
        Send2Mode = Rgb.LIGHT_BLUE_HALF
        Send2ModeOn = Rgb.LIGHT_BLUE
        Send3Mode = Rgb.MINT_HALF
        Send3ModeOn = Rgb.MINT
        #Send4Mode = Rgb.DARK_YELLOW_HALF
        #Send4ModeOn = Rgb.DARK_YELLOW
        #Send5Mode = Rgb.YELLOW_HALF
        #Send5ModeOn = Rgb.YELLOW
        Disabled = Rgb.BLACK
        StopMode = Rgb.ORANGE_HALF
        StopModeOn = Rgb.ORANGE
        SoloMode = Rgb.PURPLE_HALF
        SoloModeOn = Rgb.PURPLE
        MuteMode = Rgb.DARK_YELLOW_HALF
        MuteModeOn = Rgb.DARK_YELLOW

    class Device:
        Bank = Rgb.DARK_PURPLE
        BestOfBank = Rgb.PURPLE_HALF
        BankSelected = Rgb.PURPLE


def make_skin():
    return Skin(Colors)
