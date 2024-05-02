#!/usr/bin/env python3
import sys
import os
import subprocess

# if os.path.isdir(os.path.join("..", "dmmc")):
#     # sys.path = ["..", sys.path]
#     sys.path.append("..")
from dmmc import (  # noqa: F401
    # PlaylistM3U,
    echo0,
    echo1,
    echo2,
    set_verbosity,
    which,
)


# tryPath = "(New) 2022-04-01 OCR4242-4325.txt"
tryFPRun = "flatpak run --branch=stable --arch=x86_64"
tryFPRun += " --command=strawberry"
tryFPRun += " --file-forwarding org.strawberrymusicplayer.strawberry"
# ^ Based on flatpak-generated Exec line:
"""
/usr/bin/flatpak run --branch=stable --arch=x86_64 --command=strawberry
--file-forwarding org.strawberrymusicplayer.strawberry @@u %U @@
"""


def strawberry_add_to_playlist(path):
    """Call strawberry and add the path to the current playlist
    (The playlist must be open in the Strawberry user interface).

    Raises:
        FileNotFoundError: "Neither strawberry nor flatpak is in the
            path"
    """
    strawberryPath = which("strawberry")
    if strawberryPath is None:
        # strawberryPath = "strawberry"
        stawberryPath = tryFPRun
        strawberryParts = stawberryPath.split()
        flatpakPath = which("flatpak")
        if flatpakPath is None:
            raise FileNotFoundError(
                "Neither strawberry nor flatpak is in the path."
            )
        else:
            echo0(
                "Warning: strawberry isn't in path. Trying {}..."
                "".format(stawberryPath)
            )
    else:
        strawberryParts = [strawberryPath]
    cmdParts = strawberryParts + ["--append", path]
    subprocess.run(cmdParts, check=True)
    # ^ Check raises an exception on a bad (non-zero) exit code.
    print(path)
    return True


def strawberry_add_to_playlist_from(path):
    """Add files to Strawberry based on names in the list file.

    Raises exceptions: See strawberry_add_to_playlist.

    Args:
        path (str): A list file (Can be m3u format since lines starting
            with '#' are ignored).

    Returns:
        int: the number of files added (based on count of successful
            strawberry calls).

    """
    count = 0
    echo1('* reading paths from "{}"'.format(path))
    with open(path, "r") as ins:
        lineN = 0
        for rawL in ins:
            lineN += 1
            line = rawL.strip()
            if len(line) < 1:
                continue
            if line.startswith("#"):
                continue
            if not os.path.isfile(line):
                echo0('* "{}" does not exist.'.format(line))
                continue
            ok = strawberry_add_to_playlist(line)
            if ok:
                count += 1
    return count


def main():
    src = None
    """
    if os.path.isfile(tryPath):
        src = tryPath
    if src is None:
    """
    options = {}
    next_name = None
    bool_names = ["verbose", "debug"]
    for argI in range(1, len(sys.argv)):
        arg = sys.argv[argI]
        if next_name is not None:
            options[next_name] = arg
            next_name = None
        elif arg.startswith("--"):
            name = arg[2:]
            if name in bool_names:
                options[name] = True
                if name == "verbose":
                    set_verbosity(1)
                    echo1("Verbose logging level 1 is enabled.")
                elif name == "debug":
                    set_verbosity(2)
                    echo1("Verbose logging level 2 is enabled.")
            else:
                next_name = name
        elif src is None:
            if not os.path.isfile(arg):
                echo0("Error: {} doesn't exist.".format(arg))
            elif not arg.endswith(".txt"):
                echo0("Error: {} is not a .txt file.".format(arg))
            else:
                src = arg
    if src is None:
        echo0(
            "You must provide a txt file (or m3u) that is a list of"
            " music files to add to the current Strawberry playlist."
        )
        return 1
    count = strawberry_add_to_playlist_from(src)
    print("* Done (added {} songs)".format(count))
    return 0


if __name__ == "__main__":
    sys.exit(main())
