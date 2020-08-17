# emacs-mode: -*- python-*-
# -*- coding: utf-8 -*-

import Live
import logging
import math
from _Framework.SessionComponent import SessionComponent
from _Framework import Task
from _Framework.ButtonElement import ButtonElement
from .EncoderElement import EncoderElement
from _Framework.Control import EncoderControl

logger = logging.getLogger(__name__)

class SpecialSessionComponent(SessionComponent):
    " Special SessionComponent for APC combination mode and button to fire selected clip slot "
    __module__ = __name__
    scene_select_encoder = EncoderControl()
    track_select_encoder = EncoderControl()

    def __init__(self, control_surface, num_tracks, num_scenes, cc_type, midi_chan, hscroll, vscroll, padlights_enabled):
        SessionComponent.__init__(self, num_tracks, num_scenes)
        self._arming_task = self._tasks.add(Task.sequence(Task.delay(1), self._arm_task))
        self._arming_task.kill()
        self._slot_launch_button = None
        self._selected_scene_launch_button = None
        self._control_surface = control_surface
        self._padlights_enabled = padlights_enabled
        self._ignore_encoders = False
        self._cliplight = False
        self._track_offset2 = 0
        self._scene_offset2 = 0
        self.set_offsets(0, 0)
        self.on_selected_scene_changed()
        self.on_selected_track_changed()
        self._midi_chan = midi_chan
        self._cc_type = cc_type
        self._hscroll = hscroll
        self._vscroll = vscroll
        if (midi_chan != -1 and cc_type != -1):
            if (vscroll != -1): self.scene_select_encoder.set_control_element(EncoderElement(cc_type, midi_chan, vscroll, Live.MidiMap.MapMode.relative_smooth_two_compliment, name=u'Vertical_Scroll_Encoder'))
            if (hscroll != -1): self.track_select_encoder.set_control_element(EncoderElement(cc_type, midi_chan, hscroll, Live.MidiMap.MapMode.relative_smooth_two_compliment, name=u'Horizontal_Scroll_Encoder'))

    def set_ignore_encoders(self, ignore):
        self._ignore_encoders = ignore

        if ignore:
            self.scene_select_encoder.set_control_element(None)
            self.track_select_encoder.set_control_element(None)
        else:
            if (self._midi_chan != -1 and self._cc_type != -1):
                if (self._vscroll != -1): self.scene_select_encoder.set_control_element(EncoderElement(self._cc_type, self._midi_chan, self._vscroll, Live.MidiMap.MapMode.relative_smooth_two_compliment, name=u'Vertical_Scroll_Encoder'))
                if (self._hscroll != -1): self.track_select_encoder.set_control_element(EncoderElement(self._cc_type, self._midi_chan, self._hscroll, Live.MidiMap.MapMode.relative_smooth_two_compliment, name=u'Horizontal_Scroll_Encoder'))


    def set_scene_select_control(self, control):
        self.scene_select_encoder.set_control_element(control)

    def set_track_select_control(self, control):
        self.track_select_encoder.set_control_element(control)

    @scene_select_encoder.value
    def scene_select_encoder(self, value, encoder):
        if not self._ignore_encoders:
            all_scenes = self.song().scenes
            idx = int(math.floor((float(value)/127)*(float(len(all_scenes))-1.0)))
            self._scene_offset2 = idx
            #logger.info(u'Scene Encoder: ' + str(value) + ', ' + str(idx))
            self.song().view.selected_scene = all_scenes[idx]
            self.on_selected_scene_changed()
            self.clipslot_updated()

    @track_select_encoder.value
    def track_select_encoder(self, value, encoder):
        if not self._ignore_encoders:
            all_tracks = self.song().tracks
            idx = int(math.floor((float(value)/127)*(float(len(all_tracks))-1.0)))
            selected_track = all_tracks[idx]
            self.song().view.selected_track = selected_track
            self.on_selected_track_changed()
            self._track_offset2 = idx
            self.set_offsets(idx, self._scene_offset) # --move scene redbox with navigation-- 
            self.clipslot_updated()


    def on_selected_scene_changed(self):
        super(SessionComponent, self).on_selected_scene_changed()
        #all_scenes = list(self.song().scenes)
        #selected_scene = self.song().view.selected_scene
        if self._track_offset >=0 and self._scene_offset >=0: self.set_offsets(self._track_offset2, self._scene_offset2) # --move scene redbox with navigation-- 

    def on_selected_track_changed(self):
        super(SessionComponent, self).on_selected_track_changed()
        selected_track = self.song().view.selected_track
        all_tracks = self.song().tracks
        self._start_arming_task()
        
        # TODO: selected_track.set_arm_button, etc
        #if self._control_surface._mixer != None:
            #strip = self._control_surface._mixer.channel_strip(current_index)
            #strip.set_arm_button = self._track_controls[0]
            #strip.set_volume_control = self._track_controls[1]
        #all_tracks = list(self.song().tracks)
        #selected_track = self.song().view.selected_track
        #if selected_track in tracks:
        #    track_index = tracks.index(selected_track)

    def clipslot_updated(self):
        if self._padlights_enabled:
            playing = self.song().view.highlighted_clip_slot.is_playing
            if not playing and self._cliplight:
                self._control_surface.padlights_switch(3, 1)
                self._cliplight = False
            elif playing and not self._cliplight:
                self._control_surface.padlights_switch(3, 2)
                self._cliplight = True

    def disconnect(self):
        SessionComponent.disconnect(self)
        if (self._slot_launch_button != None):
            self._slot_launch_button.remove_value_listener(self._slot_launch_value)
            self._slot_launch_button = None
        if (self._selected_scene_launch_button != None):
            self._selected_scene_launch_button.remove_value_listener(self._selected_scene_launch_value)
            self._slot_launch_button = None

    def link_with_track_offset(self, track_offset, scene_offset):
        assert (track_offset >= 0)
        assert (scene_offset >= 0)
        if self._is_linked():
            self._unlink()
        self.set_offsets(track_offset, scene_offset)
        self._link()


    def unlink(self):
        if self._is_linked():
            self._unlink()

    def set_selected_scene_launch_button(self, button):
        assert ((button == None) or isinstance(button, ButtonElement))
        if (self._selected_scene_launch_button != button):
            if (self._selected_scene_launch_button != None):
                self._selected_scene_launch_button.remove_value_listener(self._selected_scene_launch_value)
            self._selected_scene_launch_button = button
            if (self._selected_scene_launch_button != None):
                self._selected_scene_launch_button.add_value_listener(self._selected_scene_launch_value)

            self.update()

    def _selected_scene_launch_value(self, value):
        assert (value in range(128))
        assert (self._slot_launch_button != None)
        if self.is_enabled() and not self.song().view.selected_scene.is_empty:
                self.song().view.selected_scene.fire_as_selected()

    def set_slot_launch_button(self, button):
        assert ((button == None) or isinstance(button, ButtonElement))
        if (self._slot_launch_button != button):
            if (self._slot_launch_button != None):
                self._slot_launch_button.remove_value_listener(self._slot_launch_value)
            self._slot_launch_button = button
            if (self._slot_launch_button != None):
                self._slot_launch_button.add_value_listener(self._slot_launch_value)

            self.update()

    def _slot_launch_value(self, value):
        assert (value in range(128))
        assert (self._slot_launch_button != None)
        if self.is_enabled() and self.song().view.selected_track.arm:
            if (self.song().view.highlighted_clip_slot != None) and \
            (self.song().view.highlighted_clip_slot.is_playing) and \
            not (self.song().view.highlighted_clip_slot.is_recording):
                self.song().view.highlighted_clip_slot.stop()
                #self._slot_launch_button.turn_off()
                self._control_surface.padlights_switch(3, 1)
            elif ((value != 0) or (not self._slot_launch_button.is_momentary())):
                if (self.song().view.highlighted_clip_slot != None):
                    self.song().view.highlighted_clip_slot.fire()
                    #self._slot_launch_button.turn_on()
                    self._control_surface.padlights_switch(3, 2)


    def _start_arming_task(self):
        if self._arming_task.is_killed:
            self._arming_task.restart()


    def _track_to_arm(self):
        track = self.song().view.selected_track
        # can_arm_track = track != None and track.has_midi_input and track.can_be_armed and not track.arm
        can_arm_track = track != None and track.can_be_armed and not track.arm
        if can_arm_track:
            return track


    def _try_arm(self):
        track_to_arm = self._track_to_arm()
        if track_to_arm != None:
            song = self.song()
            tracks = song.tracks
            check_arrangement = song.is_playing and song.record_mode
            if song.exclusive_arm:
                for track in tracks:
                    if track.can_be_armed and track != track_to_arm:
                        track.arm = False

            track_to_arm.arm = True
            track_to_arm.view.select_instrument()

    def _arm_task(self, delta):
        result_state = Task.KILLED
        if self.is_enabled():
            self._try_arm()
        return result_state


# local variables:
# tab-width: 4
