#!/usr/bin/env python3
'''
- Operate where the current directory is the band directory containing
  album directories that contain music files.
- The files and directories may be weird, named with space-padded
  hyphens separating each part (only " - " is accepted unless you
  specify songSep or albumSep to the processBand function), and unicode
  characters.

By default, processBand function will automatically:
- Rename files so they only contain the song name (and any other info
  such as the track number after the band and album name).
  - Remove unicode characters and make them ASCII.
- Rename directories so they only contain the album name.
- Save an "original_names.json" file to the album folder if any names
  changed.

Command Line Interface:

Specify the band name (or any other whole element to remove from
space-hyphen-space [" - "] delimited directory names) in quotes.

Example:
unmangle.py "Stratford Ct."
'''
import sys
import os
import json
import shutil

initializePreloadScreen = True

myFileName = os.path.basename(__file__)

readLink = None
try:
    readLink = os.readlink(__file__)
except OSError:
    # not a link
    readLink = __file__
realFile = os.path.realpath(readLink)
dataPath = os.path.dirname(realFile)
# try:
#     import dmmc
# except ImportError:
#     sys.path.append(os.path.dirname(dataPath))

from dmmc import (
    echo0,
    echo1,
    echo2,
    set_verbosity,
)

def showTitle():
    echo0("")
    echo0("")
    title = myName  # os.path.basename(sys.argv[0])
    echo0(title)
    echo0("-"*len(title))


myName = "unmangle"
__author__ = "Jake Gustafson"

startCLIi = __doc__.find("Command Line Interface")
usageS = __doc__[startCLIi:]

songExts = ['mp3', 'wav', 'flac', 'alac', 'aac', 'mp4', 'm4a', 'ape']
songDotExts = []
for songExt in songExts:
    songDotExts.append('.'+songExt)



# echo0("dataPath: {}".format(dataPath))
unusableChars = {}
unusableCharFiles = {}
unusableCharsPath = os.path.join(dataPath, "data", "characters")
if not os.path.isdir(unusableCharsPath):
    raise RuntimeError("unusableCharsPath is missing: \"{}\""
                       "".format(unusableCharsPath))

nameChars = {
    "space": " ",
    "apostraphe": "'",
    "doublequote": "\"",
    "singlequote": "'",
    "dash": "--",
}


# See <https://stackoverflow.com/questions/2435894/how-do-i-check-for-
# illegal-characters-in-a-path>
# (`Path.GetInvalidFileNameChars` results on Windows, a superset of
# `Path.GetInvalidPathChars`):
windowsBadChars = ""
for i in range(0, 32):
    windowsBadChars += chr(i)
windowsBadChars += '"'  # 34
windowsBadChars += '*'  # 42
windowsBadChars += '/'  # 47
windowsBadChars += ':'  # 58
windowsBadChars += '<'  # 60
windowsBadChars += '>'  # 62
windowsBadChars += '?'  # 63
windowsBadChars += '\\'  # 92
windowsBadChars += '|'  # 124

# See <https://stackoverflow.com/questions/1033424/how-to-remove-bad-
# path-characters-in-python>:

badChars = "\0"
badChars += "/"  # disallowed in POSIX
badChars += ":"  # disallowed by Apple APIs; is the linux path separator
badChars += "\\"  # Windows directory separator
badChars += ";"  # Windows path separator
for c in windowsBadChars:
    if c not in badChars:
        badChars += c

def getOneChar(path, encoding='utf-8-sig'):
    ret = ""
    try:
        with open(path, 'r', encoding=encoding) as ins:
            for rawL in ins:
                line = rawL.rstrip("\n\r")
                if len(line) > 1:
                    raise ValueError("\"{}\" must contain only one"
                                     " character per line but has"
                                     " {}: \"{}\""
                                     "".format(path, len(line), line))
                if len(line) < 1:
                    continue
                ret += line
                break
        if len(ret) != 1:
            raise ValueError("\"{}\" must contain at least one"
                             " character.".format(path))
    except TypeError as ex:
        if "invalid keyword" in str(ex):
            raise RuntimeError("This program requires Python 3.")
        else:
            raise ex
    return ret


def getFirstCharOfLines(path):
    ret = ""
    with open(path, 'r') as ins:
        for rawL in ins:
            line = rawL.rstrip("\n\r")
            if len(line) > 1:
                raise ValueError("\"{}\" must contain only one"
                                 " character per line but has {}."
                                 "".format(path, len(line)))
            if len(line) < 1:
                continue
            ret += line
    return ret

for sub in os.listdir(unusableCharsPath):
    subPath = os.path.join(unusableCharsPath, sub)
    delimiter = "-faux"
    tryDelimiter = "-nonpath"
    if "-faux" not in sub:
        if tryDelimiter in sub:
            delimiter = tryDelimiter
    if delimiter in sub:
        parts = sub.split(delimiter)
        pathChar = parts[0]
        asChar = nameChars.get(pathChar)
        if asChar is not None:
            pathChar = asChar
        key = None
        try:
            key = getOneChar(subPath, encoding='utf-8-sig')
        except ValueError as ex:
            if "invalid start byte" in str(ex):
                try:
                    key = getOneChar(subPath, encoding='utf-8')
                except ValueError as ex2:
                    if "invalid start byte" in str(ex):
                        try:
                            key = getOneChar(subPath, encoding='utf-16')
                            # hyphen-faux.txt is 'iso-8859-1' according
                            # to Geany
                        except UnicodeDecodeError as ex3:
                            key = None
                            echo0("[{}] * (UnicodeDecodeError)"
                                  " couldn't finish reading \"{}\":"
                                  "".format(myFileName, subPath))
                    else:
                        echo0("[{}] * (unknown error) couldn't finish"
                        " reading \"{}\":".format(myFileName, subPath))
                        raise ex2
            else:
                echo0("[{}] * (unknown error) couldn't finish"
                      " reading \"{}\":".format(myFileName, subPath))
                raise ex
        echo1("* gathering unusable character from \"{}\""
              "".format(sub))
        if key is None:
            continue
        if key in unusableChars.keys():
            if initializePreloadScreen:
                showTitle()
                initializePreloadScreen = False
            echo0("[unmangle] Warning: The unusable{} character from"
                  " \"{}\" was already collected from \"{}\" and will"
                  " be ignored."
                  "".format(tryDelimiter, sub, unusableCharFiles[key]))
            continue
        unusableChars[key] = pathChar
        unusableCharFiles[key] = sub
# echo0("badChars:{}".format(badChars))

# These are marks that come after an alphabetical letter and don't work
# otherwise. See "handled-by-code" under "Required Data" in readme.
unusableChars[chr(776)] = ""  # diaeresis
unusableCharFiles[chr(776)] = sys.argv[0]
unusableChars[chr(770)] = ""  # circumflex
unusableCharFiles[chr(770)] = sys.argv[0]
unusableChars[chr(778)] = ""  # ring
unusableCharFiles[chr(778)] = sys.argv[0]
unusableChars[chr(769)] = ""  # accent
unusableCharFiles[chr(769)] = sys.argv[0]
unusableChars[chr(768)] = ""  # grave accent (backward accent mark)
unusableCharFiles[chr(768)] = sys.argv[0]

# From STRATFORD CT. - CONFERO - Tora Tora:
# - There is no other space around the hyphen so make them spaces
unusableChars[chr(12302)] = " "  # box-outline-single-thick-top_left
unusableChars[chr(12303)] = " "  # box-outline-single-thick-bottom_right

# From Stratford Ct. - 1 yr Anniversary Compilation - fibre:
unusableChars[chr(12300)] = ""  # box-outline-single-thin-top_left
unusableChars[chr(12301)] = ""  # box-outline-single-thin-bottom_right

# From STRATFORD CT. - CONFERO - Harrison:
# unusableChars[chr(chr(10047))] = ""  # flower

def isFilenameChar(c, index=-1):
    '''
    Sequential arguments:
    c -- usually a string of length 1, but can be longer if index is
         specified.
    index -- This will be used as an index in c if positive for when c
             is more than one character.
    '''
    s = None
    if index < 0:
        if len(c) != 1:
            raise ValueError("isFilenameChar expected a single"
                             " character or a string & index but got {}"
                             " characters: \"{}\".".format(len(c), c))
    else:
        s = c
        c = c[index]
    if ord(c) > 126:
        return False
    if ord(c) < 32:
        return False
    return c not in badChars


def usage():
    echo0(usageS)

digits = "0123456789"
alphaLowerChars = "abcdefghijklmnopqrstuvwxyz"
alphaChars = alphaLowerChars
for c in alphaLowerChars:
    alphaChars += c.upper()

def isDigits(s):
    for c in s:
        if c not in digits:
            return False
    return True


def processBand(bandPath, bandName, songSep=" - ", albumSep=" - ",
                trackDigitsMin=2, output_only=False):
    '''
    Sequential arguments:
    bandPath -- The band directory contains album directories which
                contain song files, and only directories and files in
                that structure will be processed.
    bandName -- Set the name of the band or another whole element
                delimited by albumSep to remove from the album directory
                name. For example,
                "Stratford Ct. - Secret Selection #41-50" becomes
                "Secret Selection #41-50".

    Keyword arguments:
    albumSep -- Break apart the album directory name using this
                delimiter. Only the last part of the directory name
                should be kept. For example, if albumSep is " - " and
                the directory name is "Band - Album" the directory gets
                renamed to "Album".
    songSep -- Break apart the song file name using this delimiter.
               Only the last part or part starting with track
               numbers should be kept. For example,
               "Artist - Album - # Title - some extra stuff.mp3" becomes
               "Artist - Album - # Title - some extra stuff.mp3", where
               # is a track number at least trackDigitsMin digits long.
    trackDigitsMin -- Detect where the new filename should start in
                      terms of the old filename by detecting this in
                      the 2nd to last and 3rd to last parts (if
                      neither, then only keep last part).
    output_only -- Output rename commands and do not actually rename
                   any files.
    '''
    fileRenames = 0
    folderRenames = 0
    bandPath = os.path.realpath(bandPath)
    verb = "unmangled"
    if output_only:
        verb = "unmangle"
    for album in os.listdir(bandPath):
        albumFileRenames = 0
        albumPath = os.path.join(bandPath, album)
        if not os.path.isdir(albumPath):
            continue
        albumParts = album.split(albumSep)
        cleanAlbum = albumParts[-1]
        echo0(cleanAlbum)
        songCount = 0
        historyPath = os.path.join(albumPath, "original_names.json")
        changed = {}
        changed['songs'] = {}
        for song in os.listdir(albumPath):
            songPath = os.path.join(albumPath, song)
            songNoExt = os.path.splitext(song)[-1]
            if not songNoExt.lower() in songDotExts:
                continue
            songParts = song.split(songSep)
            songName = songParts[-1]
            if len(songParts) > 1:
                # In case the song name starts with trackDigitsMin
                # or more numbers, check previous parts regardless
                # of what last part looks like:
                if isDigits(songParts[-2][:trackDigitsMin]):
                    songName = songSep.join(songParts[-2:])
                elif isDigits(songParts[-3][:trackDigitsMin]):
                    songName = songSep.join(songParts[-3:])
                '''
                if not isDigits(songParts[-1][:trackDigitsMin]):
                    if isDigits(songParts[-2][:trackDigitsMin]):
                        songName = songSep.join(songParts[-2:])
                    elif isDigits(songParts[-3][:trackDigitsMin]):
                        songName = songSep.join(songParts[-3:])
                    else:
                        echo0("  * Warning: No part of {} starts"
                              "    with a 2-digit track number.")
                if isDigits(songParts[-1][trackDigitsMin+1:]):
                    # In case the song name starts with more than 2
                    # numbers:
                    if isDigits(songParts[-2][:trackDigitsMin]):
                        songName = songSep.join(songParts[-2:])
                    elif isDigits(songParts[-3][:trackDigitsMin]):
                        songName = songSep.join(songParts[-3:])
                    # else:
                        # echo0("  * Warning: No part of {} starts"
                        #       "    with a 2-digit track number.")
                '''
            cleanName = ""
            prevBad = False
            prevSpace = False
            # TODO: Why does "_" never happen (character is removed
            # instead)?
            for c_orig in songName:
                c = c_orig
                got = unusableChars.get(c)
                if got is not None:
                    c = got
                if (c == "") or isFilenameChar(c):
                    # ^ Can be "" if unusableChars value is "" (If
                    #   the character should be removed).
                    if (c != " ") or (not prevSpace):
                        cleanName += c
                    prevBad = False
                    if c == " ":
                        prevSpace = True
                    elif c != "":
                        prevSpace = False
                else:
                    echo0("removed chr({}) from...".format(ord(c)))
                    if not prevBad:
                        cleanName += "_"
                        prevSpace = False
                    prevBad = True
            cleanSplitName = os.path.splitext(cleanName)
            cleanName = (cleanSplitName[0].strip()
                         + cleanSplitName[1].strip())
            echo0("  {}".format(cleanName))
            if cleanName != song:
                changed['songs'][cleanName] = song
                cleanPath = os.path.join(albumPath, cleanName)
                fileRenames += 1
                albumFileRenames += 1
                if output_only:
                    print("mv \"{}\" \"{}\""
                          "".format(songPath, cleanPath))
                else:
                    shutil.move(songPath, cleanPath)
            songCount += 1
        if cleanAlbum != album:
            if 'folders' not in changed:
                changed['folders'] = {}
            changed['folders'][cleanAlbum] = album
            cleanAlbumPath = os.path.join(bandPath, cleanAlbum)
        if not os.path.isfile(historyPath):
            with open(historyPath, 'w') as outs:
                json.dump(changed, outs, sort_keys=True, indent=2)
        if cleanAlbum != album:
            folderRenames += 1
            if output_only:
                print("mv \"{}\" \"{}\""
                      "".format(albumPath, cleanAlbumPath))
            else:
                shutil.move(albumPath, cleanAlbumPath)
        echo0("  * processed {} song(s) in {}"
              " ({} {})"
              "".format(songCount, cleanAlbum, verb, albumFileRenames))
        echo0("")
    echo0("* {} {} files and {} directory(ies) total"
          "".format(verb, fileRenames, folderRenames))

def main():
    global initializePreloadScreen
    if initializePreloadScreen:
        showTitle()
        initializePreloadScreen = False
    if len(sys.argv) != 2:
        echo0("")
        usage()
        return 1
    processBand(".", sys.argv[1])

if __name__ == "__main__":
    sys.exit(main())
