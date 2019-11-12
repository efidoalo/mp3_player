#=======================================
#
#  File: Mp3Player.py
#
#  Content: The core MP3Player class
#  that is used to play mp3 files
#  and to do other operations on them
#  such as pause, stop, get_position,
#  set_position, etc.
#
#  Date: 20/10/2019
#
#  Author: Andy Oldham
#
#=======================================

import vlc   # use the vlc python module for mp3 functionality
import time

class Mp3Player:
    
    def __init__(self, mp3_filename, 
                 filepath_prefix="/home/andy/Documents/projects/mp3_player/songs/"):
        mp3_filepath = filepath_prefix + mp3_filename
        self.mp3_name = mp3_filename
        self.mp3_player = vlc.MediaPlayer(mp3_filepath)
        self.play()
        vlc.libvlc_audio_set_volume(self.mp3_player, 0)
        time.sleep(1) 
        self.len = vlc.libvlc_media_player_get_length(self.mp3_player)
        self.stop()

    def get_mp3_name(self):
        return self.mp3_name

    def play(self):
        self.mp3_player.play()
     
    def pause(self):
        self.mp3_player.pause()

    def stop(self):
        self.mp3_player.stop()

    # return the length of the mp3 file in ms (milliseconds)
    def get_len(self):
        return self.len

    # returns the current time (in ms) of the mp3 file being played or paused 
    # . returns -1 if there is no media (ie if the mp3 has been stopped)
    def get_time(self):
        return vlc.libvlc_media_player_get_time(self.mp3_player)

    # set the time of the current song being played (or paused) in ms.
    # this function has no effect when no mp3 file is being played (ie when an
    # mp3 file has been stopped).
    def set_time(self, time_in_ms):
        vlc.libvlc_media_player_set_time(self.mp3_player, time_in_ms)

    # get_pos and set_pos shouldn't be needed but are implemented just in case
    #
    # returns the position of the mp3 file (weather it is being played or 
    # paused) as a percentage between 0.0 and 1.0
    # returns -1.0 on error or if get_pos is being called on a stopped mp3 file
    def get_pos(self):
        return vlc.libvlc_media_player_get_position(self.mp3_player)
    
    # sets the position of the current mp3 file if it is playing or paused.
    # this function has no effect if the mp3 file has been stopped (the mp3
    # file remains at 0 percent)
    def set_pos(self, percentage):
        vlc.libvlc_media_player_set_position(self.mp3_player, percentage)



