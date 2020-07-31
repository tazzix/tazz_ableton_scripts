# Brought to you by st4rchild with the help of Hanz Petrov @ http://remotescripts.blogspot.com
# Avoid using tabs for indentation, use spaces.

# Combination Mode offsets
# ------------------------

TRACK_OFFSET = -1 #offset from the left of linked session origin; set to -1 for auto-joining of multiple instances
SCENE_OFFSET = 0 #offset from the top of linked session origin (no auto-join)

SCENE_NUM = 2
TRACK_NUM = 4
DEVICE_NUM = 6

# Buttons / Pads
# -------------
# Valid Note/CC assignments are 0 to 127, or -1 for NONE
# Duplicate assignments are permitted

BUTTONCHANNEL = 0 #Channel assignment for all mapped buttons/pads; valid range is 0 to 15 ; 0=1, 1=2 etc.
MESSAGETYPE = 1 #Message type for buttons/pads; set to 0 for MIDI Notes, 1 for CCs.
        #When using CCs for buttons/pads, set BUTTONCHANNEL and SLIDERCHANNEL to different values.

# Experimental, using for clip launch for now
PADLIGHTSENABLED = 1
# For AKAI MPK mini MK2 ControlSurface.send_midi works by sending MIDI notes 9 - 16 via message 144
PADLIGHTMSG = 144
PADLIGHTON = 127
PADLIGHTOFF = 0
PADOFFSET = 8
PADCOUNT = 8

# General
PLAY = -1 #Global play
STOP = -1 #Global stop
REC = 24 #Global record
TAPTEMPO = -1 #Tap tempo
NUDGEUP = -1 #Tempo Nudge Up
NUDGEDOWN = -1 #Tempo Nudge Down
UNDO = -1 #Undo
REDO = -1 #Redo
LOOP = 21 #Loop on/off
PUNCHIN = -1 #Punch in
PUNCHOUT = -1 #Punch out
OVERDUB = 20 #Overdub on/off
METRONOME = 26 #Metronome on/off
RECQUANT = -1 #Record quantization on/off
DETAILVIEW = -1 #Detail view switch
CLIPTRACKVIEW = 25 #Clip/Track view switch

# Device Control
DEVICELOCK = 28 #Device Lock (lock "blue hand")
DEVICEONOFF = 32 #Device on/off
DEVICENAVLEFT = 30 #Device nav left
DEVICENAVRIGHT = 31 #Device nav right
DEVICEBANKNAVLEFT = 34 #Device bank nav left
DEVICEBANKNAVRIGHT = 35 #Device bank nav right
DEVICEBANK = (-1, #Bank 1 #All 8 banks must be assigned to positive values in order for bank selection to work
              -1, #Bank 2
              -1, #Bank 3
              -1, #Bank 4
              -1, #Bank 5
              -1, #Bank 6
              -1, #Bank 7
              -1, #Bank 8
              )

# Arrangement View Controls
SEEKFWD = -1 #Seek forward
SEEKRWD = -1 #Seek rewind

# Session Navigation (aka "red box")
SESSIONLEFT = -1 #Session left
SESSIONRIGHT = -1 #Session right
SESSIONUP = 44 #Session up
SESSIONDOWN = 45 #Session down
ZOOMUP = -1 #Session Zoom up
ZOOMDOWN = -1 #Session Zoom down
ZOOMLEFT = -1 #Session Zoom left
ZOOMRIGHT = -1 #Session Zoom right

# Track Navigation
TRACKLEFT = 9 #Track left
TRACKRIGHT = 10 #Track right
HSCROLLENCODER = 7

# Scene Navigation
SCENEUP = 66 #Scene down
SCENEDN = 67 #Scene up
VSCROLLENCODER = 8

# Scene Launch
SELSCENELAUNCH = 27 #Selected scene launch
SCENELAUNCH = (-1, #Scene 1 Launch
               -1, #Scene 2
               -1, #Scene 3
               -1, #Scene 4
               -1, #Scene 5
               -1, #Scene 6
               -1, #Scene 7
               -1, #Scene 8
               )

# Clip Launch / Stop
SELCLIPLAUNCH = 22 #Selected clip launch
SELCLIPPAD = -1
STOPALLCLIPS = 23 #Stop all clips

# 8x8 Matrix note assignments
# Track no.:     1   2   3   4   5   6   7   8
CLIPNOTEMAP = ((-1, -1, -1, -1, -1, -1, -1, -1), #Row 1
               (-1, -1, -1, -1, -1, -1, -1, -1), #Row 2
               (-1, -1, -1, -1, -1, -1, -1, -1), #Row 3
               (-1, -1, -1, -1, -1, -1, -1, -1), #Row 4
               (-1, -1, -1, -1, -1, -1, -1, -1), #Row 5
               (-1, -1, -1, -1, -1, -1, -1, -1), #Row 6
               (-1, -1, -1, -1, -1, -1, -1, -1), #Row 7
               (-1, -1, -1, -1, -1, -1, -1, -1), #Row 8
               )

# Track Control
MASTERSEL = 40 #Master track select
TRACKSTOP = (-1, #Track 1 Clip Stop
             -1, #Track 2
             -1, #Track 3
             -1, #Track 4
             -1, #Track 5
             -1, #Track 6
             -1, #Track 7
             -1, #Track 8
             )
TRACKSEL = (36, #Track 1 Select
            -1, #Track 2
            -1, #Track 3
            -1, #Track 4
            -1, #Track 5
            -1, #Track 6
            -1, #Track 7
            -1, #Track 8
            )
TRACKMUTE = (72, #Track 1 On/Off
             73, #Track 2
             74, #Track 3
             75, #Track 4
             -1, #Track 5
             -1, #Track 6
             -1, #Track 7
             -1, #Track 8
             )
TRACKSOLO = (68, #Track 1 Solo
             69, #Track 2
             70, #Track 3
             71, #Track 4
             -1, #Track 5
             -1, #Track 6
             -1, #Track 7
             -1, #Track 8
             )
TRACKARM = (41, #Track 1 Record
            -1, #Track 2
            -1, #Track 3
            -1, #Track 4
            -1, #Track 5
            -1, #Track 6
            -1, #Track 7
            -1, #Track 8
            )


# Pad Translations for Drum Rack

PADCHANNEL = 0 # MIDI channel for Drum Rack notes
DRUM_PADS = (-1, -1, -1, -1, # MIDI note numbers for 4 x 4 Drum Rack
             -1, -1, -1, -1, # Mapping will be disabled if any notes are set to -1
             -1, -1, -1, -1, # Notes will be "swallowed" if already mapped elsewhere
             -1, -1, -1, -1,
             )

# Sliders / Knobs
# ---------------
# Valid CC assignments are 0 to 127, or -1 for NONE
# Duplicate assignments will be ignored

SLIDERCHANNEL = 0 #Channel assignment for all mapped CCs; valid range is 0 to 15
TEMPO_TOP = 180.0 # Upper limit of tempo control in BPM (max is 999)
TEMPO_BOTTOM = 100.0 # Lower limit of tempo control in BPM (min is 0)

TEMPOCONTROL = -1 #Tempo control CC assignment; control range is set above
MASTERVOLUME = 6 #Master track volume
CUELEVEL = -1 #Cue level control
CROSSFADER = -1 #Crossfader control

TRACKVOL = (100, #Track 1 Volume
            101, #Track 2
            102, #Track 3
            103, #Track 4
            104, #Track 5
            105, #Track 6
            106, #Track 7
            107, #Track 8
            )
TRACKPAN = (92, #Track 1 Pan
            93, #Track 2
            94, #Track 3
            95, #Track 4
            96, #Track 5
            97, #Track 6
            98, #Track 7
            99, #Track 8
            )
TRACKSENDA = (108, #Track 1 Send A
              109, #Track 2
              110, #Track 3
              111, #Track 4
              112, #Track 5
              113, #Track 6
              114, #Track 7
              115, #Track 8
              )
TRACKSENDB = (116, #Track 1 Send B
              117, #Track 2
              118, #Track 3
              119, #Track 4
              120, #Track 5
              121, #Track 6
              122, #Track 7
              123, #Track 8
              )
TRACKSENDC = (-1, #Track 1 Send C
              -1, #Track 2
              -1, #Track 3
              -1, #Track 4
              -1, #Track 5
              -1, #Track 6
              -1, #Track 7
              -1, #Track 8
              )
PARAMCONTROL = (1, #Param 1 #All 8 params must be assigned to positive values in order for param control to work
                2, #Param 2
                3, #Param 3
                4, #Param 4
                5, #Param 5
                125, #Param 6
                127, #Param 7
                126, #Param 8
                )
