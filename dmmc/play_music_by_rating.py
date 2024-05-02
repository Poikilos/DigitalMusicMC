#!/usr//bin/env python
from __future__ import print_function
import os
import subprocess
import sys

if sys.version_info.major < 3:
    input = raw_input  # noqa: F821  # type: ignore

noise_dir = "/mnt/seandata/Projects/experimental"
am_name = "AM Tube Radio Background Noise Loop 1b (2013-09 final) - newAMbgsound1.wav"  # noqa: E501

# subprocess.call(["/home/owner/Projects/genrate_playlist_with_output.sh"])
# subprocess.call(["/usr/bin/vlc", os.path.join(noise_dir, am_name), "--loop"])  # noqa: E501
# subprocess.call(["smplayer", "/mnt/seandata/wav/11211121113.m3u8"])
p1 = subprocess.Popen([
    "/home/owner/Projects/generate_playlist_with_output.sh"
])
# NOTE: vlc shoudl be at 66% volume (for AM loop) & smplayer at middle (100%?)
p2 = subprocess.Popen(
    [
        "/usr/bin/vlc",
        os.path.join(noise_dir, am_name),
        "--loop",
    ]
)
p3 = subprocess.Popen(["smplayer", "/mnt/seandata/wav/11211121113.m3u8"])
input("press enter while this window is highlighted"
      " or press x to stop playback...")
