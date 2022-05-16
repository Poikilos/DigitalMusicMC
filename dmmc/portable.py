#!/usr/bin/env python
'''
dmmc.portable

This file is part of the DigitalMusicMC project.

Transfer files to portable MP3 players or similar devices or storage
devices for music players. The source tree will be recreated on the
destination, with the directory containing the playlist as the root
(The playlist's directory is removed from the music file path case
insensitively on OS X which is case insensitive by default and on
Windows).
For that reason:
- Placing the Playlist in a deeper directory will create
  a shallower directory structure on the destination.
- Playlists with files that are not in a subdirectory of the directory
  containing the playlist may have a mangled destination, so in those
  cases the full path will not be changed, and the destination's copy
  of the playlist will have an entry that doesn't work.

Typically, place
playlists in your "Music" directory and set the destination to the root
of the device. The destination's copy of the playlist will be changed
to use relative paths. The detection of the root path in the filename


Usage:
transfer_playlist <source playlist m3u> <destination directory>

Example:
transfer-playlist "$HOME/Music/(.Tag) Dance.m3u" /media/$USER/SANDISK32/Music
'''
from __future__ import print_function
import sys
import os
import shutil


from dmmc import (
    error,
    OSCaseSensitive,
)


def usage():
    error(__doc__)


def transfer_playlist(source_playlist, destination_dir):
    '''
    See the docstring for the portable module.

    Raises:
    - OSError: [Errno 28] No space left on device: ...
    '''
    if not os.path.isfile(source_playlist):
        raise ValueError("{} is not a file.".format(source_playlist))
    if len(destination_dir) == 0:
        raise ValueError("destination_dir is blank.")
    if not os.path.isdir(destination_dir):
        raise ValueError("{} is not a folder.".format(destination_dir))
    source_paths = []
    new_lines = []
    oldRoot, playlistName = os.path.split(source_playlist)
    if not oldRoot.endswith(os.path.sep):
        oldRoot += os.path.sep
    oldRootLower = oldRoot
    if not OSCaseSensitive:
        oldRootLower = oldRoot.lower()
    destLower = destination_dir
    if not OSCaseSensitive:
        destLower = destLower.lower()
    if oldRootLower == destLower:
        raise ValueError(
            "The source is same as the destination (OSCaseSensitive={}"
            ", oldRoot=\"{}\", destination_dir=\"{}\")."
            "".format(OSCaseSensitive, oldRoot)
        )
    changed = 0
    found = 0
    not_commented = 0
    pairs = []
    missing = []
    copied_new = 0
    with open(source_playlist, 'r') as ins:
        for rawL in ins:
            line = rawL.rstrip()
            if (len(line.strip()) == 0) or line.startswith("#"):
                new_lines.append(line)
                continue
            isRel = False
            newLine = line
            if not os.path.isfile(line):
                srcAbsPath = os.path.join(oldRoot, line)
                if os.path.isfile(srcAbsPath):
                    # It is relative so make it absolute temporarily.
                    newLine = srcAbsPath
                else:
                    missing.append(line)
                    new_lines.append(line)
                    continue
            not_commented += 1
            lineLower = line
            if not OSCaseSensitive:
                lineLower = line.lower()
            if lineLower.startswith(oldRootLower):
                newLine = line[len(oldRoot):]
                # ^ This is OK since oldRoot is guaranteed to end with
                #   '/' so that will be removed from the music file
                #   path.
                if (os.path.sep == "/") and ("\\" in newLine):
                    raise ValueError(
                        "The '\\' (backslash) in \"{}\" doesn't"
                        " match the OS path separator, so the"
                        " relative path couldn't be calculated."
                    )
                if (os.path.sep == "\\") and ("/" in newLine):
                    raise ValueError(
                        "The '/' (forward slash) in \"{}\" doesn't"
                        " match the OS path separator, so the"
                        " relative path couldn't be calculated."
                    )
                newPath = os.path.join(destination_dir, newLine)
                newDir = os.path.split(newPath)[0]
                if not os.path.isdir(newDir):
                    os.makedirs(newDir)
                    # print('mkdir -p "{}"'.format(newDir))
                if not os.path.isfile(newPath):
                    error('cp "{}" "{}" --preserve=timestamps'
                          ''.format(line, newPath))
                    shutil.copy(line, newPath)
                    copied_new += 1
                changed += 1
            new_lines.append(newLine)
    error("lines: {}".format(len(new_lines)))
    error("missing: {}".format(missing))
    error("music files specified: {}".format(not_commented))
    error("music files found: {}".format(changed))
    error("made relative: {}".format(changed))
    error("new: {}".format(copied_new))
    destPath = os.path.join(destination_dir, playlistName)
    error('* writing "{}"...'.format(destPath))
    missingName = playlistName + ".missing.txt"
    missingPath = os.path.join(destination_dir, missingName)
    with open(destPath, 'w') as outs:
        for line in new_lines:
            # print(line)
            outs.write(line + "\n")
    if len(missing) > 0:
        with open(missingPath, 'w') as outs:
            for line in missing:
                outs.write(line + "\n")
    error("  * done")



def transfer_playlist_cli():
    if (len(sys.argv) > 1) and (sys.argv[1] == "--help"):
        usage()
        exit(0)
    if len(sys.argv) < 3:
        usage()
        raise ValueError(
            "You must provide a source playlist and destination directory."
        )
    transfer_playlist(sys.argv[1], sys.argv[2])


def main():
    usage()
    error("")
    error("Error:")
    error("This module should be imported or called from the CLI.")
    error("")


if __name__ == "__main__":
    main()
