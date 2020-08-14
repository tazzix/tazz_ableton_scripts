# mpkminiableton

MIDI Remote Script to use Akai MPK Mini MKII with Ableton Live, somewhat according to my workflow preferences. Might be useful for others and easily customizable.

Based on Code and Video Tutorial at: <https://github.com/laidlaw42/Ableton-Live-MIDI-Remote-Scripts>

## Setup Instructions

### Ableton MIDI Remote Scripts

- Copy the directory "MPK_mini_tazz" into Live MIDI script folder:

On a MAC machine: right click on Ableton Live application, click on Show Contents, then /Contents/App-Resources/MIDI Remote Scripts/

On a Windows machine: \ProgramData\Ableton\Live x.x\Resources\MIDI Remote Scripts\

- Select the script as Control Surface in Live preferences, and couple it with the MIDI controller you want to use.

### Select Script in MIDI Settings

- On a MAC CMD-, on Windows Ctrl-,  or Preferences from the menu, under MIDI select MPK mini tazz for your MPK Mini MKII
- Make sure device for both Input and Output is ON for Track and Remote, output is only needed for control of Pad lights

### Hardware Presets to load

The folder Presets had presets saved from MPK Mini editor which you can load either in the same or different order or maybe only the ones you need.

The Editor folder also has screen shots if the presets don't work for some reason.

### Printable template

The PNG file in the root folder contains a scaled printable template that you can cut and put on the keyboard instead of tape and handwriting. Print on 100% with 72 dpi.

## What does it do

I was using a bigger Novation Launchkey MKII and really liked the way it worked without the need to constantly reach for the mouse or keyboard during leisure playback or production. Which the much more compact MPK mini was lacking; although I have also taken a stab at performance but I guess that might still be better off with a Push or Novation product.

Considering the popularity of MPK mini and Ableton, it is surprising that such a script does not exist already but it also turned out to be rather simple.

### Setup

I am using a foot switch (Sustain Pedal) as a recording and overdub tool and it is mapped to "Session Record" via MIDI mapping. All other controls are setup using presets as explained below.

### Preset 1

This is a usual composing preset with a twist. Instead of sacrificing 4 pads for direction arrows, the encoder knobs 7 and 8 are used to scroll through scenes and tracks automatically arming them (I use exclusive arming). Encoders 1-5 are device parameters and 6th is master volume.

Note that clip fire (launch) uses MIDI out to light up the Pad while playing, this might get in the wrong state if switching to other presets and back but is made to work when scrolling around using encoders 7 and 8, I am looking into making this Asynchronous but if you feel it is slowing down then edit the MIDI_map.py to disable this feature by changing from 1 to 0 for: PADLIGHTSENABLED = 1

Once this is working better, would be implemented for other features like solo and mute, etc.

CC Pads on bank A from 1 to 8 are: Overdub on/off, Loop on/off, Clip launch (Record if empty, play if recording, stop if playing), stop all clips, global record, switch clip/track view, metronome on/off, launch current scene.

CC Pads on bank B from 1 to 8: Device lock, blank (change to 68 for Solo), Device left, Device right, Device on/off, blank (change to 72 for Mute), Device bank left, Device bank right.

### Preset 2

This is a preset more focused on a single track at a time, so gives you more control over a single track when you scroll to it.

Encoder knobs 1-8: volume, pan, send-A, send-B, device param 1, master volume, scroll tracks, scroll scenes.

CC Pads Bank-A 1-8: same as preset 1. Overdub on/off, Loop on/off, Clip Fire (Record if empty, play if recording, stop if playing), stop all clips, global record, switch clip/track view, metronome on/off, launch current scene.

CC Pads Bank-B 1-8: track select, track stop, clip launch, stop all clips, select master, arm track, blank (change to 68 in editor to get solo), mute.

### Preset 3

This preset is focused towards a 4 track performance, I know sounds awkward to get much in four tracks but there are not enough controls to get 8 tracks worth. Still might be useful for some or the "Lite" users who don't have many tracks to begin with.

The controls only let you move up and down but if you move the red box prior to loading this preset you can control those tracks.

Encoder knobs 1-4: Volume for tracks 1-4.
Encoder knobs 5-8: Send-A for tracks 1-4.

CC Pads Bank-A 1 and 5: Down and Up for red box.
CC Pads Bank-A 2 and 6: Down and Up for scene selection.
CC Pads Bank-A 3 and 4: Clip launch, Stop all clips.
CC Pads Bank-A 7 and 8: Global record, scene launch.

CC Pads Bank-B 1-4: Mute for tracks 1-4.
CC Pads Bank-B 5-8: Solo for tracks 1-4

# MPK mini SHIFT Script

Uses Preset 4, details as under:

|Control|MIDI CC|Normal|Shift|Alt|
|-------|-------|------|-----|---|
|Encoders 1-4|1,2,3,4|Device Params|Track Vol x4|Blank x4 (Blanks for mapping)|
|Encoders 5-8|5,6,7,8|D-5, M-Vol, Nav x2|Track Send x4|Blank x2, Nav x2|
|Pads 5-8 Bank-B|32,68,34,35|Device R/L x2, toggle, lock|Track Solo x4|Track Select x4|
|Pads 1-4 Bank-B|28,72,30,31|Track Arm x4|Track Mute x4|Scene Launch, ..., Stop All|
|Pads 5-8 Bank-A|26,22,27,23|Metro, Clip, Scene, Stop|Clip launch x4|Track Stop x4|
|Pads 1-4 Bank-A|20,21,Shift,Alt|Overdub, Loop|Sends U/D x2|Track R/L x2|
