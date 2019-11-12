#!/usr/bin/python3.7
#===============================================
#
#  File: Playlists.py
#
#  Content: Module that supports playing,
#  creation, editing, and deletion of playlists
#  . The playlists are listed in the file named
#  playlists.
#
#  Date: 29/10/2019
#
#  Author: Andy Oldham
#
#===============================================

# function that returns a list of all playlist names
# in the "playlists" file. If the "playlists" file contains no playlists
# an empty list is returned.
# 
def list_all_playlists():
    with open("playlists","r") as f:
        playlists_file = f.read()
        playlists_list = []
        if (playlists_file == ""):
            return playlists_list  # playlists file contains no playlists
        single_newline_pos_index = playlists_file.find("\n")

        # if "playlists" file contains 1 empty playlist
        if single_newline_pos_index == -1: 
           playlists_list.append(playlists_file)
           return playlists_list

        first_playlist_name = playlists_file[0:single_newline_pos_index]
        playlists_list.append(first_playlist_name)
        while (True):
            curr_start_index = single_newline_pos_index #+ 1
            double_newline_pos_index = playlists_file.find("\n\n", 
                                            curr_start_index )
            if double_newline_pos_index == -1:
                break
            single_newline_pos_index = playlists_file.find("\n",
                                         double_newline_pos_index + 2)
            if single_newline_pos_index == -1: # last playlist in file is empty
                last_playlist_name = playlists_file[double_newline_pos_index+2:]
                playlists_list.append(last_playlist_name)
                return playlists_list

            playlist_name = playlists_file[double_newline_pos_index+2:single_newline_pos_index]
            playlists_list.append(playlist_name)
        return playlists_list


# appends to the playlists file named "playlist" the new playlist
# to be created. input arguemnents playlist_name is a string giving
# the new playlist name and and songs_list is a list of song names
# that constitutes the playlist. The song names in songs_list must
# all be found in the /home/andy/Documents/projects/mp3_player/songs
# directory. If a playlist already exists with the name playlist_name in the 
# "playlists" file, this function returns -1
def create_new_playlist(playlist_name, songs_list):
    playlists_has_content = 0
    with open("playlists","r+") as f:
        content = f.read()

        # check for playlist_name already in file and return from function
        # if it is already there returning a value of -1
        f.seek(0,0)
        playlists_list = f.readlines()
        if (len(playlists_list) > 0):
            playlist_name_already_exists = 0
            if playlists_list[len(playlists_list)-1] == playlist_name:
                playlist_name_already_exists = 1
            playlist_name_locate_string_at_first_line = playlist_name + "\n"
            if playlists_list[0] == playlist_name_locate_string_at_first_line:
                playlist_name_already_exists = 1
            playlist_name_locator = "\n\n" + playlist_name + "\n"
            index = content.find(playlist_name_locator)
            if index > -1:
                playlist_name_already_exists = 1
            if playlist_name_already_exists == 1:
                return -1
        ##

        if content != "":
            playlists_has_content = 1
    
        append_to_playlists_string = ""
        if playlists_has_content == 1: 
            append_to_playlists_string = "\n\n"

        append_to_playlists_string += playlist_name
        for song in songs_list:
            curr_song = "\n" + song
            append_to_playlists_string += curr_song
        if playlists_has_content == 1:
            f.seek(0, 2)
            f.write(append_to_playlists_string)
        else:
            f.seek(0, 0)
            f.write(append_to_playlists_string)
            f.truncate()

# Removes a playlist from the "playlists" file. If playlist_name is not found in
# the "playlists" file, this function does nothing
def delete_playlist(playlist_name):
    if playlist_name == "": # do nothing if the playlist name is the empty string
        return
    playlist_name_exists = 0
    with open("playlists", "r+") as f:
        playlists_list = f.readlines()
        if playlists_list[len(playlists_list)-1] == playlist_name:
            playlist_name_exists = 1
        playlist_name_line = playlist_name + "\n"
        playlist_name_line_index = -1
        try:
            playlist_name_line_index = playlists_list.index(playlist_name_line)
        except ValueError:
            playlist_name_line_index = -1
        if playlist_name_line_index > -1:
            playlist_name_exists = 1
        if playlist_name_exists == 0:
            return  # return if the playlist is not found in file "playlists"
        
        playlist_is_last_in_file = 0
        if playlists_list[len(playlists_list)-1] == playlist_name:
            playlist_is_last_in_file = 1

        if playlist_is_last_in_file == 0:
            playlist_name_line = playlist_name + "\n"
            playlist_name_line_index = playlists_list.index(playlist_name_line)
            newline_str = "\n"
            try:
                newline_index = playlists_list.index(newline_str, 
                                                  playlist_name_line_index)
            except ValueError:
                playlist_is_last_in_file = 1
        
        playlist_names = list_all_playlists()
        number_of_playlists = len(playlist_names)
        
        # if playlist_name is the first and last playlist in the "playlists"
        # file
        if number_of_playlists == 1:
            f.seek(0,0)
            f.truncate() # "playlists" file is now empty (check this code
                         # , f.seek(0,0) followed by f.truncate() makes the file
                         # empty )
        
        # if playlists_name is the last playlist in the file and there are
        # more than 1 playlist in the "playlists" file
        if ( (number_of_playlists > 1) and (playlist_is_last_in_file == 1) ):
            playlist_name_line_index = -1
            eof_playlist_line_index = len(playlists_list) - 1
            if playlists_list[len(playlists_list)-1] == playlist_name:
                playlist_name_line_index = len(playlists_list)-1
            else: # if playlist playlist_name contains songs
                playlist_name_line = playlist_name + "\n"
                playlist_name_line_index = playlists_list.index(
                                               playlist_name_line)
            # delete playlist lines in "playlists" file    
            del playlists_list[playlist_name_line_index:eof_playlist_line_index+1 ]
            
            # delete preceeding newline line
            del playlists_list[len(playlists_list)-1]

            # strip newline character of the last line
            old_end_line = playlists_list[len(playlists_list)-1]
            new_end_line = old_end_line[0:len(old_end_line)-1]
            playlists_list[len(playlists_list)-1] = new_end_line

            # update "playlists" file
            empty_str = ""
            updated_playlists_file = empty_str.join(playlists_list)
            f.seek(0, 0)
            f.write(updated_playlists_file)
            f.truncate()

        # if playlist playlist_name is not the last playlist in the file
        if ( (number_of_playlists > 1) and (playlist_is_last_in_file == 0) ):
            playlist_name_line = playlist_name + "\n"
            newline_string = "\n"
            playlist_name_line_index = playlists_list.index(playlist_name_line)
            newline_string_index = playlists_list.index(newline_string,
                                         playlist_name_line_index)
            
            del playlists_list[playlist_name_line_index:newline_string_index+1]
            empty_str = ""
            updated_playlists_file = empty_str.join(playlists_list)
            f.seek(0, 0)
            f.write(updated_playlists_file)
            f.truncate()

                

        


class Playlist:
    """
     A class that provides playliSt functionality
    """

    def __init__(self, playlist_name):
        self.playlist_name = playlist_name
        self.curr_song_index = 0
        self.songs_list = []
        self.populate_songs_list()

    # Populates self.songs_list with the songs from this playlist.
    # THis function is used internally
    def populate_songs_list(self):
        with open("playlists","r") as f:
            playlists_list = f.readlines()
            f.seek(0, 0)
            playlists_file = f.read()
            # populate songs if the name of the playlist is an empty string
            if self.playlist_name == "":
                
                # populate songs if there is only 1 playlist 
                # in the playlists file
                if playlists_file == "": # if the single playlist has no songs
                    return  
                first_line_is_newline=0
                if playlists_list[0] == "\n":
                    first_line_is_newline = 1
                next_newline_index = -2
                newline_str = "\n"
                try:
                    next_newline_index = playlists_list.index(newline_str, 1)
                except ValueError:
                    next_newline_index = -1
                # if the single playlist has songs
                if ( (first_line_is_newline==1) and (next_newline_index==-1) ):
                    songs_list_with_newlines = playlists_list[1:len(playlists_list)]
                    songs_list = []
                    for i in range(len(songs_list_with_newlines)):
                        curr_song = ""
                        if ( i < (len(songs_list_with_newlines)-1) ):
                            curr_song_with_newline = songs_list_with_newlines[i]
                            curr_song = curr_song_with_newline[0:len(curr_song_with_newline)-1]
                        else:
                            curr_song = songs_list_with_newlines[i]
                        songs_list.append(curr_song)
                    self.songs_list = songs_list
                    return
                ##

                # Populate songs where the playlist with empty name is the first
                # playlist in the playlists file and there are more than 1 
                # playlists in the file 

                # if the first playlist contains no songs return without
                # populating self.songs_list
                # 
                if ( (playlists_list[0]=="\n") and (playlists_list[1]=="\n") ): 
                    return
                # if the first playlist contains songs
                first_line_is_newline = 0
                if (playlists_list[0]=="\n"):
                    first_line_is_newline = 1
                newline_str = "\n"
                newline_line_index = playlists_list.index(newline_str, 1)
                if first_line_is_newline == 1:
                    songs_list_with_newlines = playlists_list[1:newline_line_index]
                    songs_list = []
                    for curr_song_with_newline in songs_list_with_newlines:
                        curr_song = curr_song_with_newline[0:len(curr_song_with_newline)-1]
                        songs_list.append(curr_song)
                    self.songs_list = songs_list
                    return
                ##
 
                # playlist file contains more than 2 playlists and the playlist
                # with empty name is not the first or last playlist
                #
                # if the playlist has no songs, return from this function without
                # populating self.songs_list
                newline_seq_str = "\n\n\n\n"
                prev_playlist_end_pos = playlists_file.find(newline_seq_str)
                if (prev_playlist_end_pos > -1):
                    return
                # if the playlist has songs, populate self.songs
                newline_seq_str = "\n\n\n"
                prev_playlist_end_pos = playlists_file.find(newline_seq_str)
                newline_seq_str = "\n\n"
                end_playlist_pos= playlists_file.find(newline_seq_str, 
                                                    prev_playlist_end_pos+3)
                if end_playlist_pos > -1:
                    playlist_str = playlists_file[prev_playlist_end_pos+3:end_playlist_pos]
                    self.songs_list = playlist_str.split("\n")
                    return
                ##
                
                # the playlist with name being an empty string is the
                # last playlist in the "playlists" file and there are
                # more than 1 playlists in the file
                # 
                # if last playlist doesn't contain any songs return without
                # populating self.songs_list
                if playlists_file[len(playlists_file)-1] == "\n":
                    return
                # if last playlist contains songs populate self.songs_list
                playlists_list_copy = playlists_list.copy()
                playlists_list_copy.reverse()
                newline_str = "\n"
                newline_index = playlists_list_copy.index(newline_str)
                songs_list = []
                for i in range(newline_index-1, -1, -1):
                    curr_song_with_newline = playlists_list_copy[i]
                    curr_song = ""
                    if i>0:
                        curr_song = curr_song_with_newline[0:len(curr_song_with_newline)-1]
                    else:
                        curr_song = curr_song_with_newline
                    songs_list.append(curr_song)
                self.songs_list = songs_list
                return
                ##

            playlist_start_index = playlists_file.find(self.playlist_name)
            first_newline_index = playlists_file.find("\n", 
                                         playlist_start_index)
            if first_newline_index == -1: # playlist is at end of "playlists" 
                return                    # file and is empty

            eof_playlist_double_newline_index = playlists_file.find("\n\n",
                                              first_newline_index )
                                           #  first_newline_index + 1)
            # empty playlist so return without populating self.songs_list
            if first_newline_index == eof_playlist_double_newline_index:
                return
            if (eof_playlist_double_newline_index > -1 ):
                playlist_newline_seperated = playlists_file[first_newline_index+1:eof_playlist_double_newline_index]
                self.songs_list = playlist_newline_seperated.split("\n")
            else:
                playlist_newline_seperated = playlists_file[first_newline_index+1:]
                self.songs_list = playlist_newline_seperated.split("\n")
               
    # Returns the list of songs that makes this playlist. Altering
    # the returned list alters the internal list of songs, so beware of doing 
    # this.
    def get_songs(self):
        return self.songs_list

    # returns the current song name ( self.songs_list[self.curr_song_index] )
    def get_curr_song(self):
        return self.songs_list[self.curr_song_index] 
    
    # returns the next song name (to be played) in the list
    def get_next_song(self):
        self.curr_song_index += 1
        if self.curr_song_index == len(self.songs_list):
            self.curr_song_index = 0
        return self.get_curr_song()
    
    # return the previous song name (to be played) in the list
    def get_prev_song(self):
        self.curr_song_index -= 1
        if self.curr_song_index < 0:
            self.curr_song_index = len(self.songs_list) - 1
        return self.get_curr_song()
 
    # PLAYLIST EDIT FUNCTIONS
    #
    # edit the playlist name. changes the playlist name in the "playlists"
    # file and also changes self.playlist_name
    def edit_playlist_name(self, new_playlist_name):
        with open("playlists", "r+") as f:
            playlist_name_line_to_change = self.playlist_name + "\n"
            new_playlist_name_line = new_playlist_name + "\n"
            playlists_list = f.readlines()

            if len(playlists_list)==0:
                f.seek(0, 0)
                f.write(new_playlist_name)
                f.truncate()

                self.playlist_name = new_playlist_name
                return

            lastline = playlists_list[len(playlists_list)-1]
            #print(str(playlists_list), self.playlist_name)
            if lastline  == self.playlist_name:
              #  print("here", self.playlist_name)
                playlist_name_line_to_change = self.playlist_name
                new_playlist_name_line = new_playlist_name
            
            line_index = playlists_list.index(playlist_name_line_to_change)
            if ( (playlist_name_line_to_change == "\n") or (playlist_name_line_to_change == "") ):
                if playlist_name_line_to_change == "\n":
                    if playlists_list[0] == playlist_name_line_to_change:
                        line_index=0
                    else:
                        for i in range(1, len(playlists_list)-1):
                            if ( (playlists_list[i] == "\n") and
                                  (playlists_list[i+1]=="\n") ):
                                line_index=i+1
                                break
                if playlist_name_line_to_change == "":
                    line_index = len(playlists_list)-1

            if (self.playlist_name == "") and (playlists_list[len(playlists_list)-1]=="\n"):
                playlists_list.append(new_playlist_name)
                seperator=""
                new_playlists_file = seperator.join(playlists_list)

                f.seek(0, 0)
                f.write(new_playlists_file)
                f.truncate()

                self.playlist_name = new_playlist_name
                return

            playlists_list[line_index] = new_playlist_name_line
            
            seperator=""
            new_playlists_file = seperator.join(playlists_list)
            
            f.seek(0, 0)
            f.write(new_playlists_file)
            f.truncate()
            
            self.playlist_name = new_playlist_name
            

    # changes the 0 starting index of song_name to new_index. where new_index is
    # an integer in the interval [0, len(self.songs_list)-1]. The internal
    # songs_list list is ammended and the playlists file is also ammended
    # accordingly. The index of a song is the 0 starting index indicating the 
    # line number after the playlist name in the playlists file, with the first
    # song after the playlist name having index 0, the second index 1, and so 
    # on. This song indexing is also identical to the indexing of 
    # self.songs_list. Function returns -1 if new_index is out of range for 
    # inserting into self.songs_list.
    def edit_song_pos(self, song_name, new_index):
        
        if ( (new_index < 0 ) or (new_index >= len(self.songs_list)) ):
            return -1
        curr_song_index = self.songs_list.index(song_name)
        if curr_song_index == new_index:
            return  # do nothing if the new_index is the same as the songs
                    # current index, ie the songs position isnt being 
                    # changed
        # change the song positions in self.songs_list first
        if (curr_song_index < new_index):
            for i in range(curr_song_index, new_index):
                self.songs_list[i] = self.songs_list[i+1]
            self.songs_list[new_index] = song_name
        else: # if curr_song_index > new_index
            for i in range(curr_song_index, new_index, -1):
                self.songs_list[i] = self.songs_list[i-1]
            self.songs_list[new_index] = song_name

        # write song position changes to file "playlists"
        with open("playlists", "r+") as f:
           
            playlists_list = f.readlines()
            playlist_name_line = self.playlist_name + "\n"
            playlist_name_file_index = playlists_list.index(playlist_name_line)

            last_playlist_indicator = 1
            for i in range(playlist_name_file_index+1, len(playlists_list)):
                if playlists_list[i] == "\n":
                    last_playlist_indicator = 0

            songs_list_length = len(self.songs_list)
            file_input_songs_list = []
            for i in range(len(self.songs_list)):
                curr_song = self.songs_list[i] 
                if ( (i == (len(self.songs_list)-1) ) and 
                        (last_playlist_indicator == 1) ):
                    file_input_songs_list.append(curr_song)
                else:
                    file_input_songs_list.append(curr_song + "\n")

            playlists_list[playlist_name_file_index+1:playlist_name_file_index+songs_list_length+1] = file_input_songs_list

            f.seek(0, 0)
            empty_str = ""
            updated_playlists_file = empty_str.join(playlists_list)
            f.write(updated_playlists_file)
            f.truncate()

    # song_name is an mp3 file in the songs directory. This function appends
    # song_name to the self.songs_list internal list and the playlist file 
    # "playlists" into the end of the relevant playlist.
    def add_new_song(self, song_name):
        self.songs_list.append(song_name)
        with open("playlists", "r+") as f:
            playlists_list = f.readlines()

            # handle the case where the playlist name is an empty strng
            if self.playlist_name == "": 
                
                # if the playlists file contans only 1 playlist which has
                # no songs
                if ( playlists_list == [] ):
                    playlists_file_updated = "\n" + song_name
                    f.seek(0 , 0)
                    f.write(playlists_file_updated)
                    f.truncate()
                    return

                # if the playlist is the only playlist in the "playlists" file
                # and the playlist already contains songs
                playlist_starts_with_newline=0
                if playlists_list[0] == "\n":
                    playlist_starts_with_newline = 1
                playlists_file_has_single_playlist = 0
                newline_str = "\n"
                try:
                    playlists_list.index(newline_str, 1)
                except ValueError:
                    playlists_file_has_single_playlist = 1
                if ( (playlist_starts_with_newline == 1) and
                     (playlists_file_has_single_playlist == 1) ):
                    f.seek(0, 0)
                    old_playlists_file = f.read()
                    updated_playlists_file = old_playlists_file + "\n" + song_name
                    f.seek(0, 0)
                    f.write(updated_playlists_file)
                    f.truncate()
                    return
                
                # if the playlist with empty string name is the first playlist
                # in the "playlists" file and has no songs and where there are 
                # more than 1 playlists in the "playlists" file 
                if ( (playlists_list[0] == "\n") and (playlists_list[1] == "\n") ):
                    new_song_line_str = song_name + "\n"
                    playlists_list.insert(1, new_song_line_str)
                    empty_str = ""
                    updated_playlists_file = empty_str.join(playlists_list)
                    f.seek(0, 0)
                    f.write(updated_playlists_file)
                    f.truncate()
                    return

                # if the playlist with empty string name is the first playlist
                # in the "playlists" file with songs where there are more than
                # one playlists in the "playlists" file
                first_playlist_has_empty_name = 0
                if playlists_list[0] == "\n":
                    first_playlist_has_empty_name = 1
                if first_playlist_has_empty_name == 1:
                    newline_str = "\n"
                    second_newline_index = playlists_list.index(newline_str,1)
                    new_song_line = song_name + "\n"
                    playlists_list.insert(second_newline_index, new_song_line)
                    empty_str = ""
                    updated_playlists_file = empty_str.join(playlists_list)
                    f.seek(0, 0)
                    f.write(updated_playlists_file)
                    f.truncate()
                    return
                
                # if playlist with empty name is the middle playlist (not 1st
                # or last playlist in "playlists" file) with no songs where 
                # there are more than 2 playlists in the "playlists" file
                f.seek(0, 0)
                playlists_file = f.read()
                newline_seq = "\n\n\n\n"
                end_prev_playlist_pos = playlists_file.find(newline_seq)
                start_of_next_playlist_pos = end_prev_playlist_pos+4
                if ( (end_prev_playlist_pos > -1) and (len(playlists_file) > start_of_next_playlist_pos) ):
                    new_song_line = song_name + "\n"
                    updated_playlists_file = playlists_file[0:end_prev_playlist_pos+3] + new_song_line + playlists_file[end_prev_playlist_pos+3:]
                    f.seek(0, 0)
                    f.write(updated_playlists_file)
                    f.truncate()
                    return
                
                # if the playlist with empty string name is the
                # middle playlist (not first or last) in the "playlists" file
                # with songs where there are more than 2 playlists in the
                # "playlists" file
                newline_seq = "\n\n\n"
                end_prev_playlist_pos = playlists_file.find(newline_seq)
                newline_seq = "\n\n"
                end_curr_playlist_pos = -1
                if (end_prev_playlist_pos > -1):
                    end_curr_playlist_pos = playlists_file.find(newline_seq, 
                                               end_prev_playlist_pos+3)
                if ( (end_prev_playlist_pos>-1) and (end_curr_playlist_pos>-1) ):
                    new_song_line = song_name + "\n"
                    updated_playlists_file = playlists_file[0:end_curr_playlist_pos+1] + new_song_line + playlists_file[end_curr_playlist_pos+1:]
                    f.seek(0, 0)
                    f.write(updated_playlists_file)
                    f.truncate()
                    return
            
                # if the playlist with empty string for its name is the
                # last playlist in the "playlists" file with no songs where
                # there is more than 1 playlist in the "playlists" file
                if playlists_list[len(playlists_list)-1] == "\n":
                    playlists_list.append("\n")
                    playlists_list.append(song_name)
                    empty_str = ""
                    updated_playlists_file = empty_str.join(playlists_list)
                    f.seek(0, 0)
                    f.write(updated_playlists_file)
                    f.truncate()
                    return

                # finally, this case must be the case:
                # if the playlist with empty string for its name is the last
                # playlist in the "playlists" file with songs where there is
                # more than 1 playlist in the "playlists" file
                update_previous_last_line = playlists_list[len(playlists_list)-1] + "\n"
                playlists_list[len(playlists_list)-1] = update_previous_last_line
                playlists_list.append(song_name)
                empty_str = ""
                updated_playlists_file = empty_str.join(playlists_list)
                f.seek(0, 0)
                f.write(updated_playlists_file)
                f.truncate()
                return
                

            last_playlist_and_empty = 0
            if playlists_list[len(playlists_list)-1] == self.playlist_name:
                last_playlist_and_empty = 1
            playlist_name_line_index = len(playlists_list)-1
            if last_playlist_and_empty == 0:
                playlist_name_line = self.playlist_name + "\n"
                playlist_name_line_index = playlists_list.index(
                                                playlist_name_line)
            last_playlist_indicator = 1
            for i in range(playlist_name_line_index, len(playlists_list)):
                if playlists_list[i] == "\n":
                    last_playlist_indicator = 0
            if last_playlist_indicator==0:
                newline_str = "\n"
                newline_index = playlists_list.index(newline_str,
                                                  playlist_name_line_index)
                insert_line = song_name + newline_str
                playlists_list.insert(newline_index, insert_line)
            else: # if last_playlist_indicator == 1
                old_last_line = playlists_list[len(playlists_list)-1]
                old_last_line += "\n"
                playlists_list[len(playlists_list)-1] = old_last_line
                playlists_list.append(song_name)
           
            empty_str = ""
            new_playlists_file = empty_str.join(playlists_list)
            f.seek(0,0)
            f.write(new_playlists_file)
            f.truncate()

    # Delete a song from the playlist. Deletes the song from self.songs_list
    # array and also deletes the song from the "playlists" file.
    # if
    def del_song(self, song_name):
        # delete song from internal list
        song_name_index = self.songs_list.index(song_name)
        del self.songs_list[song_name_index]
        
        # delete song from playlist in "playlists" file
        with open("playlists", "r+") as f:
            playlists_list = f.readlines()
            playlist_name_line = self.playlist_name + "\n"
            playlist_name_line_index = playlists_list.index(playlist_name_line)
                                                                    
            song_name_is_last_line = 0
            if playlists_list[len(playlists_list)-1] == song_name:
                song_name_is_last_line = 1
                
            if song_name_is_last_line == 0:
                song_name_line = song_name + "\n"
                song_name_line_index = playlists_list.index(song_name_line,
                                             playlist_name_line_index)
                del playlists_list[song_name_line_index]
            else: # if song_name_is_last_line = 1
                del playlists_list[len(playlists_list)-1]
                new_last_line = playlists_list[len(playlists_list)-1]
                # strip trailing newline character off of last line
                new_last_line_changed = new_last_line[0:len(new_last_line)-1]
                playlists_list[len(playlists_list)-1] = new_last_line_changed
            
            newline_str = ""
            playlists_file_updated = newline_str.join(playlists_list)
            f.seek(0,0)
            f.write(playlists_file_updated)
            f.truncate()

            
if __name__ == "__main__":
    playlists_list = list_all_playlists()
    print(str(playlists_list))
   # playlist1 = Playlist("Example Playlist 2")
   # print(str(playlist1.songs_list))
   # playlist1.edit_playlist_name("Example Playlist 3")  
   # playlist1.edit_song_pos("theshire.mp3", 1)    
   # playlist1.del_song("niky-nine-road.mp3")
   # print(str(playlist1.songs_list))
    print("\n\n")
     
    #curr_song = playlist1.get_curr_song()
    #print(curr_song)
    #curr_song = playlist1.get_prev_song()
    #print(curr_song)
    #curr_song = playlist1.get_prev_song()
    #print(curr_song)
    #curr_song = playlist1.get_prev_song()
    #print(curr_song)
    #curr_song = playlist1.get_prev_song()
    #print(curr_song)

    playlist1 = "Example Playlist 1"
    playlist1_songs = []#"timestalker_street_prowler.mp3",
                       #"niky-nine-road.mp3",
                       #"theshire.mp3"]
    playlist2 = "Example Playlist 2"
    playlist2_songs = ["timestalker_street_prowler.mp3",
                       "compilerbau-death-in-space.mp3",
                       "vector-sector-the-zeta-city-slasher.mp3",
                       "niky-nine-road.mp3"]
    playlist3 = "Example Playlist 3"
    playlist3_songs = ["theshire.mp3",
                       "timestalker_street_prowler.mp3"]
    playlist4 = "Example Playlist 4"
    playlist4_songs = ["theshire.mp3",
                       "vector-sector-the-zeta-city-slasher.mp3",
                       "compilerbau-death-in-space.mp3",
                      "timestalker_street_prowler.mp3"]
    playlist5 = "Example Playlist 5"
    playlist5_songs = ["compilerbau-death-in-space.mp3",
                      "timestalker_street_prowler.mp3"]

    playlist6 = "Example Playlist 6"
    playlist6_songs = []#"theshire.mp3",
                       #"vector-sector-the-zeta-city-slasher.mp3",
                       #"compilerbau-death-in-space.mp3",
                      #"timestalker_street_prowler.mp3",
                     # "niky-nine-road.mp3",
                      #"theshire.mp3",
                      # "vector-sector-the-zeta-city-slasher.mp3",
                      # "compilerbau-death-in-space.mp3",
                      #"timestalker_street_prowler.mp3",
                      #"niky-nine-road.mp3",
                      #"vector-sector-the-zeta-city-slasher.mp3",
                      # "compilerbau-death-in-space.mp3"]
    create_new_playlist(playlist1, playlist1_songs)
    create_new_playlist(playlist2, playlist2_songs)
    create_new_playlist(playlist3, playlist3_songs)
    #create_new_playlist(playlist4, playlist4_songs)
    #create_new_playlist(playlist5, playlist5_songs)
    #create_new_playlist(playlist6, playlist6_songs)

    #playlist_name = "Example Playlist 2"
    #delete_playlist(playlist_name)
