#!/usr/bin/env python3
from __future__ import print_function
import argparse
from mutagen.flac import FLAC


def clean_title(title, *args):
    """Remove patterns from " - " delimited title."""
    patterns = [
    ]
    for arg in args:
        patterns += [
            " - %s - " % arg,
            " - %s" % arg,
            "%s - " % arg
        ]
    for pattern in patterns:
        title = title.replace(pattern, "")
    return title


def main():
    parser = argparse.ArgumentParser(description="Clean FLAC file title tags.")
    parser.add_argument("file", type=str, help="Path to the FLAC file")

    args = parser.parse_args()

    # Load the FLAC file
    audio = FLAC(args.file)

    # Extract the title, artist, and album title
    title = audio.get("title", [""])[0]
    # print("title=\"%s\"" % title)
    artist = audio.get("artist", [""])[0]
    album_title = audio.get("album", [""])[0]

    # Clean the title by removing patterns
    cleaned_title = clean_title(title, artist, album_title)

    # Save the cleaned title back to the FLAC file
    if cleaned_title != title:
        audio["title"] = cleaned_title
        audio.save()
        print("Changed title from \"%s\" to \"%s\"" % (title, cleaned_title))
    else:
        print("No changes made to the title \"%s\"." % title)

if __name__ == "__main__":
    main()
