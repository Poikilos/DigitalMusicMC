# DigitalMusicMC
Manage your local music and never listen to another commercial.

The main focus on the project right now is to generate playlists intelligently.

## Project Status
### 2021-06-24
This project is a Python remake of a C# program I made that was never released (but was usable for certain tasks).
- So far this Python remake can:
  - (WIP) (`dmmc/unmangle.py`) unmangle filenames by removing characters not compatible with some operating systems or file systems such as FAT32 for portable devices or drives used by car music players
  - (`dmmc/generate_playlist.py`) generate playlists (Shuffle using numbers in the filename as per the *Sean Naming Scheme*--See below--This should improve eventually).
- This project has been in the pre-alpha stage since at least 2010 as a C# GUI program that:
  - exports songs to portable music players
  - reencodes the files (if not compatible with player or bitrate is enforced)
  - fixes unicode characters in filenames
  - exports WinAmp playlists in bulk, making the filenames readable and the paths relative
  - (and does nothing else)

## Credits
- tsf.svg, tsf-*.* CC0 posted 2014 by [spadassin](https://openclipart.org/user-detail/spadassin) on openclipart.org.
  - See also `tsf license.txt`.
- vintage_radio_drawing_5890254.png CC0 from https://pixy.org/5890254/

## Known Issues
- In mencoder mode, cannot convert from mp4 or ogg and possibly some other common types (only supports mencoder native types AND lame)

## Conventions
### Tagging and Naming
(preliminary)
- If a song is an internet single, the Album tag value should be set to "Song Name [internet single]" where "Song Name" is the song name (" [internet single]" is literal).
#### Sean Naming Scheme
The Sean Naming Scheme (SNS) is a scheme for adding various metrics to Sean's massive collection by changing the filename. This is the situation because Sean is an archivalist using obscure formats with elusive tagging support, and he doesn't have advanced software or the skills to use it. Whether or not using the filename will be the ongoing method, the plan for supporting the SNS is as follows:
- Derive the meaning of all characters in every filename in [tests/filename-based_tag_generation--Sean_Naming_Scheme-songs.txt](tests/filename-based_tag_generation--Sean_Naming_Scheme-songs.txt)

The main advantage is that it is a multi-dimensional (or multi-metric) naming scheme, So you can have:
1. Album, Artist, etc. (common metadata)
2. Category
3. Tag
4. Rating

Combining the data allows shuffling (or generating shuffled playlists) intelligently for huge collections.
- Playing all top-rated songs would be obtrusive, but using a generator string (see generate_playlist.py) such as `11211121113` you can space out the high-rated songs (on a scale of `0-3`).
  - This makes the playlist good for long playback since it is both unobtrusive and breaks up the boredom.
- Adding in other metrics such as tags (such as "party") or category (such as "instrumental") adds multiple metrics, not merely multiple tags. Having both tags and categories as separate metrics enables better results.
  - You don't need cloud AI to have a good selection. You can make your own decisions and this software can help you.


## Planned Features
### Playlist Repair
(These features are from the cancelled project ~/Nextcloud/d.cs/DigitalMusicMC/playlistfix)
- map song after asking once
  - add the folder of the picked song to search folders
  - add partial path mapper if drive and/or category folder is different but rest of path is same
  - if found at mapped location, do not ask
    - if re-asked, change existing mapping
  - make a command where if the mapped from and mapped-to both exist, delete the mapped from
    e.g. map ocremix album song from ocremix.org folder to Video Game Music\%album%\%disc%\%filetype%\ folder
    - and MOVE & RENAME if only exists at source (automatically create full dest folder path)
  - permanently store each type of file path mapper in BOM-marked unicode csv (partial.csv8, Fullname.csv8)
- allow fixing m3u8 playlists (for loading and unicode byte order chunk, see DigitalMusicMC)
- remove hardcoded song search root
- remove hardcoded folder exclusions (sarrExclude)
- remove hardcoded sarrRequireExactIfStartsWith
- remove hardcoded Backup_FullName and instances of J:
- look for ALL possible matches BEFORE user interaction in case there is an exact match that could avoid the need for asking
  - let user choose the right one if none of them are exact
  - sort by most likely (closest filename match)
  - save chosen match in case the same OLD file FullName occurs in another playlist
- handle: doesn't find or ask about missing MegaDriver songs (moved to album subfolders) for AllByArtist-2009-11-09(Artist-Album-Disc-Track-File_Path)

### Alpha
- Make the main interface jukebox-style and fully-functional.
- Play AM background noise during the song to simulate a radio.
- Make list of checkboxes under headings such as "Hide by tag:" and "Hide by Category:"
  - defaults under "Hide by tag:"
    "Bleeps and Bloops", "Questionable", "Questionable Title", and "Dark"
  - default under "Hide by Score:" <= **
- Make many methods of categorizing
- Make only converted files cached (such as to "%LOCALAPPDATA%\DigitalMusicMC\Music-transfertemp")
  - Prevent creation of "Music" folder under that (?)
  - add option to clear cache
- Make option to remove playlist from device
  - THEN copy files created 2013-06-03 to phone ("(New)*.m3u8" before that date)
- Optionally make paths relative when copying "playlists to folder using name as filename"
- Make separate copy playlists method (overload) for portable
  - automatically change playlists to have "/" directory separator
  - First handle path reconstruction issue where all entries in the playlist start with "./Music/"
    (start with path relative to the playlist file instead).
  - relative song file naming in playlist
- Allow "Copy from tree to limited depth tree", "Copy playlist using limited depth"
- Make sure ffmpeg mode uses lame
  - Make sure ffmpeg mode works with m4a (should if recent enough version -- in linux (~2005), it needs libavcodec-extra-52 such as from Medibuntu repo!)
    `ffmpeg -i input.m4a -acodec libmp3lame -ab 190k output.mp3`
- Convert ogg or m4a to wav first to that mencoder works:
  `mplayer -ao pcm:file=targetfile.wav sourcefile.m4a`
- Save name of open playlist on exit
  - load on open
- Implement "hyphen-faux.txt" and "hyphen-real.txt" (faux hyphen is used by discogs.com [between artist and album])
- Better defaults:
  - Copy to Device (Copy to Temp folder to avoid commandline-encoder lag glitch, then move finished file automatically):
    - encodes at 128K to `[PortableMediaPlayerDriveThenSlash]{%albumartist%|%artist%\}{%album%\}{%disc%.}{%track%} %title%.%ext%`
    - OR
      encodes at 192K to `[PortableMediaPlayerDriveThenSlash]{%file.dir.dir.dir%\}{%albumartist%|%artist%\}{%album%\}{%disc%.}{%track%} %title%.%ext%`
- Add song metadata (to the comment tag) such as
  `{"generator":"DigitalMusicMC", "tags":["unobtrusive","electronic"]}`
  - if generator is not `myName`, append a new set of braces: `{generator:DigitalMusicMC}`
- use LAME for encoding and include LAME sourcecode url
- option to rename file upon copying to mp3 player (such as `%artist%(%year%) %track% %title%`)
  - automatically remove groups of two spaces (such as when no `%track%` is specified)
  - optionally mark characters for deletion on either side of %% var when var is not present
    - then condense name and replace marked regions with ONE space per region
- Add option to remove all jpg files (or other extension; non-music by default) from playlists.
- Show the image in the folder of nearest depth as song thumbnail, named such as: Folder.*, cover.*, album.*
- stop showing every line in tbStatus upon File, Copy playlists to folder...
- integrate D:\Projects\DigitalMusicMC\playlistfix into DigitalMusicMC
- Remove files from a playlist if they are in a certain path or subfolder under it (such as `D:\Music\Video Game Music\Final Fantasy VII - Voices of the Lifestream\MP3_unused`)
- Remove files from a playlist that have a higher-quality equivalent
- Tag file types:
  - mp3
  - flac
  - mpc
  - m4p
  - ogg
  - it
  - mod
- For non-taggable files, handle tagging by reading & writing a `<filename.ext>.DigitalMusicMC.csv`.
  - OR use .meta, and Read/Write the RealPlayer XML meta file format.
  - upon load, check if file needs to be moved
    - maintain a non-redundant list of folder names EVERY time a csv file is saved, then check those locations if the csv file isn't found at first.
    - the csv file MUST be renamed whenever the file is renamed.
  - Also do this for tags that can't be saved in the particular format
  - Do same for m4p etc
  - If any file is or becomes taggable (program is updated to handle more tag types) and `<filename.ext>.DigitalMusicMC.csv` exists,
    then DigitalMusicMC should overwrite the tags with the data in the file where blank, and ask where different.
    - Asking where different should occur on a separate message pane to avoid interrupting the user interface.  There should be a permanent queue for questions for the user,
      and questions should never be repeated for a given file within the queue.
    - There should be a "Use recommended setting for all questions" option in the queue.
      - "Yes" should be default for overwriting tags with different tags from `<filename.ext>.DigitalMusicMC.csv`
- Handle duplicate songs -- make an ID or make one version the master copy.
  - Handle songs from O.C. ReMix albums that are later released in the feed.

### Beta
- use eyed3 (open source tagging library) instead?? Make sure reads and writes all formats first.
- Write all metadata that can't be written to tags to filebasename.ext.digitalmusicmc in XML
- Load tags in a separate thread to avoid interruption (enable sorting methods when finished)
  - show message if a sort (or other tag operation) is pressed before all tags are loaded

### Final
- Share songs on the web, and assist people with purchasing and adding songs people recommend to their local playlists or matching up online songs with local ones.
- Add global hooks for keyboard playback control keys (Play/Pause, Previous, Next such as on Dell optiplex 3040 keyboard)
- Option: "Move file after changing tag" using ripping destination path
  such as `%Root%/[%Albumartist%/ %or% %Artist%/][%album%/][%track% ][%Title% %or% %filename%]`
- Search in playlist names
- Reverse list order
- Reverse playback of a song
- Change playback speed
- Ability to cause a search folder to always set the category (or have a folder set category)
  - example of search folder sets category:
    all songs found in search folder "E:\Music\vgmix.com" are set to "vgmix.com" category
  - example of folder set category:
    `E:\Music\%Category%\%Artist%\%Album%` (but never do this, since each of my categories have different folder structure below Category)
- Undo possible for (applies to any playlist viewer including "Now Playing" playlist):
  - Clear playlist
  - Replace "Now Playing" playlist with something else
    - OPTION 2: make NO now playing playlist
      - allow playlist1 to be set as "playlist 1 (Now Playing)" and allow moving to next playlist
      - allows modifying playlists on the fly since other playlists can be viewed without "(Now Playing)" changing to another playlist
- Allow enqueing playlists
  - label them "(3rd playlist after playlist1)" where "3rd" is the order it will appear and where "playlist1" is the "(Now Playing)" playlist
- Double-click songs in library to ADD TO QUEUE (the ENQUEUE AFTER LAST ADDED command) - this is good for allowing guests to add songs to queue (by default, add as NEXT SONG AFTER [x] where x is the playing OR LAST ADDED-VIA-ENQUEUE-AFTER-LAST-ADDED song and tell user that)
- Handle (during load, save, find missing, and find duplicates) instances of "'" in filename.  Example: I once had both "Metal_Gear_Snake%27s_Revenge_OC_ReMix.mp3" and "Metal_Gear_Snake's_Revenge_OC_ReMix.mp3"
- Show Progress bar after clicking "File", "Copy playlists to folder..."

## Optional
- add from.Sean filename-based tag generation
  - see [docs/filename-based_tag_generation--Sean_scheme.md](docs/filename-based_tag_generation--Sean_scheme.md)
- Make able to play AM noise loop in background
- Add global hook for multimedia keys (play/pause toggle, stop, previous, next) - allow volume and mute to be handled by the OS
- Search for files that do not have artwork for their album


## Developer Notes
### Potential Alternate Names
* DigiMC (used by an overseas medical certificate system)
