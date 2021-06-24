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

Specify the band name in quotes such as via:

python unmangle.py "Stratford Ct."
'''
import sys
import os

usageS = '''
Specify the band name in quotes such as via:

python unmangle.py "Stratford Ct."
'''

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
# print("dataPath: {}".format(dataPath))
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
}


# See <https://stackoverflow.com/questions/2435894/how-do-i-check-for-illegal-characters-in-a-path>
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
                        except Exception as ex3:
                            print("* couldn't finish"
                                  " reading \"{}\":".format(subPath))
                            # raise ex3
                    else:
                        print("* (unknown error) couldn't finish"
                        " reading \"{}\":".format(subPath))
                        raise ex2
            else:
                print("* (unknown error) couldn't finish"
                      " reading \"{}\":".format(subPath))
                raise ex
        if getVerbose():
            print("* gathering unusable character from \"{}\"".format(sub))
        if key in unusableChars.keys():
            print("Warning: The unusable{} character from \"{}\" was"
                  " already collected from \"{}\" and will be ignored."
                  "".format(tryDelimiter, sub, unusableCharFiles[key]))
            continue
        unusableChars[key] = pathChar
        unusableCharFiles[key] = sub
# print("badChars:{}".format(badChars))

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
    # print(usageS)
    print(__doc__)

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
        print(albumName)
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
                        print("  * Warning: No part of {} starts with"
                              "    a 2-digit track number.")
                if isDigits(songParts[-1][trackDigitsMin+1:]):
                    # In case the song name starts with more than 2
                    # numbers:
                    if isDigits(songParts[-2][:trackDigitsMin]):
                        songName = sep.join(songParts[-2:])
                    elif isDigits(songParts[-3][:trackDigitsMin]):
                        songName = sep.join(songParts[-3:])
                    # else:
                        # print("  * Warning: No part of {} starts with"
                        #       "    a 2-digit track number.")
                '''
            cleanName = ""
            prevBad = False
            for c_orig in songName:
                c = c_orig
                got = unusableChars.get(c)
                if got is not None:
                    c = got
                if isFilenameChar(c):
                    cleanName += c
                    prevBad = False
                else:
                    if not prevBad:
                        songName += "_"
                    prevBad = True
            while cleanName.endswith("_") or cleanName.endswith(" "):
                cleanName = cleanName[:-1]
            print("  {}".format(cleanName))
            songCount += 1
        print("  * processed {} song(s) in {}"
              "".format(songCount, albumName))
        print("")

def main():
    if len(sys.argv) != 2:
        print(usageS)
        exit(1)
    processBand(".", sys.argv[1])

if __name__ == "__main__":
    main()
