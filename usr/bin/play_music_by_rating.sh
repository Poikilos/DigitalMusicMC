#!/bin/sh
#python3 $HOME/Projects/generate-playlist.py > "$HOME/Desktop/Playlist Stats.txt"
#exec "vlc /mnt/seandata/Projects/experimental/AM\ Tube\ Radio\ Background\ Noise\ Loop\ 1b\ \(2013-09\ final\)\ -\ newAMbgsound1.wav --loop"
#exec "/usr/bin/vlc \"/mnt/seandata/Projects/experimental/AM Tube Radio Background Noise Loop 1b (2013-09 final) - newAMbgsound1.wav\" --loop"
#/usr/bin/vlc /mnt/seandata/Projects/experimental/AM\ Tube\ Radio\ Background\ Noise\ Loop\ 1b\ \(2013-09\ final\)\ -\ newAMbgsound1.wav --loop &
#smplayer /mnt/seandata/wav/11211121113.m3u8 &
cd /mnt/seandata/wav
python3 $HOME/Projects/play_music_by_rating.py
#sleep 5
