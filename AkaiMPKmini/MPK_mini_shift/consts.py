
####### ALL CONTROLS ARE CC

num_tracks = 4
num_scenes = 1
num_device_params = 5
#session_left = 40
#session_right = 41
HSCROLLENCODER = 7
session_up = 46
session_down = 47
VSCROLLENCODER = 8
# initial_mod = 42 : not implemented
shift_mod = 121
alt_mod = 122
ctrl_mod = 123
modifiers_buttons = [shift_mod, alt_mod, ctrl_mod]

# INITIAL MODE CONSTS
device_param_cc = [0,1,2,3,4,5]
device_left_cc = 32
device_right_cc = 68
device_lock = 35
device_onoff = 34
track_arm_cc = [28,72,30,31]
transport_metronome_cc = 26
transport_overdub_cc = 20
transport_loop_cc = 21
transport_record_cc = 24
session_stopall_cc = 23
session_scenelaunch_cc = [27]
mixer_mastervol_cc = 6
sel_clip_launch = 22
sel_scene_launch = 27


# SHIFT MODE CONSTS
mixer_volumefader_cc = [1, 2, 3, 4]
mixer_sendknob_cc = [5, 6, 7, 8]
session_cliplaunch_cc = [26,22,27,23] # the number of notes in here must match box_width * box_height\
track_solo_cc = [32,68,34,35]
track_mute_cc = [28,72,30,31]
session_left = 20
session_right = 21

#                   Normal                              Shift                       Alt                                 Shift-Alt (Ctrl) - Not implemented
# 1,2,3,4           Device Params                      Track Vol *4               Blank *4 (Blanks for mapping)
# 5,6,7,8           D-5, M-Vol, Nav *2                 Track Sends *4             Blank *2, Nav *2
#-------------
#B 32,68,34,35      Device R/L *2, toggle, lock        Track Solo *4              Track Select *4
#B 28,72,30,31      Track Arm *4                       Track Mute *4              Scene Launch, ..., Stop All
#-------------
#A 26,22,27,23      Metro, Clip, Scene, Stop           Clip launch *4             Track Stop *4
#A 20,21,24,Sh      Overdub, Loop                      Sends U/D *2               Track R/L *2

# ALT MODE CONSTS
alt_scenelaunch_cc =[28]
track_select_cc = [32,68,34,35]
stop_track_cc = [26,22,27,23]
send_up = 20
send_down = 21
stop_all = 31


# CTRL MODE CONSTS
detailclip_view_cc = [16,17,18,19]
lock_device_cc = 99
onoff_device_cc = 72
#device_param_cc = [0,1,2,3,4,5]
#device_left_cc = 20
#device_right_cc = 21
transport_stop_cc = 32
transport_play_cc = 33
#transport_record_cc = 24
transport_quantization_cc = 35
transport_tempodown_cc = 46
transport_tempoup_cc = 47
#transport_metronome_cc = 26
#session_stopall_cc = 23
#session_scenelaunch_cc = [27]
# mixer_masterselect_cc = 31   : Not implemented
# mixer_mastervol_cc = 7         : Not implemented

CHANNEL = 1 # Channels are numbered 0 through 15, this script only makes use of one MIDI Channel