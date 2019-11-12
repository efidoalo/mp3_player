#!/usr/bin/python3.7
#=====================================
#
#  File: mp3_player_app.py
#
#  Content: The main gui frame class
#  that implements the mp3 player.
#
#  Date: 21/10/2019
#
#  Author: Andy Oldham
#
#=====================================

import Mp3Player
import Playlists
import wx
import wx.html2
import os
import math
import re
import vlc
import time
import wx.lib.statbmp

# returns a list of strings (in no partiular order) where each string is a 
# mp3 filename in the songs directory
def get_list_of_songs():
   songs_path = "/home/andy/Documents/projects/mp3_player/songs"
   return os.listdir(songs_path)

class mp3_player_gui(wx.Frame):

    def __init__(self, *args, **kw):
        # ensure the parent's __init__ is called
        super(mp3_player_gui, self).__init__(*args, **kw)
        
        self.mp3_player = self.get_first_song()
        self.current_time = -1

        mainPanel = wx.Panel(self)

        vbox = wx.BoxSizer(wx.VERTICAL)

        hbox1_searchbar = wx.BoxSizer(wx.HORIZONTAL)
        search_text = wx.StaticText(mainPanel, label="Search: ")
        
        hbox1_searchbar.Add(search_text, 
                            0,      # not stretchable horizontally
                            wx.LEFT, 
                            20)
        search_bar_size = wx.Size(250,25)
        self.search_bar = wx.TextCtrl(mainPanel, size=search_bar_size)
        search_bar_font = self.search_bar.GetFont()
        search_bar_font.SetPointSize(9)
        self.search_bar.SetFont(search_bar_font)

        hbox1_searchbar.Add(self.search_bar,  
                                 1, wx.LEFT, 6)

        vbox.Add(hbox1_searchbar,0, wx.TOP, 20)
        
        hbox2_currentsong = wx.BoxSizer(wx.HORIZONTAL)
        curr_song_text = wx.StaticText(mainPanel, label="Current Song: ")
        hbox2_currentsong.Add(curr_song_text, 0, wx.LEFT, 20)

        curr_song_label = self.mp3_player.get_mp3_name()
        self.curr_song = wx.StaticText(mainPanel, label=curr_song_label)
        hbox2_currentsong.Add(self.curr_song, 0, wx.LEFT , 10)

        vbox.Add(hbox2_currentsong, 0, wx.TOP, 10)
        
        progressbar_vleftline = wx.Bitmap("images/left_vertbar_10x15")
        lvline_pos = wx.Point(120,90)
        left_vline_sbm = wx.StaticBitmap(mainPanel, 
                                         bitmap=progressbar_vleftline,
                                         pos=lvline_pos)

        progressbar_vrightline = wx.Bitmap("images/right_vertbar_10x15")
        rvline_pos = wx.Point(470,90)
        right_vline_sbm = wx.StaticBitmap(mainPanel, 
                                          bitmap=progressbar_vrightline,
                                          pos=rvline_pos)

        progressbar_hline = wx.Bitmap("images/horizontal_bar_341x2")
        hline_pos = wx.Point(129, 97)
        hline_sbm = wx.StaticBitmap(mainPanel,
                                     bitmap=progressbar_hline,
                                     pos = hline_pos)

        progress_circle = wx.Bitmap("images/play_circle_10x10")
        progress_circle_pos = wx.Point(124, 93)
        self.progress_circle_sbm = wx.lib.statbmp.GenStaticBitmap(mainPanel,-1,
                                     bitmap=progress_circle,
                                     pos = progress_circle_pos)
        
        progress_timer_pos = wx.Point(126, 104)
        self.progress_timer = wx.StaticText(mainPanel, label="0:00/x:yz",
                                        pos=progress_timer_pos) 

        hbox3_playoptions = wx.BoxSizer(wx.HORIZONTAL)
        prev_button_size = wx.Size(40,28)
        self.prev_button = wx.Button(mainPanel, label="Prev",
                                 size=prev_button_size)

        
        hbox3_playoptions.Add(self.prev_button)

        play_button_size = wx.Size(52, 28)
        self.play_button = wx.Button(mainPanel, label="Play",
                                      size=play_button_size)
        hbox3_playoptions.Add(self.play_button)
        
        stop_button_size = wx.Size(40, 28)
        self.stop_button = wx.Button(mainPanel, label="Stop",
                                  size=stop_button_size)
        hbox3_playoptions.Add(self.stop_button)

        next_button_size = wx.Size(40, 28)
        self.next_button = wx.Button(mainPanel, label="Next",
                                  size=next_button_size)
        hbox3_playoptions.Add(self.next_button)

        vbox.Add(hbox3_playoptions, 0, 
                 wx.ALIGN_CENTER_HORIZONTAL | wx.TOP, 50)


        mainPanel.SetSizer(vbox)
        
        ddsm_size = wx.Size(250,90)
        ddsm_pos = wx.Point(80,45)
        songs = get_list_of_songs()
        self.drop_down_song_menu = wx.ListBox(mainPanel,
                                         size=ddsm_size,
                                         pos=ddsm_pos,
                                         choices=songs,
                                         style=wx.LB_SINGLE | 
                                               wx.LB_NEEDED_SB |
                                               wx.LB_SORT )
        ddsm_font = self.drop_down_song_menu.GetFont()
        ddsm_font.SetPointSize(9)
        self.drop_down_song_menu.SetFont(ddsm_font)
        self.drop_down_song_menu.Show(False)

        self.curr_playlist = "placeholder"
        self.playlist_playing = 0
        self.allow_edit_playlist_name = 0
        self.edit_playlist_song_selected = ""

        ## PLAY PLAYLIST WIDGETS ##
        play_playlist_label_pos = wx.Point(94,164)
        self.play_playlist_label = wx.StaticText(mainPanel, 
                                            label="Select playlist: ",
                                            pos=play_playlist_label_pos)        
        self.play_playlist_label.Hide()

        play_playlist_selector_pos = wx.Point(200, 160)
        play_playlist_selector_size = wx.Size(200, 28)
        playlist_choices = Playlists.list_all_playlists()
        self.play_playlist_selector = wx.ComboBox(mainPanel, 
                                             pos=play_playlist_selector_pos,
                                             size=play_playlist_selector_size,
                                             choices=playlist_choices,
                                             style=wx.CB_READONLY)
        font = self.play_playlist_selector.GetFont()
        font.SetPointSize(9)
        self.play_playlist_selector.SetFont(font)
        self.play_playlist_selector.Hide()

        playlist_songs_pos = wx.Point(200, 188)
        playlist_songs_size = wx.Size(200, 100)
        self.playlist_songs = wx.TextCtrl(mainPanel,
                             pos=playlist_songs_pos,
                             size=playlist_songs_size,
                             style=wx.TE_MULTILINE | wx.TE_READONLY
                                 | wx.HSCROLL)
        self.playlist_songs.Hide()

        play_playlist_button_pos = wx.Point(406, 160)
        play_playlist_button_size = wx.Size(100, 28)
        self.play_playlist_button = wx.Button(mainPanel, label="Play playlist",
                                      size=play_playlist_button_size,
                                      pos = play_playlist_button_pos)
        self.play_playlist_button.Hide()
        ##
        
        ## CREATE PLAYLIST WIDGETS ##
        create_playlist_main_label_pos = wx.Point(251,160)
        self.create_playlist_main_label = wx.StaticText(mainPanel,
                                          label="Create Playlist",
                                          pos=create_playlist_main_label_pos)
        self.create_playlist_main_label.Hide()

        create_playlist_playlist_name_label_pos = wx.Point(100,184)
        self.create_playlist_playlist_name_label = wx.StaticText(mainPanel,
                                          label="Playlist name: ",
                            pos=create_playlist_playlist_name_label_pos)
        self.create_playlist_playlist_name_label.Hide()

        cppni_pos = wx.Point(200, 180)
        cppni_size = wx.Size(200, 25) 
        self.create_playlist_playlist_name_inputbox = wx.TextCtrl(mainPanel,
                                             pos=cppni_pos,
                                             size=cppni_size)
        font = self.create_playlist_playlist_name_inputbox.GetFont()
        font.SetPointSize(9)
        self.create_playlist_playlist_name_inputbox.SetFont(font)
        self.create_playlist_playlist_name_inputbox.Hide()

        create_playlist_playlist_songs_label_pos = wx.Point(98,209)
        self.create_playlist_playlist_songs_label = wx.StaticText(mainPanel,
                                   pos=create_playlist_playlist_songs_label_pos,
                                   label="Playlist songs: ")
        self.create_playlist_playlist_songs_label.Hide()

        create_playlist_playlist_songs_pos = wx.Point(200,205)
        create_playlist_playlist_songs_size = wx.Size(200, 100)
        self.create_playlist_playlist_songs = wx.TextCtrl(mainPanel,
                             pos=create_playlist_playlist_songs_pos,
                           size=create_playlist_playlist_songs_size,
                             style=wx.TE_MULTILINE 
                                 | wx.TE_READONLY | wx.HSCROLL)
        self.create_playlist_playlist_songs.Hide()

        create_playlists_add_song_label_pos = wx.Point(408,184)
        self.create_playlists_add_song_label = wx.StaticText(mainPanel,
                                pos=create_playlists_add_song_label_pos,
                                label="Add song to playlist")
        self.create_playlists_add_song_label.Hide()

        add_song_search_size = wx.Size(180,25)
        add_song_search_pos = wx.Point(408, 202)
        self.add_song_search = wx.TextCtrl(mainPanel, 
                                   size=add_song_search_size,
                                   pos=add_song_search_pos)
        font = self.add_song_search.GetFont()
        font.SetPointSize(9)
        self.add_song_search.SetFont(font)
        self.add_song_search.Hide()

        songs = get_list_of_songs()
        ddasm_size = wx.Size(180,100)
        ddasm_pos = wx.Point(408, 227)
        self.drop_down_add_song_menu = wx.ListBox(mainPanel,
                                         size=ddasm_size,
                                         pos=ddasm_pos,
                                         choices=songs,
                                         style=wx.LB_SINGLE |
                                               wx.LB_NEEDED_SB |
                                               wx.LB_SORT )
        font = self.drop_down_add_song_menu.GetFont()
        font.SetPointSize(9)
        self.drop_down_add_song_menu.SetFont(font)
        self.drop_down_add_song_menu.Hide()
        
        delete_song_button_pos = wx.Point(5, 236)
        delete_song_button_size = wx.Size(190, 25)
        self.delete_song_button = wx.Button(mainPanel,
                                            label="Delete song from playlist",
                                            pos=delete_song_button_pos,
                      size=delete_song_button_size)
        self.delete_song_button.Hide()

        delete_song_drop_down_list_pos = wx.Point(5, 261)
        delete_song_drop_down_list_size = wx.Size(190, 70)
        self.delete_song_drop_down_list = wx.ListBox(mainPanel,
                             pos=delete_song_drop_down_list_pos,
                             size=delete_song_drop_down_list_size)
        self.delete_song_drop_down_list.Hide()

        create_playlist_save_playlist_pos = wx.Point(250 ,310)
        create_playlist_save_playlist_size = wx.Size(100, 25)
        self.create_playlist_save_playlist = wx.Button(mainPanel,
                                    pos=create_playlist_save_playlist_pos,
                                    size=create_playlist_save_playlist_size,
                                    label="Save playlist")
        self.create_playlist_save_playlist.Hide()
        ##

        ## EDIT PLAYLIST WIDGETS ##
        edit_playlist_playlist_selector_label_pos = wx.Point(78, 160)
        self.edit_playlist_playlist_selector_label = wx.StaticText(mainPanel,
                          pos=edit_playlist_playlist_selector_label_pos,
                          label="Select playlist to edit: ")
        self.edit_playlist_playlist_selector_label.Hide()

        edit_playlist_playlist_selector_pos = wx.Point(230, 156)
        edit_playlist_playlist_selector_size = wx.Size(200, 30)
        list_of_playlists = Playlists.list_all_playlists()
        self.edit_playlist_playlist_selector = wx.ComboBox(mainPanel,
                      pos=edit_playlist_playlist_selector_pos,
                      size=edit_playlist_playlist_selector_size,
                      choices=list_of_playlists,
                      style= wx.CB_READONLY |
                             wx.CB_SORT)
        self.edit_playlist_playlist_selector.Hide()

        edit_playlist_playlist_name_label_pos = wx.Point(100, 190)
        self.edit_playlist_playlist_name_label = wx.StaticText(mainPanel,
                                   pos=edit_playlist_playlist_name_label_pos,
                                   label="Edit Playlist name: ")
        self.edit_playlist_playlist_name_label.Hide()

        edit_playlist_playlist_name_pos = wx.Point(230, 186)
        edit_playlist_playlist_name_size = wx.Size(200, 25)
        self.edit_playlist_playlist_name = wx.TextCtrl(mainPanel,
                                   pos=edit_playlist_playlist_name_pos,
                             size=edit_playlist_playlist_name_size)
        font = self.edit_playlist_playlist_name.GetFont()
        font.SetPointSize(9)
        self.edit_playlist_playlist_name.SetFont(font)
        self.edit_playlist_playlist_name.Hide()

        edit_playlist_playlist_songs_label_pos = wx.Point(96, 220)
        self.edit_playlist_playlist_songs_label = wx.StaticText(mainPanel,
                                     pos=edit_playlist_playlist_songs_label_pos,
                                     label="Edit Playlist songs: ")
        self.edit_playlist_playlist_songs_label.Hide()

        edit_playlist_playlist_songs_pos = wx.Point(230, 215)
        edit_playlist_playlist_songs_size = wx.Size(200, 100)
        self.edit_playlist_playlist_songs = wx.TextCtrl(mainPanel,
                                 pos=edit_playlist_playlist_songs_pos,
                                 size=edit_playlist_playlist_songs_size,
                                 style=wx.TE_MULTILINE | 
                                       wx.TE_READONLY |
                                       wx.HSCROLL )
        font = self.edit_playlist_playlist_songs.GetFont()
        font.SetPointSize(9)
        self.edit_playlist_playlist_songs.SetFont(font)
        self.edit_playlist_playlist_songs.Hide()

        # create menu for deletion and moving of songs
        self.edit_menu = wx.Menu()
        self.move_song_options = wx.Menu()
        self.edit_menu.AppendSubMenu(self.move_song_options, "Move song to pos")
        delete_song_item = self.edit_menu.Append(wx.ID_ANY, "Delete song")
        self.edit_menu.Bind(wx.EVT_MENU,
                            self.edit_playlist_delete_song,
                            delete_song_item)
        #

        edit_playlist_add_song_label_pos = wx.Point(440,210)
        self.edit_playlist_add_song_label = wx.StaticText(mainPanel,
                                pos=edit_playlist_add_song_label_pos,
                                label="Add song to playlist")
        self.edit_playlist_add_song_label.Hide()

        edit_playlist_add_song_search_size = wx.Size(150,25)
        edit_playlist_add_song_search_pos = wx.Point(440, 229)
        self.edit_playlist_add_song_search = wx.TextCtrl(mainPanel,
                              size=edit_playlist_add_song_search_size,
                              pos=edit_playlist_add_song_search_pos)
        font = self.edit_playlist_add_song_search.GetFont()
        font.SetPointSize(9)
        self.edit_playlist_add_song_search.SetFont(font)
        self.edit_playlist_add_song_search.Hide()

        songs = get_list_of_songs()
        edit_playlist_add_song_drop_down_menu_size = wx.Size(150,90)
        edit_playlist_add_song_drop_down_menu_pos = wx.Point(440, 254)
        self.edit_playlist_add_song_drop_down_menu = wx.ListBox(mainPanel,
                            size=edit_playlist_add_song_drop_down_menu_size,
                            pos=edit_playlist_add_song_drop_down_menu_pos,    
                            choices=songs,
                            style=wx.LB_SINGLE |
                                               wx.LB_NEEDED_SB |
                                               wx.LB_SORT )
        font = self.edit_playlist_add_song_drop_down_menu.GetFont()
        font.SetPointSize(9)
        self.edit_playlist_add_song_drop_down_menu.SetFont(font)
        self.edit_playlist_add_song_drop_down_menu.Hide()
        
        edit_playlist_finished_editing_button_pos = wx.Point(230,318)
        edit_playlist_finished_editing_button_size = wx.Size(140,25)
        self.edit_playlist_finished_editing_button = wx.Button(mainPanel,
                label="Finished Editing",
                pos=edit_playlist_finished_editing_button_pos,
                size=edit_playlist_finished_editing_button_size)
        self.edit_playlist_finished_editing_button.Hide()
        ##

        ## DELETE PLAYLIST WIDGETS ##
        delete_playlist_label_pos = wx.Point(94,164)
        self.delete_playlist_label = wx.StaticText(mainPanel,
                                            label="Select playlist: ",
                                            pos=delete_playlist_label_pos)
        self.delete_playlist_label.Hide()

        delete_playlist_selector_pos = wx.Point(200, 160)
        delete_playlist_selector_size = wx.Size(200, 28)
        playlist_choices = Playlists.list_all_playlists()
        self.delete_playlist_selector = wx.ComboBox(mainPanel,
                                             pos=delete_playlist_selector_pos,
                                             size=delete_playlist_selector_size,
                                             choices=playlist_choices,
                                             style=wx.CB_READONLY)
        font = self.delete_playlist_selector.GetFont()
        font.SetPointSize(9)
        self.delete_playlist_selector.SetFont(font)
        self.delete_playlist_selector.Hide()

        delete_playlist_songs_pos = wx.Point(200, 188)
        delete_playlist_songs_size = wx.Size(200, 100)
        self.delete_playlist_songs = wx.TextCtrl(mainPanel,
                             pos=delete_playlist_songs_pos,
                             size=delete_playlist_songs_size,
                             style=wx.TE_MULTILINE | wx.TE_READONLY
                                 | wx.HSCROLL)
        self.delete_playlist_songs.Hide()

        delete_playlist_button_pos = wx.Point(406, 160)
        delete_playlist_button_size = wx.Size(110, 28)
        self.delete_playlist_button = wx.Button(mainPanel, label="Delete playlist",
                                      size=delete_playlist_button_size,
                                      pos = delete_playlist_button_pos)
        self.delete_playlist_button.Hide()    
        ##
       
        self.browser = wx.html2.WebView.New()
        browser_pos = wx.Point(50, 160)
        browser_size = wx.Size(500, 150)
        self.browser.Create(mainPanel, 
                            url="http://www.google.com",
                            pos=browser_pos, 
                            size=browser_size)
        #self.browser.LoadURL("http://www.google.com")
        #
        self.createMenuBar()

        self.timer1 = wx.Timer(self) # every hundredth of a second (position 
                                     # progress bar)
        self.timer2 = wx.Timer(self) # every second (check if song has finished
                                     # playing )
        
        self.Bind(wx.EVT_TIMER, self.timer_handler)
       
        self.Bind(wx.EVT_COMBOBOX, self.delete_playlist_selector_handler,
                  self.delete_playlist_selector)
        self.Bind(wx.EVT_BUTTON, self.delete_playlist_handler,
                  self.delete_playlist_button)

        self.Bind(wx.EVT_COMBOBOX, self.edit_playlist_selector_handler,
                  self.edit_playlist_playlist_selector)
        self.Bind(wx.EVT_TEXT, self.edit_playlist_playlist_name_edit_handler,
                  self.edit_playlist_playlist_name)
        self.edit_playlist_playlist_songs.Bind(wx.EVT_ENTER_WINDOW, 
                          self.edit_playlist_mouse_entered_handler)
        self.edit_playlist_playlist_songs.Bind(wx.EVT_RIGHT_DOWN, 
                           self.edit_playlist_song_selected_handler)
        self.edit_playlist_add_song_search.Bind(wx.EVT_LEFT_DOWN,
            self.edit_playlist_add_song_search_bar_left_button_down_handler)
        self.edit_playlist_add_song_search.Bind(wx.EVT_KILL_FOCUS,
            self.edit_playlist_add_song_search_bar_kill_focus_handler)
        self.edit_playlist_add_song_search.Bind(wx.EVT_TEXT,
            self.edit_playlist_adaptive_drop_down_add_song_menu_handler)      
        self.Bind(wx.EVT_LISTBOX, 
                  self.edit_playlist_add_song_drop_down_menu_select_handler,
                  self.edit_playlist_add_song_drop_down_menu)
        self.Bind(wx.EVT_BUTTON, self.edit_playlist_finished_editing_handler,
                   self.edit_playlist_finished_editing_button)

        self.Bind(wx.EVT_BUTTON, self.create_playlist_delete_song_handler,
                  self.delete_song_button)
        self.Bind(wx.EVT_LISTBOX, self.create_playist_delete_song_selected,
                  self.delete_song_drop_down_list)
        self.Bind(wx.EVT_BUTTON, self.create_playlist_save_playlist_handler,
                  self.create_playlist_save_playlist)
        

        self.Bind(wx.EVT_BUTTON, self.prev_track_handler,
                  self.prev_button)
        self.Bind(wx.EVT_BUTTON, self.next_track_handler,
                  self.next_button)

        self.Bind(wx.EVT_BUTTON, self.play_playlist_handler,
                  self.play_playlist_button)

        self.Bind(wx.EVT_COMBOBOX, self.playlist_to_play_selected_handler,
                  self.play_playlist_selector)

        self.Bind(wx.EVT_BUTTON, self.play_button_click_handler, 
                  self.play_button)

        self.Bind(wx.EVT_BUTTON, self.stop_button_click_handler, 
                  self.stop_button)
        
        self.Bind(wx.EVT_LISTBOX, self.drop_down_song_menu_select_handler,
                  self.drop_down_song_menu)
        self.Bind(wx.EVT_LISTBOX, self.drop_down_add_song_menu_select_handler,
                  self.drop_down_add_song_menu)
          

        self.add_song_search.Bind(wx.EVT_LEFT_DOWN,
                  self.add_song_search_bar_left_button_down_handler)
        self.add_song_search.Bind(wx.EVT_KILL_FOCUS,
                 self.add_song_search_bar_kill_focus_handler)
        self.add_song_search.Bind(wx.EVT_TEXT,
                self.adaptive_drop_down_add_song_menu_handler)     

        self.search_bar.Bind(wx.EVT_LEFT_DOWN,  
                  self.search_bar_left_button_down_handler)
        self.search_bar.Bind(wx.EVT_KILL_FOCUS,
                  self.search_bar_kill_focus_handler)
        self.search_bar.Bind(wx.EVT_TEXT, 
                self.adaptive_drop_down_song_menu_handler)
        mainPanel.Bind(wx.EVT_LEFT_DOWN,
                   self.implicit_drop_down_song_menu_hide)
         
    
       # implement dragging of progress_circle 
       # self.progress_circle_sbm.Bind(wx.EVT_LEFT_iDOWN, 
       #           self.drag_progress_circle_left_down_handler )
       # self.progress_circle_sbm.Bind(wx.EVT_LEAVE_WINDOW,
       #           self.drag_progress_circle_leave_window_handler )

    def delete_playlist_handler(self, commandevent):
        playlist_name_to_delete = self.delete_playlist_selector.GetStringSelection()
        Playlists.delete_playlist(playlist_name_to_delete)
        playlist_deleted_message = "Playlist '" + playlist_name_to_delete + "' has been deleted."
        self.delete_playlist_label.Hide()
        self.delete_playlist_selector.Hide()
        self.delete_playlist_songs.Hide()
        self.delete_playlist_button.Hide()
        wx.MessageBox(playlist_deleted_message)

    def delete_playlist_selector_handler(self, commandevent):
        playlist_selected = commandevent.GetString()
        curr_playlist = Playlists.Playlist(playlist_selected)
        songs_list = curr_playlist.get_songs()
        newline_str = "\n"
        songs_str = newline_str.join(songs_list)
        self.delete_playlist_songs.SetValue(songs_str)

    def edit_playlist_finished_editing_handler(self, commandevent):
        self.edit_playlist_playlist_selector_label.Hide()
        self.edit_playlist_playlist_selector.Hide()
        self.edit_playlist_playlist_name_label.Hide()
        self.edit_playlist_playlist_name.Hide()
        self.edit_playlist_playlist_songs_label.Hide()
        self.edit_playlist_playlist_songs.Hide()
        self.edit_playlist_add_song_label.Hide()
        self.edit_playlist_add_song_search.Hide()
        self.edit_playlist_add_song_drop_down_menu.Hide()
        self.edit_playlist_finished_editing_button.Hide()

    def edit_playlist_add_song_search_bar_left_button_down_handler(self, mouseevent):
        mouseevent.Skip()
        self.edit_playlist_add_song_drop_down_menu.Show(True) 
   
    def edit_playlist_add_song_search_bar_kill_focus_handler(self,mouseevent):
        self.edit_playlist_add_song_drop_down_menu.Show(False)

    def edit_playlist_adaptive_drop_down_add_song_menu_handler(self, commandevent):
        self.edit_playlist_add_song_drop_down_menu.Show()
        search_bar_str = self.edit_playlist_add_song_search.GetLineText(0)
        songslist = os.listdir("/home/andy/Documents/projects/mp3_player/songs")
        matching_songs = []
        for curr_song in songslist:
            search_bar_str = search_bar_str.lower()
            curr_song_lowercase = curr_song.lower()
            if search_bar_str in curr_song_lowercase:
                matching_songs.append(curr_song)
        self.edit_playlist_add_song_drop_down_menu.Clear()
        for song in matching_songs:
            self.edit_playlist_add_song_drop_down_menu.Append(song)
    
    def edit_playlist_add_song_drop_down_menu_select_handler(self, commandevent):
        selected_song_to_add = commandevent.GetString()
        self.curr_playlist.add_new_song(selected_song_to_add)
        songs_list = self.curr_playlist.get_songs()
        newline_str = "\n"
        songs_string = newline_str.join(songs_list)
        self.edit_playlist_playlist_songs.Clear()
        self.edit_playlist_playlist_songs.SetValue(songs_string)
    
    def edit_playlist_delete_song(self, commandevent):
        self.curr_playlist.del_song(self.edit_playlist_song_selected)
        self.edit_playlist_playlist_songs.Clear()
        playlist_songs = self.curr_playlist.get_songs()
        newline_str = "\n"
        playlist_songs_string = newline_str.join(playlist_songs)
        self.edit_playlist_playlist_songs.SetValue(playlist_songs_string)

    def edit_playlist_song_selected_handler(self, mouseevent):
        mouse_pos = mouseevent.GetPosition()
        start_pos = 0
        end_pos = self.edit_playlist_playlist_songs.GetLastPosition()
        if end_pos == 0: # if self.edit_playlist_playlist_songs is empty return
            return 
        line_y_coords = []
        for pos in range(start_pos, end_pos+1):
            curr_coord = self.edit_playlist_playlist_songs.PositionToCoords(pos)
            curr_y = curr_coord.y
            if curr_y not in line_y_coords:
                line_y_coords.append(curr_y)
        line_height = 15 # this will need to change if the font size changes
        line_y_coords.append(line_y_coords[len(line_y_coords)-1] + line_height)
        mouse_y_coord = mouse_pos.y
        line_of_mouse_click = -1 # zero starting index giving line number
                                 # of where the mouse was clicked
        for i in range(0, len(line_y_coords)-1):
            if ( (line_y_coords[i] <= mouse_y_coord) and 
                 (mouse_y_coord < line_y_coords[i+1]) ):
                line_of_mouse_click = i
        if (line_of_mouse_click > -1):
            self.edit_playlist_song_selected = self.edit_playlist_playlist_songs.GetLineText(line_of_mouse_click)
            # append the correct amount of positions to the submenu
            menu_items = self.move_song_options.GetMenuItems()
            for menu_item in menu_items:
                menu_id = menu_item.GetId()
                self.move_song_options.Delete(menu_id)
            NoOfLines = self.edit_playlist_playlist_songs.GetNumberOfLines()
            move_song_pos_items = []
            for line_number in range(0, NoOfLines):
                menu_item_label = str(line_number)
                move_song_pos_item = self.move_song_options.Append(wx.ID_ANY, menu_item_label)
                self.move_song_options.Bind(wx.EVT_MENU, self.edit_playlist_song_move_helper(menu_item_label), move_song_pos_item)
                 
            self.edit_playlist_playlist_songs.PopupMenu(self.edit_menu)

    def edit_playlist_song_move_helper(self, menu_item_label):
        
        def edit_playlist_song_move_handler(commandevent):
            new_song_index_position = int(menu_item_label)
            self.curr_playlist.edit_song_pos(self.edit_playlist_song_selected,
                                               new_song_index_position)
            new_order_playlist_songs_list = self.curr_playlist.get_songs()
            newline_str = "\n"
            playlist_songs_string = newline_str.join(new_order_playlist_songs_list)
            self.edit_playlist_playlist_songs.Clear()
            self.edit_playlist_playlist_songs.SetValue(playlist_songs_string)   
        
        return edit_playlist_song_move_handler    
   

    def edit_playlist_mouse_entered_handler(self, mouseevent):
        updated_cursor = wx.Cursor(wx.CURSOR_ARROW)
        self.edit_playlist_playlist_songs.SetCursor(updated_cursor)


    def edit_playlist_playlist_name_edit_handler(self, commandevent):
        new_playlist_name = commandevent.GetString()
        curr_selected_playlist = self.edit_playlist_playlist_selector.GetValue()
        if ((curr_selected_playlist != "") or (self.allow_edit_playlist_name==1)):
            self.curr_playlist.edit_playlist_name(new_playlist_name)
            self.edit_playlist_playlist_selector.Clear()
            new_playlist_list = Playlists.list_all_playlists()
            self.edit_playlist_playlist_selector.AppendItems(new_playlist_list)    

    def edit_playlist_selector_handler(self, commandevent):
        selected_playlist = commandevent.GetString()
        self.playlist_playing = 0 # disable next and prev buttons
        self.allow_edit_playlist_name = 1
        self.curr_playlist = Playlists.Playlist(selected_playlist)
        self.edit_playlist_playlist_name.ChangeValue(self.curr_playlist.playlist_name)
        songs_list = self.curr_playlist.get_songs()
        newline_str = "\n"
        songs_string = newline_str.join(songs_list)
        self.edit_playlist_playlist_songs.SetValue(songs_string)

       # self.edit_playlist_add_song_drop_down_menu.Show()        



    def create_playlist_save_playlist_handler(self, commandevent):
        songs_content = self.create_playlist_playlist_songs.GetValue()
        playlist_name_content=self.create_playlist_playlist_name_inputbox.GetValue()
        if ( (songs_content=="") or (playlist_name_content=="") ):
            wx.MessageBox(
                     "Please enter a playlist name and the playlist songs.")
            return
        songs_list = songs_content.split("\n")
        res = Playlists.create_new_playlist(playlist_name_content, songs_list)
        if res==-1:
            playlist_already_exists_message = "The playlist '" + playlist_name_content + "' already exists. Please choose a different playlist name."
            wx.MessageBox(playlist_already_exists_message)
            return
        success_message = "The playlist '" + playlist_name_content + "' has now been saved."
        wx.MessageBox(success_message)
        

    def create_playist_delete_song_selected(self, commandevent):
        deleted_song = commandevent.GetString()
        playlist_songs_string = self.create_playlist_playlist_songs.GetValue()
        playlist_songs_list = playlist_songs_string.split("\n")
        playlist_songs_list.remove(deleted_song)
        newline_str = "\n"
        new_playlist_songs_str = newline_str.join(playlist_songs_list)
        self.create_playlist_playlist_songs.Clear()
        self.create_playlist_playlist_songs.SetValue(new_playlist_songs_str)
        self.delete_song_drop_down_list.Hide()


    def create_playlist_delete_song_handler(self, commandevent):
        line0_len = self.create_playlist_playlist_songs.GetLineLength(0)
        if line0_len > 0:
            songs_value = self.create_playlist_playlist_songs.GetValue()
            songs_list = songs_value.split("\n")
            self.delete_song_drop_down_list.Set(songs_list)
            self.delete_song_drop_down_list.Show()
       
    def prev_track_handler(self, commandevent):
        if self.playlist_playing == 1:
            prev_song = self.curr_playlist.get_prev_song()
            self.play_mp3(prev_song)

    def next_track_handler(self, commandevent):
        if self.playlist_playing == 1:
            next_song = self.curr_playlist.get_next_song()
            self.play_mp3(next_song)

    def play_playlist_handler(self, commandevent):
        self.playlist_playing = 1
        first_song = self.curr_playlist.get_curr_song()
        self.play_mp3(first_song)

    def playlist_to_play_selected_handler(self, commandevent):
        selected_playlist_name = commandevent.GetString()
        self.curr_playlist = Playlists.Playlist(selected_playlist_name)
        songs_list = self.curr_playlist.get_songs()
        newline_str = "\n"
        songs_list_string = newline_str.join(songs_list)
        self.playlist_songs.SetValue(songs_list_string)

    def createMenuBar(self):
        
        file_menu = wx.Menu()
        browse_and_play_item = file_menu.Append(-1, "&Browse and Play mp3..\tCTRL+B", "Browse the computer for an mp3 file to play.", wx.ITEM_NORMAL)
        exit_item = file_menu.Append(wx.ID_EXIT)
  
        playlists_menu = wx.Menu()
        play_playlist_item = playlists_menu.Append(-1, "Play playlist")
        create_playlist_item = playlists_menu.Append(-1, "Create playlist")
        edit_playlist_item = playlists_menu.Append(-1, "Edit playlist")
        delete_playlist_item = playlists_menu.Append(-1, "Delete playlist")
      
        menu_bar = wx.MenuBar()

        menu_bar.Append(file_menu, "File")
        menu_bar.Append(playlists_menu, "Playlists")

        self.SetMenuBar(menu_bar)
        
        self.Bind(wx.EVT_MENU, 
                  self.browse_and_play_handler, 
                  browse_and_play_item)
        self.Bind(wx.EVT_MENU,
                  self.quit_app_handler,
                  exit_item)
        self.Bind(wx.EVT_MENU,
                  self.play_playlist_menu_handler,
                  play_playlist_item)
        self.Bind(wx.EVT_MENU,
                  self.create_playlist_menu_handler,
                  create_playlist_item)
        self.Bind(wx.EVT_MENU,
                  self.edit_playlist_menu_handler,
                  edit_playlist_item)
        self.Bind(wx.EVT_MENU,
                  self.delete_playlist_menu_handler,
                  delete_playlist_item)

    def delete_playlist_menu_handler(self, commandevent):    
        
        # Hide play playlist widgets
        self.play_playlist_label.Hide()
        self.play_playlist_selector.Hide()
        self.playlist_songs.Hide()
        self.play_playlist_button.Hide()

        # Hide create playlist widgets
        self.create_playlist_main_label.Hide()
        self.create_playlist_playlist_name_label.Hide()
        self.create_playlist_playlist_name_inputbox.Hide()
        self.create_playlist_playlist_songs_label.Hide()
        self.create_playlist_playlist_songs.Hide()
        self.create_playlists_add_song_label.Hide()
        self.add_song_search.Hide()
        self.delete_song_button.Hide()
        self.create_playlist_save_playlist.Hide()

        # Hide edit playlist widgets
        self.edit_playlist_playlist_selector_label.Hide()
        self.edit_playlist_playlist_selector.Hide()
        self.edit_playlist_playlist_name_label.Hide()
        self.edit_playlist_playlist_name.Hide()
        self.edit_playlist_playlist_songs_label.Hide()
        self.edit_playlist_playlist_songs.Hide()
        self.edit_playlist_add_song_label.Hide()
        self.edit_playlist_add_song_search.Hide()
        self.edit_playlist_add_song_drop_down_menu.Hide() 
        self.edit_playlist_finished_editing_button.Hide()

        # Show delete playlist widgets
        self.delete_playlist_selector.Clear()
        playlists_list = Playlists.list_all_playlists()
        self.delete_playlist_selector.AppendItems(playlists_list)
        
        self.delete_playlist_selector.Show()
        self.delete_playlist_songs.Clear()      
        self.delete_playlist_label.Show()
        self.delete_playlist_songs.Show()
        self.delete_playlist_button.Show()

    def edit_playlist_menu_handler(self, commandevent):  
        
        # Hide play playlist widgets
        self.play_playlist_label.Hide()
        self.play_playlist_selector.Hide()
        self.playlist_songs.Hide()
        self.play_playlist_button.Hide()

        # Hide create playlist widgets
        self.create_playlist_main_label.Hide()
        self.create_playlist_playlist_name_label.Hide()
        self.create_playlist_playlist_name_inputbox.Hide()
        self.create_playlist_playlist_songs_label.Hide()
        self.create_playlist_playlist_songs.Hide()
        self.create_playlists_add_song_label.Hide()
        self.add_song_search.Hide()
        self.delete_song_button.Hide()
        self.create_playlist_save_playlist.Hide()

        # Hide delete playlist widgets
        self.delete_playlist_label.Hide()
        self.delete_playlist_selector.Hide()
        self.delete_playlist_songs.Hide()
        self.delete_playlist_button.Hide()

        # Show edit playlist widgets
        playlists_list = Playlists.list_all_playlists()
        self.edit_playlist_playlist_selector.Clear()
        self.edit_playlist_playlist_selector.AppendItems(playlists_list)
        self.edit_playlist_playlist_name.ChangeValue("")
        self.edit_playlist_playlist_songs.Clear()
        self.edit_playlist_playlist_selector_label.Show()
        self.edit_playlist_playlist_selector.Show()
        self.edit_playlist_playlist_name_label.Show()
        self.edit_playlist_playlist_name.Show()
        self.edit_playlist_playlist_songs_label.Show()
        self.edit_playlist_playlist_songs.Show()
        self.edit_playlist_add_song_label.Show()
        self.edit_playlist_add_song_search.Show()
        self.edit_playlist_add_song_drop_down_menu.Hide() # keep hidden
        self.edit_playlist_finished_editing_button.Show()

    def create_playlist_menu_handler(self, commandevent):

        # Hide play playlist widgets
        self.play_playlist_label.Hide()
        self.play_playlist_selector.Hide()
        self.playlist_songs.Hide()
        self.play_playlist_button.Hide()

        # Hide edit playlist widgets
        self.edit_playlist_playlist_selector_label.Hide()
        self.edit_playlist_playlist_selector.Hide()
        self.edit_playlist_playlist_name_label.Hide()
        self.edit_playlist_playlist_name.Hide()
        self.edit_playlist_playlist_songs_label.Hide()
        self.edit_playlist_playlist_songs.Hide()
        self.edit_playlist_add_song_label.Hide()
        self.edit_playlist_add_song_search.Hide()
        self.edit_playlist_add_song_drop_down_menu.Hide() # keep hidden
        self.edit_playlist_finished_editing_button.Hide()

        # Hide delete playlist widgets
        self.delete_playlist_label.Hide()
        self.delete_playlist_selector.Hide()
        self.delete_playlist_songs.Hide()
        self.delete_playlist_button.Hide()

        # Show create playlist widgets
        self.create_playlist_main_label.Show() 
        self.create_playlist_playlist_name_label.Show()
        self.create_playlist_playlist_name_inputbox.Show()
        self.create_playlist_playlist_songs_label.Show()
        self.create_playlist_playlist_songs.Show()
        self.create_playlists_add_song_label.Show()
        self.add_song_search.Show()
        self.delete_song_button.Show()
        self.create_playlist_save_playlist.Show()

    def browse_and_play_handler(self, commandevent):    
        # otherwise ask the user what new file to open
        with wx.FileDialog(self, 
                           "Open MP3 file to play", 
                           wildcard="mp3 files (*.mp3)|*.mp3",
                           style=wx.FD_OPEN | 
                                 wx.FD_FILE_MUST_EXIST) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return     # the user changed their mind

            # Proceed loading the file chosen by the user
            full_pathname = fileDialog.GetPath()
            directory_filename_tuple = os.path.split(full_pathname)
            directory = directory_filename_tuple[0] + "/"
            filename = directory_filename_tuple[1]
            self.play_mp3(filename, directory)

    def quit_app_handler(self, commandevent):
        self.Close(True)

    def play_playlist_menu_handler(self, commandevent):
        
        # Hide create playlist widgets
        self.create_playlist_main_label.Hide()
        self.create_playlist_playlist_name_label.Hide()
        self.create_playlist_playlist_name_inputbox.Hide()
        self.create_playlist_playlist_songs_label.Hide()
        self.create_playlist_playlist_songs.Hide()
        self.create_playlists_add_song_label.Hide()
        self.add_song_search.Hide()
        self.drop_down_add_song_menu.Hide()
        self.delete_song_button.Hide()
        self.delete_song_drop_down_list.Hide()
        self.create_playlist_save_playlist.Hide()

        # Hide edit playlist widgets
        self.edit_playlist_playlist_selector_label.Hide()
        self.edit_playlist_playlist_selector.Hide()
        self.edit_playlist_playlist_name_label.Hide()
        self.edit_playlist_playlist_name.Hide()
        self.edit_playlist_playlist_songs_label.Hide()
        self.edit_playlist_playlist_songs.Hide()
        self.edit_playlist_add_song_label.Hide()
        self.edit_playlist_add_song_search.Hide()
        self.edit_playlist_add_song_drop_down_menu.Hide() # keep hidden
        self.edit_playlist_finished_editing_button.Hide()

        # Hide delete plsylist widgets
        self.delete_playlist_label.Hide()
        self.delete_playlist_selector.Hide()
        self.delete_playlist_songs.Hide()
        self.delete_playlist_button.Hide()

        # Show play plsylist widgets
        self.play_playlist_label.Show()
        playlists_list = Playlists.list_all_playlists()
        self.play_playlist_selector.Clear()
        self.play_playlist_selector.AppendItems(playlists_list)
        self.play_playlist_selector.Show()
        self.playlist_songs.Clear()
        self.playlist_songs.Show()
        self.play_playlist_button.Show()

    def drag_progress_circle_left_down_handler(self, mouseevent):
        mouseevent.Skip() # allow for other handlers to handle
                          # this event as well to allow the frame to get focus
        #while (mouseevent.LeftIsDown()):
        #    print("here0")
        #print("here")
        
    def drag_progress_circle_leave_window_handler(self, mouseevent):
        mouseevent.Skip()
        if (mouseevent.LeftIsDown()):
          curr_pos = mouseevent.GetPosition()
          if (curr_pos.x == 10):
              progress_circle_old_pos = self.progress_circle_sbm.GetPosition()
              progress_circle_new_pos = wx.Point(progress_circle_old_pos.x + 4,
                                                 progress_circle_old_pos.y )
              self.progress_circle_sbm.SetPosition(progress_circle_new_pos)
              print("here")

    # timer1: this code runs every 100th of a second to update the progress
    # bars circle when a song is playing. it also updates the progress timer
    # currmm:currss/totalmm:totalss
    #
    # timer2: code runs every second, comparing the current progress of the mp3
    # song with the current progress calculated during the last timer event. iF
    # the two progression times are the same then the end of the mp3 song has 
    # been reached and the function restarts the mp3 song (without playing it)
    #
    def timer_handler(self, timerevent):
        timerobj = timerevent.GetTimer()
        if (timerobj == self.timer1):
            curr_progress = self.mp3_player.get_pos()
            #print(curr_progress)

            mp3_length = self.mp3_player.get_len() # returns the length of
                                               # the mp3 song in ms
            curr_time = self.mp3_player.get_time() # returns total length of mp3 
                                               # song in ms
            progress_percent = curr_time / mp3_length

            # update progress circle in progress bar
            progress_circle_pos = wx.Point( 124 + 
                                        math.floor(progress_percent*341) , 93 )
            self.progress_circle_sbm.SetPosition(progress_circle_pos)

            # update timer just below progress bat 0:00/x:yz
            curr_secs = curr_time / 1000
            curr_mins = math.floor(curr_secs / 60)
            curr_secs_after_mins = math.floor( curr_secs - (60.0*curr_mins) )
            # curr_mins:curr_secs_after_mins
            curr_mins = str(curr_mins)
            curr_secs_after_mins = str(curr_secs_after_mins)        
        
            total_secs = mp3_length / 1000
            total_mins = math.floor(total_secs / 60)
            total_secs_after_mins = math.floor( total_secs - (60.0*total_mins) )
            total_mins = str(total_mins)
            total_secs_after_mins = str(total_secs_after_mins)

            # ensure format is mm:ss or m:ss
            single_digit_pattern="^[0-9]{1}$"
            match = re.match(single_digit_pattern, curr_secs_after_mins)
            if (match):
                curr_secs_after_mins = "0" + curr_secs_after_mins
            match = re.match(single_digit_pattern, total_secs_after_mins)
            if (match):
                total_secs_after_mins = "0" + total_secs_after_mins

            self.progress_timer.SetLabel(curr_mins+":"+curr_secs_after_mins+"/"+
                                     total_mins+":"+total_secs_after_mins)
        elif (timerobj == self.timer2):
            curr_time = self.mp3_player.get_time()
            if (self.current_time == curr_time):
                if (self.playlist_playing == 1):
                    next_song = self.curr_playlist.get_next_song()
                    self.play_mp3(next_song)
                    return
                else:
                    self.play_button.SetLabel("Play")

                    mp3_length = self.mp3_player.get_len()
                    total_secs = mp3_length / 1000
                    total_mins = math.floor(total_secs / 60)
                    total_secs_after_mins = math.floor( total_secs - (60.0*total_mins) )
                    total_mins = str(total_mins)
                    total_secs_after_mins = str(total_secs_after_mins)
                    single_digit_pattern="^[0-9]{1}$"
                    match = re.match(single_digit_pattern, total_secs_after_mins)
                    if (match):
                        total_secs_after_mins = "0" + total_secs_after_mins
                    progressbar_timerlabel = "0:00/" +total_mins+":"+total_secs_after_mins
                    self.progress_timer.SetLabel(progressbar_timerlabel)

                    self.timer1.Stop()
                    self.timer2.Stop()
                    self.mp3_player.stop()
                    progress_circle_pos = wx.Point( 124 , 93 )
                    self.progress_circle_sbm.SetPosition(progress_circle_pos)
            self.current_time = curr_time   
                 

    # returns the first song to be played from the directory songs as 
    # an Mp3Player object. os.listdir returns a list of files in the directory 
    # with ordering not preserved
    def get_first_song(self):
        songs_path = "/home/andy/Documents/projects/mp3_player/songs"
        first_song = os.listdir(songs_path)[0]
        mp3_player_first_song = Mp3Player.Mp3Player(first_song)
        return mp3_player_first_song

    def play_button_click_handler(self, event):
        if (self.play_button.GetLabel() == "Play"):
            self.play_button.SetLabel("Pause")
            self.mp3_player.play()
            self.timer1.Start(10, wx.TIMER_CONTINUOUS)
            self.timer2.Start(1000, wx.TIMER_CONTINUOUS)
        elif (self.play_button.GetLabel() == "Pause"):
            self.play_button.SetLabel("Play")
            self.mp3_player.pause()
            self.timer1.Stop()
            self.timer2.Stop()

    def stop_button_click_handler(self, event):
        self.play_button.SetLabel("Play")

        mp3_length = self.mp3_player.get_len()
        total_secs = mp3_length / 1000
        total_mins = math.floor(total_secs / 60)
        total_secs_after_mins = math.floor( total_secs - (60.0*total_mins) )
        total_mins = str(total_mins)
        total_secs_after_mins = str(total_secs_after_mins)
        single_digit_pattern="^[0-9]{1}$"
        match = re.match(single_digit_pattern, total_secs_after_mins)
        if (match):
            total_secs_after_mins = "0" + total_secs_after_mins 
        progressbar_timerlabel = "0:00/" +total_mins+":"+total_secs_after_mins
        self.progress_timer.SetLabel(progressbar_timerlabel)

        self.timer1.Stop()
        self.timer2.Stop()
        self.mp3_player.stop()
        progress_circle_pos = wx.Point( 124 , 93 )
        self.progress_circle_sbm.SetPosition(progress_circle_pos)
    
    def add_song_search_bar_kill_focus_handler(self, mouseevent):
        self.drop_down_add_song_menu.Show(False)

    def search_bar_kill_focus_handler(self, mouseevent):
        #focusevent.Skip()
        self.drop_down_song_menu.Show(False)

    def add_song_search_bar_left_button_down_handler(self, mouseevent):
        mouseevent.Skip()
        self.drop_down_add_song_menu.Show(True)

    def search_bar_left_button_down_handler(self, mouseevent):
        #focusevent.Skip()
        mouseevent.Skip()
        self.drop_down_song_menu.Show(True)

    def drop_down_add_song_menu_select_handler(self, commandevent):
        songname = commandevent.GetString()
        line0_len =  self.create_playlist_playlist_songs.GetLineLength(0)
        if (line0_len > 0):
            songname = "\n" + songname
        self.create_playlist_playlist_songs.AppendText(songname)

    def drop_down_song_menu_select_handler(self, commandevent):
        mp3_filename = commandevent.GetString()
        self.playlist_playing = 0

        # Hide play playlist widgets
        self.play_playlist_label.Hide()
        self.play_playlist_selector.Hide()
        self.playlist_songs.Hide()
        self.play_playlist_button.Hide()

        # Hide create playlist widgets
        self.create_playlist_main_label.Hide()
        self.create_playlist_playlist_name_label.Hide()
        self.create_playlist_playlist_name_inputbox.Hide()
        self.create_playlist_playlist_songs_label.Hide()
        self.create_playlist_playlist_songs.Hide()
        self.create_playlists_add_song_label.Hide()
        self.add_song_search.Hide()
        self.drop_down_add_song_menu.Hide()
        self.delete_song_button.Hide()
        self.delete_song_drop_down_list.Hide()
        self.create_playlist_save_playlist.Hide()

        self.play_mp3(mp3_filename)
   
    def adaptive_drop_down_add_song_menu_handler(self, commandevent):
        self.drop_down_add_song_menu.Show()
        search_bar_str = self.add_song_search.GetLineText(0)
        songslist = os.listdir("/home/andy/Documents/projects/mp3_player/songs")
        matching_songs = []
        for curr_song in songslist:
            search_bar_str = search_bar_str.lower()
            curr_song_lowercase = curr_song.lower()
            if search_bar_str in curr_song_lowercase:
                matching_songs.append(curr_song)
        self.drop_down_add_song_menu.Clear()
        for song in matching_songs:
            self.drop_down_add_song_menu.Append(song)

    def adaptive_drop_down_song_menu_handler(self, commandevent):
        self.drop_down_song_menu.Show()
        search_bar_str = self.search_bar.GetLineText(0)
        songslist = os.listdir("/home/andy/Documents/projects/mp3_player/songs")
        matching_songs = []
        for curr_song in songslist:
            search_bar_str = search_bar_str.lower()
            curr_song_lowercase = curr_song.lower()
            if search_bar_str in curr_song_lowercase:
                matching_songs.append(curr_song)
        self.drop_down_song_menu.Clear()
        for song in matching_songs:
            self.drop_down_song_menu.Append(song)

    def implicit_drop_down_song_menu_hide(self, mouseevent):
        mouseevent.Skip()
        if (self.drop_down_song_menu.IsShown()):
            self.drop_down_song_menu.Hide()
        if (self.drop_down_add_song_menu.IsShown()):
            self.drop_down_add_song_menu.Hide()
        if (self.edit_playlist_add_song_drop_down_menu.IsShown()):
            self.edit_playlist_add_song_drop_down_menu.Hide()
            
 
    # stops the currently playing mp3 and plays the input arguement mp3 file.
    # The progress timer and progress circle are reset, and timer1 and timer2
    # are started. the play button is set to display "pause" since the new
    # mp3 will be playing and the curr_song label is also updated
    def play_mp3(self, mp3_filename, 
                 mp3_path="/home/andy/Documents/projects/mp3_player/songs/"):
        self.curr_song.SetLabel(mp3_filename)
        self.mp3_player.stop()
        progress_circle_pos = wx.Point(124, 93)
        self.progress_circle_sbm.SetPosition(progress_circle_pos)
        self.mp3_player = Mp3Player.Mp3Player(mp3_filename, mp3_path)
        self.play_button.SetLabel("Pause")
        mp3_length = self.mp3_player.get_len()
        total_secs = mp3_length / 1000
        total_mins = math.floor(total_secs / 60)
        total_secs_after_mins = math.floor( total_secs - (60.0*total_mins) )
        total_mins = str(total_mins)
        total_secs_after_mins = str(total_secs_after_mins)

        # ensure format is mm:ss or m:ss
        single_digit_pattern="^[0-9]{1}$"
        match = re.match(single_digit_pattern, total_secs_after_mins)
        if (match):
            total_secs_after_mins = "0" + total_secs_after_mins
        self.progress_timer.SetLabel("0:00/"+
                                     total_mins+":"+total_secs_after_mins)
        self.mp3_player.play()
        self.timer1.Start(10, wx.TIMER_CONTINUOUS)
        self.timer2.Start(1000, wx.TIMER_CONTINUOUS)

if __name__ == "__main__":
    app = wx.App()
    mp3_player_size = wx.Size(600,400)
    mp3_player = mp3_player_gui(None, title="Mp3 Player", size=mp3_player_size)
    mp3_player.Show()
    app.MainLoop()

