# emacs-mode: -*- python-*-
# -*- coding: utf-8 -*-

import Live
import logging
import math
from _Framework.SessionComponent import SessionComponent
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
        self._slot_launch_button = None
        self._selected_scene_launch_button = None
        self._control_surface = control_surface
        self._padlights_enabled = padlights_enabled
        self._cliplight = False
        self.set_offsets(0, 0)
        self.on_selected_scene_changed()
        self.on_selected_track_changed()
        if (midi_chan != -1 and cc_type != -1):
            if (vscroll != -1): self.scene_select_encoder.set_control_element(EncoderElement(cc_type, midi_chan, vscroll, Live.MidiMap.MapMode.relative_smooth_two_compliment, name=u'Vertical_Scroll_Encoder'))
            if (hscroll != -1): self.track_select_encoder.set_control_element(EncoderElement(cc_type, midi_chan, hscroll, Live.MidiMap.MapMode.relative_smooth_two_compliment, name=u'Horizontal_Scroll_Encoder'))

    def set_scene_select_control(self, control):
        self.scene_select_encoder.set_control_element(control)

    def set_track_select_control(self, control):
        self.track_select_encoder.set_control_element(control)

    @scene_select_encoder.value
    def scene_select_encoder(self, value, encoder):
        all_scenes = self.song().scenes
        idx = int(math.floor((float(value)/127)*(float(len(all_scenes))-1.0)))
        #logger.info(u'Scene Encoder: ' + str(value) + ', ' + str(idx))
        self.song().view.selected_scene = all_scenes[idx]
        self.on_selected_scene_changed()
        self.clipslot_updated()

        u"""
        self._control_surface.send_midi((144,  9, 127))
        self._control_surface.send_midi((144, 10, 127))
        self._control_surface.send_midi((144, 11, 127))
        self._control_surface.send_midi((144, 12, 127))
        self._control_surface.send_midi((144, 13, 127))
        self._control_surface.send_midi((144, 14, 127))
        self._control_surface.send_midi((144, 15, 127))
        self._control_surface.send_midi((144, 16, 127))
        """
        #if abs(value) > 0:
            #selected_scene = self.song().view.selected_scene
            #all_scenes = self.song().scenes
            #current_index = list(all_scenes).index(selected_scene)
            #if value > 0 and selected_scene != all_scenes[-1]:
                #self.song().view.selected_scene = all_scenes[current_index + 1]
            #elif value < 0 and selected_scene != all_scenes[0]:
                #self.song().view.selected_scene = all_scenes[current_index - 1]
        

    @track_select_encoder.value
    def track_select_encoder(self, value, encoder):
        all_tracks = self.song().tracks
        idx = int(math.floor((float(value)/127)*(float(len(all_tracks))-1.0)))
        selected_track = all_tracks[idx]
        self.song().view.selected_track = selected_track
        self.on_selected_track_changed()
        self.clipslot_updated()

        # if abs(value) > 0:
        #     song = self.song()
        #     selected_track = song.view.selected_track
        #     all_tracks = song.tracks
        #     current_index = list(all_tracks).index(selected_track)
        #     if value > 0 and selected_track != all_tracks[-1]:
        #         song.view.selected_track = all_tracks[current_index + 1]
        #     elif value < 0 and selected_track != all_tracks[0]:
        #         song.view.selected_track = all_tracks[current_index - 1]
        #     selected_track = song.view.selected_track
        #     if song.exclusive_arm:
        #         for track in all_tracks:
        #             if track.can_be_armed and track.arm and track != selected_track:
        #                 track.arm = False
        #     selected_track.arm = True


    def on_selected_scene_changed(self):
        super(SessionComponent, self).on_selected_scene_changed()
        #all_scenes = list(self.song().scenes)
        #selected_scene = self.song().view.selected_scene

    def on_selected_track_changed(self):
        super(SessionComponent, self).on_selected_track_changed()
        selected_track = self.song().view.selected_track
        all_tracks = self.song().tracks
        current_index = list(all_tracks).index(selected_track)
        self.set_offsets(current_index, self._scene_offset)
        if self.song().exclusive_arm:
            for track in all_tracks:
                if track.can_be_armed and track.arm and track != selected_track:
                    track.arm = False
        if selected_track.can_be_armed: selected_track.arm = True
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
                self._control_surface.padlights_switch(3, 1)
            elif ((value != 0) or (not self._slot_launch_button.is_momentary())):
                if (self.song().view.highlighted_clip_slot != None):
                    self.song().view.highlighted_clip_slot.fire()
                    self._control_surface.padlights_switch(3, 2)

# local variables:
# tab-width: 4
