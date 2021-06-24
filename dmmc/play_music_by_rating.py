#!/bin/env python
import subprocess
#subprocess.call(["/home/owner/Projects/genrate_playlist_with_output.sh"])
#subprocess.call(["/usr/bin/vlc", "/mnt/seandata/Projects/experimental/AM Tube Radio Background Noise Loop 1b (2013-09 final) - newAMbgsound1.wav", "--loop"])
#subprocess.call(["smplayer", "/mnt/seandata/wav/11211121113.m3u8"])
p1=subprocess.Popen(["/home/owner/Projects/generate_playlist_with_output.sh"])
#NOTE: vlc shoudl be at 66% volume (for AM loop) and smplayer at middle (100%?)
p2=subprocess.Popen(["/usr/bin/vlc", "/mnt/seandata/Projects/experimental/AM Tube Radio Background Noise Loop 1b (2013-09 final) - newAMbgsound1.wav", "--loop"])
p3=subprocess.Popen(["smplayer", "/mnt/seandata/wav/11211121113.m3u8"])
input("press enter while this window is highlighted or press x to stop playback...")
