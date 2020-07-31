#
# TODO: 
#   1. implement Async for send_midi
#   2. improve encoder logic to use slow relative
#

from __future__ import with_statement

import Live
from _Framework.ControlSurface import ControlSurface
from _Framework.InputControlElement import *
from _Framework.SliderElement import SliderElement
from _Framework.ButtonElement import ButtonElement
from _Framework.ButtonMatrixElement import ButtonMatrixElement
from _Framework.ChannelStripComponent import ChannelStripComponent
from _Framework.DeviceComponent import DeviceComponent
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent
from _Framework.SessionZoomingComponent import SessionZoomingComponent
from SpecialMixerComponent import SpecialMixerComponent
from SpecialTransportComponent import SpecialTransportComponent
from SpecialSessionComponent import SpecialSessionComponent
from SpecialZoomingComponent import SpecialZoomingComponent
from SpecialViewControllerComponent import DetailViewControllerComponent
import threading
import time
from MIDI_Map import *
#MIDI_NOTE_TYPE = 0
#MIDI_CC_TYPE = 1
#MIDI_PB_TYPE = 2

class MPK_mini_tazz(ControlSurface):
    __doc__ = " Script for MPK_mini_tazz in APC emulation mode "

    _active_instances = []
    def _combine_active_instances():
        track_offset = 0
        scene_offset = 0
        for instance in MPK_mini_tazz._active_instances:
            instance._activate_combination_mode(track_offset, scene_offset)
            track_offset += instance._session.width()
    _combine_active_instances = staticmethod(_combine_active_instances)

    def __init__(self, c_instance):
        ControlSurface.__init__(self, c_instance)
        #self.set_suppress_rebuild_requests(True)
        self.__c_instance = c_instance
        with self.component_guard():
            self._note_map = []
            self._ctrl_map = []
            self._load_MIDI_map()
            self._session = None
            self._session_zoom = None
            self._mixer = None
            self._setup_session_control()
            self._setup_mixer_control()
            self._session.set_mixer(self._mixer)
            self._setup_device_and_transport_control()
            self.set_highlighting_session_component(self._session)
            #self.set_suppress_rebuild_requests(False)
        self._pads = []
        self._load_pad_translations()
        self._do_combine()
        #self._horizontal_scroll_encoder = EncoderElement(MIDI_CC_TYPE, 0, 123, Live.MidiMap.MapMode.relative_smooth_two_compliment, name=u'Horizontal_Scroll_Encoder')
        #self._vertical_scroll_encoder = EncoderElement(MIDI_CC_TYPE, 0, 7, Live.MidiMap.MapMode.relative_smooth_two_compliment, name=u'Vertical_Scroll_Encoder')


    def send_midi(self, midi_event_bytes):
        u"""Use this function to send MIDI events through Live to the _real_ MIDI devices
        that this script is assigned to.
        """
        try:
            self._c_instance.send_midi(midi_event_bytes)
        except:
            self.log_message(u'MPKTAZZ: Error while sending midi message', midi_event_bytes)
            #traceback.print_exc()
            return False
        return True

    u"""def _send_midi2(self, midi_event_bytes, optimized = True):
        u" ""
        Script -> Live
        Use this function to send MIDI events through Live to the
        _real_ MIDI devices that this script is assigned to.
        
        When optimized=True it is assumed that messages can be
        dropped -- only the last message within an update for a
        given (channel, key) has visible effects.
        "" "
        if self._accumulate_midi_messages:
            sysex_status_byte = 240
            entry = (self._midi_message_count, midi_event_bytes)
            if optimized and midi_event_bytes[0] != sysex_status_byte:
                self._midi_message_dict[midi_event_bytes[0], midi_event_bytes[1]] = entry
            else:
                self._midi_message_list.append(entry)
            self._midi_message_count += 1
        else:
            self._do_send_midi(midi_event_bytes)
        return True
        """


    def disconnect(self):
        #self._padlights_info["stop"] = True
        #if self._padlights_thread != None and self._padlights_thread.is_alive():
            #self._padlights_thread.join()
        self._session.disconnect()
        self._session_zoom.disconnect()
        self._mixer.disconnect()
        self._device.disconnect()
        self._note_map = None
        self._ctrl_map = None
        self._pads = None
        self._do_uncombine()
        self._shift_button = None
        self._session = None
        self._session_zoom = None
        self._mixer = None
        ControlSurface.disconnect(self)


    def _do_combine(self):
        if self not in MPK_mini_tazz._active_instances:
            MPK_mini_tazz._active_instances.append(self)
            MPK_mini_tazz._combine_active_instances()


    def _do_uncombine(self):
        if ((self in MPK_mini_tazz._active_instances) and MPK_mini_tazz._active_instances.remove(self)):
            self._session.unlink()
            MPK_mini_tazz._combine_active_instances()


    def _activate_combination_mode(self, track_offset, scene_offset):
        if TRACK_OFFSET != -1:
            track_offset = TRACK_OFFSET
        if SCENE_OFFSET != -1:
            scene_offset = SCENE_OFFSET
        self._session.link_with_track_offset(track_offset, scene_offset)


    def _setup_session_control(self):
        is_momentary = True
        self._session = SpecialSessionComponent(self, TRACK_NUM, SCENE_NUM, MESSAGETYPE, SLIDERCHANNEL, HSCROLLENCODER, VSCROLLENCODER, PADLIGHTSENABLED==1)
        self._session.name = 'Session_Control'
        self._session.set_track_bank_buttons(self._note_map[SESSIONRIGHT], self._note_map[SESSIONLEFT])
        self._session.set_scene_bank_buttons(self._note_map[SESSIONDOWN], self._note_map[SESSIONUP])
        self._session.set_select_buttons(self._note_map[SCENEDN], self._note_map[SCENEUP])
        self._scene_launch_buttons = [self._note_map[SCENELAUNCH[index]] for index in range(SCENE_NUM) ]
        self._track_stop_buttons = [self._note_map[TRACKSTOP[index]] for index in range(TRACK_NUM) ]
        self._session.set_stop_all_clips_button(self._note_map[STOPALLCLIPS])
        self._session.set_stop_track_clip_buttons(tuple(self._track_stop_buttons))
        self._session.selected_scene().name = 'Selected_Scene'
        #self._session.selected_scene().set_launch_button(self._note_map[SELSCENELAUNCH])
        self._session.set_selected_scene_launch_button(self._note_map[SELSCENELAUNCH])
        self._session.set_slot_launch_button(self._note_map[SELCLIPLAUNCH])
        #self._session.set_scene_select_control(self._vertical_scroll_encoder)
        for scene_index in range(SCENE_NUM):
            scene = self._session.scene(scene_index)
            scene.name = 'Scene_' + str(scene_index)
            button_row = []
            scene.set_launch_button(self._scene_launch_buttons[scene_index])
            scene.set_triggered_value(SCENE_NUM)
            for track_index in range(TRACK_NUM):
                button = self._note_map[CLIPNOTEMAP[scene_index][track_index]]
                button_row.append(button)
                clip_slot = scene.clip_slot(track_index)
                clip_slot.name = str(track_index) + '_Clip_Slot_' + str(scene_index)
                clip_slot.set_launch_button(button)
        self._session_zoom = SpecialZoomingComponent(self._session)
        self._session_zoom.name = 'Session_Overview'
        self._session_zoom.set_nav_buttons(self._note_map[ZOOMUP], self._note_map[ZOOMDOWN], self._note_map[ZOOMLEFT], self._note_map[ZOOMRIGHT])

    def _setup_mixer_control(self):
        is_momentary = True
        self._mixer = SpecialMixerComponent(TRACK_NUM)
        self._mixer.name = 'Mixer'
        self._mixer.master_strip().name = 'Master_Channel_Strip'
        self._mixer.master_strip().set_select_button(self._note_map[MASTERSEL])
        self._mixer.selected_strip().name = 'Selected_Channel_Strip'
        self._mixer.set_select_buttons(self._note_map[TRACKRIGHT], self._note_map[TRACKLEFT])
        self._mixer.set_crossfader_control(self._ctrl_map[CROSSFADER])
        self._mixer.set_prehear_volume_control(self._ctrl_map[CUELEVEL])
        self._mixer.master_strip().set_volume_control(self._ctrl_map[MASTERVOLUME])
        for track in range(TRACK_NUM):
            strip = self._mixer.channel_strip(track)
            strip.name = 'Channel_Strip_' + str(track)
            strip.set_arm_button(self._note_map[TRACKARM[track]])
            strip.set_solo_button(self._note_map[TRACKSOLO[track]])
            strip.set_mute_button(self._note_map[TRACKMUTE[track]])
            strip.set_select_button(self._note_map[TRACKSEL[track]])
            strip.set_volume_control(self._ctrl_map[TRACKVOL[track]])
            strip.set_pan_control(self._ctrl_map[TRACKPAN[track]])
            strip.set_send_controls((self._ctrl_map[TRACKSENDA[track]], self._ctrl_map[TRACKSENDB[track]], self._ctrl_map[TRACKSENDC[track]]))
            strip.set_invert_mute_feedback(True)


    def _setup_device_and_transport_control(self):
        is_momentary = True
        self._device = DeviceComponent()
        self._device.name = 'Device_Component'
        device_bank_buttons = []
        device_param_controls = []
        for index in range(DEVICE_NUM):
            device_param_controls.append(self._ctrl_map[PARAMCONTROL[index]])
            device_bank_buttons.append(self._note_map[DEVICEBANK[index]])
        if None not in device_bank_buttons:
            self._device.set_bank_buttons(tuple(device_bank_buttons))
        if None not in device_param_controls:
            self._device.set_parameter_controls(tuple(device_param_controls))
        self._device.set_on_off_button(self._note_map[DEVICEONOFF])
        self._device.set_bank_nav_buttons(self._note_map[DEVICEBANKNAVLEFT], self._note_map[DEVICEBANKNAVRIGHT])
        self._device.set_lock_button(self._note_map[DEVICELOCK])
        self.set_device_component(self._device)

        detail_view_toggler = DetailViewControllerComponent()
        detail_view_toggler.name = 'Detail_View_Control'
        detail_view_toggler.set_device_clip_toggle_button(self._note_map[CLIPTRACKVIEW])
        detail_view_toggler.set_detail_toggle_button(self._note_map[DETAILVIEW])
        detail_view_toggler.set_device_nav_buttons(self._note_map[DEVICENAVLEFT], self._note_map[DEVICENAVRIGHT] )

        transport = SpecialTransportComponent()
        transport.name = 'Transport'
        transport.set_play_button(self._note_map[PLAY])
        transport.set_stop_button(self._note_map[STOP])
        transport.set_record_button(self._note_map[REC])
        transport.set_nudge_buttons(self._note_map[NUDGEUP], self._note_map[NUDGEDOWN])
        transport.set_undo_button(self._note_map[UNDO])
        transport.set_redo_button(self._note_map[REDO])
        transport.set_tap_tempo_button(self._note_map[TAPTEMPO])
        transport.set_quant_toggle_button(self._note_map[RECQUANT])
        transport.set_overdub_button(self._note_map[OVERDUB])
        transport.set_metronome_button(self._note_map[METRONOME])
        transport.set_tempo_control(self._ctrl_map[TEMPOCONTROL])
        transport.set_loop_button(self._note_map[LOOP])
        transport.set_seek_buttons(self._note_map[SEEKFWD], self._note_map[SEEKRWD])
        transport.set_punch_buttons(self._note_map[PUNCHIN], self._note_map[PUNCHOUT])
        ##transport.set_song_position_control(self._ctrl_map[SONGPOSITION]) #still not implemented as of Live 8.1.6


    def _on_selected_track_changed(self):
        ControlSurface._on_selected_track_changed(self)
        track = self.song().view.selected_track
        device_to_select = track.view.selected_device
        if device_to_select == None and len(track.devices) > 0:
            device_to_select = track.devices[0]
        if device_to_select != None:
            self.song().view.select_device(device_to_select)
        self._device_component.set_device(device_to_select)


    def _load_pad_translations(self):
        if -1 not in DRUM_PADS:
            pad = []
            for row in range(4):
                for col in range(4):
                    pad = (col, row, DRUM_PADS[row*4 + col], PADCHANNEL,)
                    self._pads.append(pad)
            self.set_pad_translations(tuple(self._pads))


    def padlights_switch(self, pad_num, state):
        if PADLIGHTSENABLED==1 and pad_num <= PADCOUNT:
            value = PADLIGHTOFF if (state==1) else PADLIGHTON
            time.sleep(0.2)
            self.send_midi((PADLIGHTMSG, PADOFFSET+pad_num, value))

            #info = {"pad_num": pad_num, "state": state}
            #threading.Thread(target=self.padlights_worker, args=(info,)).start()
            #self._padlights[pad_num-1] = state
            #if self._padlights_thread is None:
                #self._padlights_thread = threading.Thread(target=self.padlights_worker, args=(self._padlights_info,))
                #self._padlights_thread.start()


    u"""
    def padlights_worker(self, args):
        pad = args["pad_num"]
        state = args["state"]
        value = 0 if (state==1 or (state==3 and not self._padlights_blink_on)) else 127
        time.sleep(0.15)
        self.send_midi((PADLIGHTMSG, PADOFFSET+pad, value))
        while not args["stop"]:
            #self.log_message(u'MPKTAZZ: 7')
            self._padlights_blink_on = not self._padlights_blink_on
            #self.log_message(u'MPKTAZZ: 1', self._padlights_blink_on)
            for pad in range(PADCOUNT):
                state = self._padlights[pad]
                value = 0 if (state==1 or (state==3 and not self._padlights_blink_on)) else 127
                #self.log_message(u'MPKTAZZ: 2-', pad, ":", state, "=>", value)
                self.send_midi((PADLIGHTMSG, PADOFFSET+pad, value))
            time.sleep(0.1)
    """

    def _load_MIDI_map(self):
        is_momentary = True
        for note in range(128):
            button = ButtonElement(is_momentary, MESSAGETYPE, BUTTONCHANNEL, note)
            button.name = 'Note_' + str(note)
            self._note_map.append(button)
        self._note_map.append(None) #add None to the end of the list, selectable with [-1]
        if False: #MESSAGETYPE == MIDI_CC_TYPE and BUTTONCHANNEL == SLIDERCHANNEL:
            for ctrl in range(128):
                self._ctrl_map.append(None)
        else:
            for ctrl in range(128):
                control = SliderElement(MIDI_CC_TYPE, SLIDERCHANNEL, ctrl)
                control.name = 'Ctrl_' + str(ctrl)
                self._ctrl_map.append(control)
            self._ctrl_map.append(None)
