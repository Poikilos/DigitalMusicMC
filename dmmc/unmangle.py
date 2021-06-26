#!/usr/bin/env python3
'''
- Operate where the current directory is the band directory containing
  album directories that contain music files.
- The files and directories may be weird, named with space-padded
  hyphens separating each part (only " - " is accepted unless you
  specify sep to the processBand function), and unicode characters.

The processBand function will automatically:
- Rename files with unicode characters and make them ASCII.
- Remove invalid characters or spaces from the end of the filename.
- Rename files so they only contain the song name (and any other info
  such as the track number after the band and album name).
- Rename directories so they only contain the album name.

Command Line Interface:

Specify the band name (or any other whole element to remove from
space-hyphen-space delimited directory names) in quotes such as via:

python unmangle.py "Stratford Ct."
'''
import sys
import os
initializePreloadScreen = True

myFileName = os.path.basename(__file__)

def error(msg):
    sys.stderr.write("{}\n".format(msg))

def showTitle():
    error("")
    error("")
    title = myName  # os.path.basename(sys.argv[0])
    error(title)
    error("-"*len(title))


myName = "unmangle"
__author__ = "Jake Gustafson"

startCLIi = __doc__.find("Command Line Interface")
usageS = __doc__[startCLIi:]

songExts = ['mp3', 'wav', 'flac', 'alac', 'aac', 'mp4', 'm4a', 'ape']
songDotExts = []
for songExt in songExts:
    songDotExts.append('.'+songExt)


readLink = None
try:
    readLink = os.readlink(__file__)
except OSError:
    # not a link
    readLink = __file__
realFile = os.path.realpath(readLink)
dataPath = os.path.dirname(realFile)
# error("dataPath: {}".format(dataPath))
unusableChars = {}
unusableCharFiles = {}
unusableCharsPath = os.path.join(dataPath, "data", "characters")
if not os.path.isdir(unusableCharsPath):
    raise RuntimeError("unusableCharsPath is missing: \"{}\""
                       "".format(unusableCharsPath))
try:
    from dmmc.common import *
except ModuleNotFoundError:
    sys.path.append(os.path.dirname(dataPath))
    from dmmc.common import *

# setVerbose(True)


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
                            error("[{}] * (UnicodeDecodeError)"
                                  " couldn't finish reading \"{}\":"
                                  "".format(myFileName, subPath))
                    else:
                        error("[{}] * (unknown error) couldn't finish"
                        " reading \"{}\":".format(myFileName, subPath))
                        raise ex2
            else:
                error("[{}] * (unknown error) couldn't finish"
                      " reading \"{}\":".format(myFileName, subPath))
                raise ex
        if getVerbose():
            error("* gathering unusable character from \"{}\""
                  "".format(sub))
        if key is None:
            continue
        if key in unusableChars.keys():
            if initializePreloadScreen:
                showTitle()
                initializePreloadScreen = False
            error("[unmangle] Warning: The unusable{} character from"
                  " \"{}\" was already collected from \"{}\" and will"
                  " be ignored."
                  "".format(tryDelimiter, sub, unusableCharFiles[key]))
            continue
        unusableChars[key] = pathChar
        unusableCharFiles[key] = sub
# error("badChars:{}".format(badChars))

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
    error(usageS)

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


def processBand(bandPath, bandName, sep=" - ", trackDigitsMin=2):
    bandPath = os.path.realpath(bandPath)
    for album in os.listdir(bandPath):
        albumPath = os.path.join(bandPath, album)
        if not os.path.isdir(albumPath):
            continue
        albumParts = album.split(sep)
        albumName = albumParts[-1]
        error(albumName)
        songCount = 0
        for song in os.listdir(albumPath):
            if not os.path.splitext(song)[-1].lower() in songDotExts:
                continue
            songParts = song.split(sep)
            songName = songParts[-1]
            if len(songParts) > 1:
                # In case the song name starts with trackDigitsMin
                # or more numbers, check previous parts regardless of
                # what last part looks like:
                if isDigits(songParts[-2][:trackDigitsMin]):
                    songName = sep.join(songParts[-2:])
                elif isDigits(songParts[-3][:trackDigitsMin]):
                    songName = sep.join(songParts[-3:])
                '''
                if not isDigits(songParts[-1][:trackDigitsMin]):
                    if isDigits(songParts[-2][:trackDigitsMin]):
                        songName = sep.join(songParts[-2:])
                    elif isDigits(songParts[-3][:trackDigitsMin]):
                        songName = sep.join(songParts[-3:])
                    else:
                        error("  * Warning: No part of {} starts with"
                              "    a 2-digit track number.")
                if isDigits(songParts[-1][trackDigitsMin+1:]):
                    # In case the song name starts with more than 2
                    # numbers:
                    if isDigits(songParts[-2][:trackDigitsMin]):
                        songName = sep.join(songParts[-2:])
                    elif isDigits(songParts[-3][:trackDigitsMin]):
                        songName = sep.join(songParts[-3:])
                    # else:
                        # error("  * Warning: No part of {} starts with"
                        #       "    a 2-digit track number.")
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
                    # ^ Can be "" if unusableChars value is "" (If the
                    #   character should be removed).
                    if (c != " ") or (not prevSpace):
                        cleanName += c
                    prevBad = False
                    if c == " ":
                        prevSpace = True
                    elif c != "":
                        prevSpace = False
                else:
                    error("removed chr({}) from...".format(ord(c)))
                    if not prevBad:
                        cleanName += "_"
                        prevSpace = False
                    prevBad = True
            cleanSplitName = os.path.splitext(cleanName)
            cleanName = (cleanSplitName[0].strip()
                         + cleanSplitName[1].strip())
            error("  {}".format(cleanName))
            songCount += 1
        error("  * processed {} song(s) in {}"
              "".format(songCount, albumName))
        error("")

def main():
    global initializePreloadScreen
    if initializePreloadScreen:
        showTitle()
        initializePreloadScreen = False
    if len(sys.argv) != 2:
        error("")
        usage()
        exit(1)
    processBand(".", sys.argv[1])

if __name__ == "__main__":
    main()
