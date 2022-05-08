#!/usr/bin/env python3
import sys
import os
import subprocess

verbose = False


def debug(*args, **kwargs):
    if verbose:
        sys.stderr.write("[debug] ")
        print(*args, file=sys.stderr, **kwargs)


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




# See <https://stackoverflow.com/questions/5574702
# /how-to-print-to-stderr-in-python>:
def error(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


# tryPath = "(New) 2022-04-01 OCR4242-4325.txt"
tryFPRun = "flatpak run --branch=stable --arch=x86_64"
tryFPRun += " --command=strawberry"
tryFPRun += " --file-forwarding org.strawberrymusicplayer.strawberry"
# ^ Based on flatpak-generated Exec line:
'''
/usr/bin/flatpak run --branch=stable --arch=x86_64 --command=strawberry
--file-forwarding org.strawberrymusicplayer.strawberry @@u %U @@
'''

def strawberry_add_to_playlist(path):
    '''
    Call strawberry and add the path to the current playlist (The
    playlist must be open in the Strawberry user interface).

    Raises:
    FileNotFoundError if "Neither strawberry nor flatpak is in the path"
    '''
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
            error("Warning: strawberry isn't in path. Trying {}..."
                  "".format(stawberryPath))
    else:
        strawberryParts = [strawberryPath]
    cmdParts = strawberryParts + ["--append", path]
    subprocess.run(cmdParts, check=True)
    # ^ Check raises an exception on a bad (non-zero) exit code.
    print(path)
    return True


def strawberry_add_to_playlist_from(path):
    '''
    Add files to Strawberry from the list of names in the list file.

    Sequential arguments:
    path -- A list file (Can be m3u format since lines starting with '#'
        are ignored).

    Returns:
    the number of files added (based on count of successful strawberry
    calls).

    Raises:
    - See strawberry_add_to_playlist.
    '''
    count = 0
    debug('* reading paths from "{}"'.format(path))
    with open(path, 'r') as ins:
        lineN = 0
        for rawL in ins:
            lineN += 1
            line = rawL.strip()
            if len(line) < 1:
                continue
            if line.startswith("#"):
                continue
            if not os.path.isfile(line):
                error("* \"{}\" does not exist.".format(line))
                continue
            ok = strawberry_add_to_playlist(line)
            if ok:
                count += 1
    return count


def main():
    global verbose
    src = None
    '''
    if os.path.isfile(tryPath):
        src = tryPath
    if src is None:
    '''
    options = {}
    next_name = None
    bool_names = ["verbose"]
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
                    verbose = True
                    debug("Verbose logging is enabled.")
            else:
                next_name = name
        elif src is None:
            if not os.path.isfile(arg):
                error("Error: {} doesn't exist.".format(arg))
            elif not arg.endswith(".txt"):
                error("Error: {} is not a .txt file.".format(arg))
            else:
                src = arg
    if src is None:
        error("You must provide a txt file (or m3u) that is a list of"
              " music files to add to the current Strawberry playlist.")
        exit(1)
    count = strawberry_add_to_playlist_from(src)
    print("* Done (added {} songs)".format(count))


if __name__ == "__main__":
    main()
