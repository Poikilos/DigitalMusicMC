#!/bin/sh
gen_py="$HOME/Projects/generate-playlist.py"
try_py="$HOME/git/DigitalMusicMC/dmmc/generate_playlist.py"
if [ -f "$try_py" ]; then
    gen_py="$try_py"
fi
python3 $gen_py >& "$HOME/Desktop/Playlist Stats.txt"
