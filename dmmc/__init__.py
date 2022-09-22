#!/usr/bin/env python
from __future__ import print_function

import os
import sys
import platform

verbosity = 0

for argI in range(1, len(sys.argv)):
    arg = sys.argv[argI]
    if arg.startswith("--"):
        if arg == "--verbose":
            verbosity = 1
        elif arg == "--debug":
            verbosity = 2

def echo0(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

# ~/.local/share/strawberry/strawberry/strawberry.db
# ^ Yes, there is a strawberry folder in a strawberry folder :(
# SQLite DB structure: See contributing.md


def echo1(*args, **kwargs):
    if verbosity >= 1:
        sys.stderr.write("[debug] ")
        print(*args, file=sys.stderr, **kwargs)


def echo2(*args, **kwargs):
    if verbosity >= 2:
        sys.stderr.write("[debug] ")
        print(*args, file=sys.stderr, **kwargs)


def get_verbosity():
    return verbosity


def set_verbosity(level):
    global verbosity
    verbosity_levels = [True, False, 0, 1, 2]
    if level not in verbosity_levels:
        raise ValueError("verbosity must be 0-2 but was {}".format(verbosity))
    verbosity = level


# from https://github.com/poikilos/blnk
def which(cmd):
    paths_str = os.environ.get('PATH')
    if paths_str is None:
        debug("Warning: There is no PATH variable, so returning {}"
              "".format(cmd))
        return cmd
    paths = paths_str.split(os.path.pathsep)
    for path in paths:
        debug("looking in {}".format(path))
        tryPath = os.path.join(path, cmd)
        if os.path.isfile(tryPath):
            return tryPath
        else:
            debug("There is no {}".format(tryPath))
    return None


OSCaseSensitive = True
if platform.system() == "Windows":
    OSCaseSensitive = False
elif platform.system() == "Darwin":
    # This OS is not case sensitive by default.
    OSCaseSensitive = False

profile = None
appsData = None
myAppData = None
myName = "dmmc"
musicPaths = []

if platform.system() == "Windows":
    profile = os.environ['USERPROFILE']
    # appsData = os.path.join(profile, "AppData", "Roaming")
    appsData = os.environ['ROAMING']
    musicPaths.append(os.path.join(profile, "Music"))
else:
    profile = os.environ['HOME']
    appsData = os.path.join(profile, ".config")
    musicPaths.append(os.path.join(profile, "Music"))

myAppData = os.path.join(appsData, myName)


class Song:
    pass


class IPlaylist:
    pass


class LineReader:

    encodingBOMs = {}
    encodingBOMs['latin-1'] = "ï»¿"

    def __init__(self, text):
        self.index = 0
        self.bomLen = 0
        self.text = text
        self.encoding = "utf-8"
        for encoding, bom in LineReader.encodingBOMs.items():
            if len(self.text) < len(bom):
                continue
            if self.text[:len(bom)] == bom:
                # print('  * using bom "{}"'.format(bom))
                self.encoding = encoding
                self.bomLen = len(bom)
                self.index = self.bomLen
                break

    def __iter__(self):
        self.index = self.bomLen
        return self

    def __next__(self):
        result = ""
        if self.index >= len(self.text):
            raise StopIteration
        NLs = "\n\r"
        while self.index < len(self.text):
            c = self.text[self.index]
            result += c
            found = NLs.find(c)
            if found >= 0:
                tmp = "".join(list(set(NLs).difference(NLs[found])))
                # ^ Remove the current newline to be able to check for
                #   the others (The code disregards order, but NL & tmp
                #   are only used as sets so that's ok).
                # If the next character is another newline but
                # different, then also get that one as part of the
                # same line.
                if self.index + 1 < len(self.text):
                    if self.text[self.index+1] in tmp:
                        result = result[:-1] + "\n"
                        # ^ Mimic Python behavior by converting the
                        #   character to "\n" and discarding the next
                        #   one (self.text[self.index+1]).
                        self.index += 1
                self.index += 1
                return result

            self.index += 1


class PlaylistM3U(IPlaylist):

    def __init__(self):
        self.songs = []
        self.stream = None

    def load(self, path):
        # print(path)
        metaOpener = "#EXTINF:"
        with open(path, 'rb') as ins:
            data = ins.read()
            text = None
            try:
                text = data.decode("utf-8-sig")
            except UnicodeDecodeError as ex:
                if "invalid continuation byte" in str(ex):
                    text = data.decode("latin-1")
                elif "invalid start byte" in str(ex):
                    text = data.decode('ISO-8859-1')
                else:
                    raise ex
            lineN = 0
            meta = {}
            for rawL in LineReader(text):
                line = rawL.strip()
                lineN += 1
                # File header:
                # #EXTM3U
                # Playlist info:
                #
                # Song info line:
                # #EXTINF:263,Sixto Sounds - Shredder (Teenage Mutant Ninja Turtles IV) - The Shredder
                #         ^ The number is the song length in seconds.
                # Song line (comes after song info line):
                # /home/owner/Music/Video Game Music/Compilations/BadAss - Boss Themes/FLAC/18 King Dedede (Kirby Super Star) - The Last Dance [The Joker].flac
                # print("length:{} '''{}'''".format(len(rawL), line))
                # if len(rawL) == 1:
                #     print("  {}".format(hex(ord(rawL))))
                if len(line) == 0:
                    meta = {}
                elif line == "#EXTM3U":
                    meta = {}
                    if lineN != 1:
                        echo0("{}:{}:1: misplaced shebang: {}"
                              "".format(path, lineN, line))
                elif line.startswith(metaOpener):
                    meta = {}
                    metaStr = line[len(metaOpener):]
                    sepI = metaStr.find(",")
                    if sepI < 0:
                        echo0("{}:{}:1: bad metadata (missing ','): {}"
                              "".format(path, lineN, line))
                        continue
                    meta["seconds"] = metaStr[:sepI]
                    meta["name"] = metaStr[sepI+1:]
                    print("  - meta: {}".format(meta))
                # elif line.startswith("/") or line.startswith("./"):
                elif line.startswith("#"):
                    meta = {}
                    echo0("{}:{}:1: unknown metadata: {}"
                          "".format(path, lineN, line))
                else:
                    # If it isn't metadata, it should be a song.
                    pass
                # else:
                #     echo0("{}:{}:1: unknown line: {}"
                #           "".format(path, lineN, line))
                continue


def getPlaylists(path, recursive=True):
    '''
    Sequential arguments:
    path -- Specify a directory containing playlists.

    Keyword arguments:
    recursive -- Specify True to also include subdirectories.
    '''
    results = []
    for sub in os.listdir(path):
        subPath = os.path.join(path, sub)
        subLower = sub.lower()
        if os.path.isdir(subPath):
            if recursive:
                getPlaylists(subPath)
        if subLower.endswith(".m3u8") or subLower.endswith(".m3u"):
            playlist = PlaylistM3U()
            print("* {}".format(sub))
            if playlist.load(subPath):
                results.append(playlist)
    return results
