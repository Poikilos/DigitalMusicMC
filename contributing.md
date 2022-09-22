# Contributing

This file explains how to help with the project.


## Planned Features
### Playlist Repair
(These features are from the cancelled project ~/Nextcloud/d.cs/DigitalMusicMC/playlistfix)
- [ ] map song after asking once
  - [ ] add the folder of the picked song to search folders
  - [ ] add partial path mapper if drive and/or category folder is different but rest of path is same
  - [ ] if found at mapped location, do not ask
    - [ ] if re-asked, change existing mapping
  - [ ] make a command where if the mapped from and mapped-to both exist, delete the mapped one
    - [ ] map ocremix album song from ocremix.org folder to `Video Game Music\%album%\%disc%\%filetype%\` folder
    - [ ] and MOVE & RENAME if only exists at source (automatically create full dest folder path)
  - [ ] permanently store each type of file path mapper in BOM-marked unicode csv (partial.csv8, Fullname.csv8)
- [ ] allow fixing m3u8 playlists (for loading and unicode byte order chunk, see DigitalMusicMC)
- [ ] remove hardcoded song search root
- [ ] remove hardcoded folder exclusions (sarrExclude)
- [ ] remove hardcoded sarrRequireExactIfStartsWith
- [ ] remove hardcoded Backup_FullName and instances of J:
- [ ] look for ALL possible matches BEFORE user interaction in case there is an exact match that could avoid the need for asking
  - [ ] let user choose the right one if none of them are exact
  - [ ] sort by most likely (closest filename match)
  - [ ] save chosen match in case the same OLD file FullName occurs in another playlist
- [ ] handle: doesn't find or ask about missing MegaDriver songs (moved to album subfolders) for AllByArtist-2009-11-09(Artist-Album-Disc-Track-File_Path)

### Alpha
- [ ] Make the main interface jukebox-style and fully-functional.
- [ ] Play AM background noise during the song to simulate a radio.
- [ ] Make list of checkboxes under headings such as "Hide by tag:" and "Hide by Category:"
  - [ ] defaults under "Hide by tag:"
    "Bleeps and Bloops", "Questionable", "Questionable Title", and "Dark"
  - [ ] default under `"Hide by Score:" <= **`
- [ ] Make many methods of categorizing
- [ ] Make only converted files cached (such as to `%LOCALAPPDATA%\DigitalMusicMC\Music-transfertemp`)
  - [ ] Prevent creation of "Music" folder under that (?)
  - [ ] add option to clear cache
- [ ] Make option to remove playlist from device
  - [ ] THEN copy files created 2013-06-03 to phone ("(New)*.m3u8" before that date)
- [ ] Optionally make paths relative when copying "playlists to folder using name as filename"
- [ ] Make separate copy playlists method (overload) for portable
  - [ ] automatically change playlists to have "/" directory separator
  - [ ] First handle path reconstruction issue where all entries in the playlist start with "./Music/"
    (start with path relative to the playlist file instead).
  - [ ] relative song file naming in playlist
- [ ] Allow "Copy from tree to limited depth tree", "Copy playlist using limited depth"
- [ ] Make sure ffmpeg mode uses lame
  - [ ] Make sure ffmpeg mode works with m4a (should if recent enough version -- in linux (~2005), it needs libavcodec-extra-52 such as from Medibuntu repo!)
    `ffmpeg -i input.m4a -acodec libmp3lame -ab 190k output.mp3`
- [ ] Convert ogg or m4a to wav first to that mencoder works:
  `mplayer -ao pcm:file=targetfile.wav sourcefile.m4a`
- [ ] Save name of open playlist on exit
  - [ ] load on open
- [ ] Implement "hyphen-faux.txt" and "hyphen-real.txt" (faux hyphen is used by discogs.com [between artist and album])
- [ ] Better defaults:
  - [ ] Copy to Device (Copy to Temp folder to avoid commandline-encoder lag glitch, then move finished file automatically):
    - [ ] encodes at 128K to `[PortableMediaPlayerDriveThenSlash]{%albumartist%|%artist%\}{%album%\}{%disc%.}{%track%} %title%.%ext%`
    - [ ] OR
      encodes at 192K to `[PortableMediaPlayerDriveThenSlash]{%file.dir.dir.dir%\}{%albumartist%|%artist%\}{%album%\}{%disc%.}{%track%} %title%.%ext%`
- [ ] Add song metadata (to the comment tag) such as
  `{"generator":"DigitalMusicMC", "tags":["unobtrusive","electronic"]}`
  - [ ] if generator is not `myName`, append a new set of braces: `{generator:DigitalMusicMC}`
- [ ] use LAME for encoding and include LAME sourcecode url
- [ ] option to rename file upon copying to mp3 player (such as `%artist%(%year%) %track% %title%`)
  - [ ] automatically remove groups of two spaces (such as when no `%track%` is specified)
  - [ ] optionally mark characters for deletion on either side of %% var when var is not present
    - [ ] then condense name and replace marked regions with ONE space per region
- [ ] Add option to remove all jpg files (or other extension; non-music by default) from playlists.
- [ ] Show the image in the folder of nearest depth as song thumbnail, named such as: Folder.*, cover.*, album.*
- [ ] stop showing every line in tbStatus upon File, Copy playlists to folder...
- [ ] integrate `D:\Projects\DigitalMusicMC\playlistfix` into DigitalMusicMC
- [ ] Remove files from a playlist if they are in a certain path or subfolder under it (such as `D:\Music\Video Game Music\Final Fantasy VII - Voices of the Lifestream\MP3_unused`)
- [ ] Remove files from a playlist that have a higher-quality equivalent
- [ ] Tag file types:
  - [ ] mp3
  - [ ] flac
  - [ ] mpc
  - [ ] m4p
  - [ ] ogg
  - [ ] it
  - [ ] mod
- [ ] For non-taggable files, handle tagging by reading & writing a `<filename.ext>.DigitalMusicMC.csv`.
  - [ ] OR use .meta, and Read/Write the RealPlayer XML meta file format.
  - [ ] upon load, check if file needs to be moved
    - [ ] maintain a non-redundant list of folder names EVERY time a csv file is saved, then check those locations if the csv file isn't found at first.
    - [ ] the csv file MUST be renamed whenever the file is renamed.
  - [ ] Also do this for tags that can't be saved in the particular format
  - [ ] Do same for m4p etc
  - [ ] If any file is or becomes taggable (program is updated to handle more tag types) and `<filename.ext>.DigitalMusicMC.csv` exists,
    then DigitalMusicMC should overwrite the tags with the data in the file where blank, and ask where different.
    - [ ] Asking where different should occur on a separate message pane to avoid interrupting the user interface.  There should be a permanent queue for questions for the user,
      and questions should never be repeated for a given file within the queue.
    - [ ] There should be a "Use recommended setting for all questions" option in the queue.
      - [ ] "Yes" should be default for overwriting tags with different tags from `<filename.ext>.DigitalMusicMC.csv`
- [ ] Handle duplicate songs -- make an ID or make one version the master copy.
  - [ ] Handle songs from O.C. ReMix albums that are later released in the feed.

### Beta
- [ ] use eyed3 (open source tagging library) instead?? Make sure reads and writes all formats first.
- [ ] Write all metadata that can't be written to tags to filebasename.ext.digitalmusicmc in XML
- [ ] Load tags in a separate thread to avoid interruption (enable sorting methods when finished)
  - [ ] show message if a sort (or other tag operation) is pressed before all tags are loaded

### Final
- [ ] Share songs on the web, and assist people with purchasing and adding songs people recommend to their local playlists or matching up online songs with local ones.
- [ ] Add global hooks for keyboard playback control keys (Play/Pause, Previous, Next such as on Dell optiplex 3040 keyboard)
- [ ] Option: "Move file after changing tag" using ripping destination path
  such as `%Root%/[%Albumartist%/ %or% %Artist%/][%album%/][%track% ][%Title% %or% %filename%]`
- [ ] Search in playlist names
- [ ] Reverse list order
- [ ] Reverse playback of a song
- [ ] Change playback speed
- [ ] Ability to cause a search folder to always set the category (or have a folder set category)
  - [ ] example of search folder sets category:
    all songs found in search folder `E:\Music\vgmix.com` are set to "vgmix.com" category
  - [ ] example of folder set category:
    `E:\Music\%Category%\%Artist%\%Album%` (but never do this, since each of my categories have different folder structure below Category)
- [ ] Undo possible for (applies to any playlist viewer including "Now Playing" playlist):
  - [ ] Clear playlist
  - [ ] Replace "Now Playing" playlist with something else
    - [ ] OPTION 2: make NO now playing playlist
      - [ ] allow playlist1 to be set as "playlist 1 (Now Playing)" and allow moving to next playlist
      - [ ] allows modifying playlists on the fly since other playlists can be viewed without "(Now Playing)" changing to another playlist
- [ ] llow enqueing playlists
  - [ ] label them "(3rd playlist after playlist1)" where "3rd" is the order it will appear and where "playlist1" is the "(Now Playing)" playlist
- [ ] Double-click songs in library to ADD TO QUEUE (the ENQUEUE AFTER LAST ADDED command) - this is good for allowing guests to add songs to queue (by default, add as NEXT SONG AFTER [x] where x is the playing OR LAST ADDED-VIA-ENQUEUE-AFTER-LAST-ADDED song and tell user that)
- [ ] Handle (during load, save, find missing, and find duplicates) instances of "'" in filename.  Example: I once had both "Metal_Gear_Snake%27s_Revenge_OC_ReMix.mp3" and "Metal_Gear_Snake's_Revenge_OC_ReMix.mp3"
- [ ] Show Progress bar after clicking "File", "Copy playlists to folder..."


## Optional
- [ ] add from.Sean filename-based tag generation
  - [ ] see [docs/filename-based_tag_generation--Sean_scheme.md](docs/filename-based_tag_generation--Sean_scheme.md)
- [ ] Make able to play AM noise loop in background
- [ ] Add global hook for multimedia keys (play/pause toggle, stop, previous, next) - allow volume and mute to be handled by the OS
- [ ] Search for files that do not have artwork for their album


## Database Structure
### playlist_items table:
```SQL
CREATE TABLE playlist_items (

  playlist INTEGER NOT NULL,
  type INTEGER NOT NULL DEFAULT 0,
  collection_id INTEGER,
  playlist_url TEXT,

  title TEXT,
  album TEXT,
  artist TEXT,
  albumartist TEXT,
  track INTEGER,
  disc INTEGER,
  year INTEGER,
  originalyear INTEGER,
  genre TEXT,
  compilation INTEGER DEFAULT 0,
  composer TEXT,
  performer TEXT,
  grouping TEXT,
  comment TEXT,
  lyrics TEXT,

  artist_id TEXT,
  album_id TEXT,
  song_id TEXT,

  beginning INTEGER,
  length INTEGER,

  bitrate INTEGER,
  samplerate INTEGER,
  bitdepth INTEGER,

  source INTEGER,
  directory_id INTEGER,
  url TEXT,
  filetype INTEGER,
  filesize INTEGER,
  mtime INTEGER,
  ctime INTEGER,
  unavailable INTEGER DEFAULT 0,

  playcount INTEGER DEFAULT 0,
  skipcount INTEGER DEFAULT 0,
  lastplayed INTEGER DEFAULT 0,

  compilation_detected INTEGER DEFAULT 0,
  compilation_on INTEGER DEFAULT 0,
  compilation_off INTEGER DEFAULT 0,
  compilation_effective INTEGER DEFAULT 0,

  art_automatic TEXT,
  art_manual TEXT,

  effective_albumartist TEXT,
  effective_originalyear INTEGER,

  cue_path TEXT,

  rating INTEGER DEFAULT -1

)
```

### playlists table:
```SQL
CREATE TABLE playlists (

  name TEXT NOT NULL,
  last_played INTEGER NOT NULL DEFAULT -1,
  ui_order INTEGER NOT NULL DEFAULT 0,
  special_type TEXT,
  ui_path TEXT,
  is_favorite INTEGER NOT NULL DEFAULT 0,

  dynamic_playlist_type INTEGER,
  dynamic_playlist_backend TEXT,
  dynamic_playlist_data BLOB

)
```


## Potential Alternate Names
* DigiMC (used by an overseas medical certificate system)


## Why is binary mode used for reading playlists?
There may be mixed or faulty encodings. Reading everything at once
(Then using dmmc.LineReader) rather than line by line prevents some
ugly nested code below, but the code below documents the actual encoding
issues that may occur (possibly due to media players or other tools
writing playlists incorrectly such as with characters inconsistent with
the encoding):
```Python
    def _load(self, stream, path=None, encoding=None):
        lineN = 0
        goodFlag = "#EXTM3U"
        if encoding is not None:
            goodFlag = LineReader.encodingBOMS[encoding] + goodFlag
        for rawL in stream:
            line = rawL.strip()
            lineN += 1
            if lineN == 1:
                if line != goodFlag:
                    raise SyntaxError("{}:{}:1: The file should"
                                      " start with {} but starts"
                                      " with {}."
                                      "".format(path, lineN, goodFlag,
                                                line))
        # Position 6243 (0x1863) (the error excludes the 3 BOM bytes)
        # in "(.Rating) 0of5stars.m3u8" is the accented e in Pokemon
        # (actually 0xE9 (character 233) not a regular 'e').


    def load(self, path):
        # print(path)
        try:
            with open(path, 'r', encoding='utf-8-sig') as ins:
                # "There is no reason to check if a BOM exists or not,
                # utf-8-sig manages that for you and behaves exactly as
                # utf-8 if the BOM does not exist"
                # -lightswitch05 on
                #  <https://stackoverflow.com/a/44573867/4541104>
                return self._load(ins, path=path)
        except UnicodeDecodeError as ex:
            # raise ex
            # such as:
            # "'utf-8' codec can't decode byte 0xe9 in position
            # 6246: invalid continuation byte"
            if "invalid continuation byte" in str(ex):
                tryEncoding = 'latin-1'
                with open(path, 'r', encoding=tryEncoding) as ins:
                    # ^ latin-1 will read the bom as literal characters!
                    return self._load(ins, path=path,
                                      encoding=tryEncoding)
            else:
                print("{}".format(path))
                # /home/owner/Music/Backup/(.Tag) Atmospheric.m3u8
                # at position 0x1218 (4632) (+3 for BOM) has
                # "UnicodeDecodeError: 'utf-8' codec can't decode byte
                # 0xfd in position 4632: invalid start byte"
                # which is the special o in Ragnarok (Actually 0xFD not
                # 'o').
                raise ex
```
